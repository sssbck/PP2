import yt_dlp
import os
import subprocess
import json
import shutil
from mutagen.mp3 import MP3

class MusicEngine:
    def __init__(self):
        self.cache_dir = "music_cache"
        self.download_dir = "downloads"
        self.is_shuffled = False
        self.is_repeating = False
        self.current_context = "cache" # "favorites" или "downloads"
        # Создаем обе папки
        for d in [self.cache_dir, self.download_dir]:
            if not os.path.exists(d): os.makedirs(d)
        
        self.playlist = []
        self.favorites = [] # Храним только названия (строки)
        self.downloaded_files = [] # Храним пути к файлам в папке downloads
        self.current_index = -1
        self.duration = 0 
        self.original_duration = 0
        
        self.load_data() # Загружаем сохраненки при старте

    def load_data(self):
        try:
            if os.path.exists("user_data.json"):
                with open("user_data.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.favorites = data.get("favorites", [])
                    self.downloaded_files = data.get("downloads", [])
        except Exception as e:
            print(f"Load error: {e}")

    def save_data(self):
        with open("user_data.json", "w", encoding="utf-8") as f:
            json.dump({
                "favorites": self.favorites,
                "downloads": self.downloaded_files
            }, f, ensure_ascii=False, indent=4)
    
    def sync_favorites(self):
        """Проверяет избранное и докачивает то, чего нет в Downloads"""
        print("Синхронизация облачных треков...")
        for fav_name in self.favorites:
            # Проверяем, нет ли этого файла в папке Downloads
            local_path = os.path.join(self.download_dir, fav_name)
            cache_path = os.path.join(self.cache_dir, fav_name)
            
            if os.path.exists(local_path):
                print(f"{fav_name} уже есть в Downloads, пропускаем.")
                if local_path not in self.playlist:
                    self.playlist.append(local_path)
                continue
            
            if not os.path.exists(cache_path):
                print(f"Загрузка облачного трека: {fav_name}")
                # Мы вызываем поиск, но передаем название файла как запрос
                # Убираем расширение .mp3 для более точного поиска
                query = fav_name.replace(".mp3", "")
                self.search_and_download(query)
            else:
                if cache_path not in self.playlist:
                    self.playlist.append(cache_path)

    def cleanup_cache(self):
        """Удаляет все файлы из кэша, которых нет в Downloads"""
        for file in os.listdir(self.cache_dir):
            file_path = os.path.join(self.cache_dir, file)
            # Если файла нет в списке избранных или скачанных - удаляем
            if file not in [os.path.basename(f) for f in self.downloaded_files]:
                try:
                    os.remove(file_path)
                except: pass

    def search_and_download(self, query):
        ffmpeg_path = os.path.join(os.getcwd(), "ffmpeg.exe")
        ydl_opts = {
            'format': 'bestaudio/best',
            'default_search': 'ytsearch1',
            'outtmpl': f'{self.cache_dir}/%(title)s.%(ext)s',
            'noplaylist': True,
            'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}],
            'ffmpeg_location': ffmpeg_path if os.path.exists(ffmpeg_path) else None,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(query, download=True)
                path = ydl.prepare_filename(info['entries'][0]).rsplit('.', 1)[0] + ".mp3"
                if path not in self.playlist:
                    self.playlist.append(path)
                self.current_index = self.playlist.index(path)
                
                audio = MP3(path)
                self.duration = audio.info.length
                self.original_duration = self.duration
                return path
            except Exception as e:
                print(f"Engine Error: {e}")
                return None

    def toggle_favorite(self):
        if self.current_index != -1:
            name = os.path.basename(self.playlist[self.current_index])
            if name in self.favorites:
                self.favorites.remove(name)
            else:
                self.favorites.append(name)
            self.save_data()

    def permanent_download(self):
        """Копирует файл из кэша в папку downloads навсегда"""
        if self.current_index != -1:
            source_path = self.playlist[self.current_index]
            filename = os.path.basename(source_path)
            dest_path = os.path.join(self.download_dir, filename)
            
            if not os.path.exists(dest_path):
                shutil.copy(source_path, dest_path)
                if dest_path not in self.downloaded_files:
                    self.downloaded_files.append(dest_path)
                self.save_data()

    def change_speed(self, speed=1.0, current_path=None):
        if not current_path or not os.path.exists(current_path):
            return None
            
        # Генерируем имя для кэша скорости
        # Пример: Ice_Baby.mp3 -> Ice_Baby_1.5.mp3
        base_name = os.path.basename(current_path).rsplit('.', 1)[0]
        output_name = f"{base_name}_{speed}.mp3"
        output_path = os.path.join(self.cache_dir, output_name)
        
        if not os.path.exists(output_path):
            ffmpeg_path = os.path.join(os.getcwd(), "ffmpeg.exe")
            # Команда фильтра: atempo (меняет скорость без смены тональности)
# Замени старый cmd на этот (добавили -preset ultrafast и понизили битрейт для скорости)
            cmd = [
            ffmpeg_path, '-i', current_path, 
            '-filter:a', f'atempo={speed}', 
            '-vn', '-y', '-preset', 'ultrafast', # Ускоряет сам процесс конвертации
            '-acodec', 'libmp3lame', '-b:a', '128k', # 128k хватит для плеера, но создастся быстрее
            output_path
            ]
            try:
                # Используем subprocess.run для контроля
                subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception as e:
                print(f"FFmpeg Error: {e}")
                return None
        
        # Обновляем длительность под новый файл
        audio = MP3(output_path)
        self.duration = audio.info.length 
        return output_path
    
    def set_current_by_path(self, path):
        """Принудительно устанавливает индекс по пути к файлу"""
        if path not in self.playlist:
            self.playlist.append(path)
        self.current_index = self.playlist.index(path)

    def get_current_track_name(self):
        if self.current_index != -1:
            name = os.path.basename(self.playlist[self.current_index])
            return (name[:35] + '..') if len(name) > 35 else name
        return "READY TO STREAM"