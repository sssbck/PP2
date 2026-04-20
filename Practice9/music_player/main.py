import pygame
import sys
import os
import random
import math
from music_engine import MusicEngine
from mutagen.mp3 import MP3

# Константы стиля
BG_DARK = (10, 10, 18)
ACCENT = (0, 255, 255)
PANEL = (20, 20, 35)
RED_ACCENT = (255, 50, 100)

class Button:
    def __init__(self, x, y, w, h, text, color, id=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.id = id
        self.hovered = False

    def draw(self, screen, font, active=False):
        c = (min(self.color[0]+60, 255), min(self.color[1]+60, 255), min(self.color[2]+30, 255)) if active or self.hovered else self.color
        pygame.draw.rect(screen, c, self.rect, border_radius=10)
        if self.hovered or active:
            pygame.draw.rect(screen, ACCENT, self.rect, 2, border_radius=10)
        txt = font.render(self.text, True, (250, 250, 250))
        screen.blit(txt, txt.get_rect(center=self.rect.center))

def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((900, 600))
    pygame.display.set_caption("CyberTube Studio v3.0 | PRO MODE")
    clock = pygame.time.Clock()
    
    engine = MusicEngine()
    engine.sync_favorites()
    
    # СОСТОЯНИЕ
    play_offset = 0  
    current_speed = 1.0 
    query = ""
    status = "READY TO STREAM"
    loading = False
    is_repeating = False
    is_shuffled = False
    current_context = "search" 
    current_idx = 0 

    font_b = pygame.font.SysFont("Verdana", 20, bold=True)
    font_m = pygame.font.SysFont("Verdana", 17)
    font_s = pygame.font.SysFont("Verdana", 13)
    
    wave_points = [random.randint(5, 70) for _ in range(70)]
    
    # Кнопки нижнего пульта
    btn_prev = Button(310, 500, 50, 45, "<<", (40, 40, 80), "prev")
    btn_play = Button(370, 500, 140, 45, "PLAY/PAUSE", (50, 50, 110), "play")
    btn_next = Button(520, 500, 50, 45, ">>", (40, 40, 80), "next")
    btn_rep  = Button(580, 500, 85, 45, "REPEAT", (60, 40, 60), "rep")
    btn_shuf = Button(675, 500, 85, 45, "SHUFFLE", (40, 60, 60), "shuf")

    def load_track(idx, context):
        nonlocal play_offset, current_idx, current_context, status, current_speed
        current_idx = idx
        current_context = context
        
        # Получаем список
        track_list = engine.favorites if context == "favorites" else engine.downloaded_files
        if not track_list: return

        target = track_list[current_idx]
        if context == "favorites":
            path = os.path.join(engine.cache_dir, target)
            if not os.path.exists(path): path = os.path.join(engine.download_dir, target)
        else:
            path = target

        if os.path.exists(path):
            play_offset = 0
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
            status = os.path.basename(path)
            engine.original_duration = MP3(path).info.length
            # Сбрасываем скорость при смене трека для стабильности
            current_speed = 1.0 

    def next_track():
        track_list = engine.favorites if current_context == "favorites" else engine.downloaded_files
        if not track_list: return
        if is_shuffled:
            new_idx = random.randint(0, len(track_list)-1)
        else:
            new_idx = (current_idx + 1) % len(track_list)
        load_track(new_idx, current_context)

    def prev_track():
        track_list = engine.favorites if current_context == "favorites" else engine.downloaded_files
        if not track_list: return
        new_idx = (current_idx - 1) % len(track_list)
        load_track(new_idx, current_context)

    while True:
        m_pos = pygame.mouse.get_pos()
        for y in range(600):
            c = (10, 10, 18 + y // 50)
            pygame.draw.line(screen, c, (0, y), (900, y))

        # --- ОБРАБОТКА СОБЫТИЙ ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                engine.cleanup_cache()
                pygame.quit(); sys.exit()
            
            for b in [btn_prev, btn_play, btn_next, btn_rep, btn_shuf]:
                b.hovered = b.rect.collidepoint(m_pos)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = m_pos
                
                # --- 1. ВЗАИМОДЕЙСТВИЕ С SIDEBAR ---
                if 0 <= mx <= 280:
                    path = None # Инициализируем, чтобы не было ошибки UnboundLocalError
                    
                    # Клик по FAVORITES
                    if 65 <= my <= 300:
                        current_context = "favorites"
                        display_favs = engine.favorites[-10:]
                        index = (my - 65) // 22
                        
                        if 0 <= index < len(display_favs):
                            target_name = display_favs[index]
                            # Проверяем сначала в кэше, потом в загрузках
                            p_cache = os.path.join(engine.cache_dir, target_name)
                            p_dl = os.path.join(engine.download_dir, target_name)
                            path = p_dl if os.path.exists(p_dl) else p_cache

                    # Клик по DOWNLOADS
                    elif 360 <= my <= 580:
                        current_context = "downloads"
                        display_dls = engine.downloaded_files[-10:]
                        index = (my - 360) // 22
                        
                        if 0 <= index < len(display_dls):
                            path = display_dls[index]

                    # Если путь был найден (клик попал в трек)
                    if path and os.path.exists(path):
                        # СИНХРОНИЗИРУЕМ ИНДЕКС (решает баг с Ice Baby)
                        engine.set_current_by_path(path)
                        
                        play_offset = 0
                        pygame.mixer.music.load(path)
                        pygame.mixer.music.play()
                        status = os.path.basename(path)
                        
                        # Обновляем длительность для нового трека
                        from mutagen.mp3 import MP3
                        engine.original_duration = MP3(path).info.length
                        current_speed = 1.0 # Сброс скорости для нового трека

                # --- 2. ПЕРЕМОТКА ПО ВОЛНЕ ---
                if 320 <= mx <= 880 and 340 <= my <= 420:
                    if engine.original_duration > 0:
                        percent = (mx - 320) / (880 - 320)
                        play_offset = percent * engine.original_duration 
                        pygame.mixer.music.play(start=play_offset / current_speed)

                # --- 3. ИКОНКИ ЛАЙК / СКАЧАТЬ ---
                if 780 <= mx <= 810 and 265 <= my <= 295: engine.toggle_favorite()
                if 830 <= mx <= 860 and 265 <= my <= 295: engine.permanent_download()

                # --- 4. ПУЛЬТ УПРАВЛЕНИЯ ---
                if btn_play.rect.collidepoint(m_pos):
                    if pygame.mixer.music.get_busy(): pygame.mixer.music.pause()
                    else: pygame.mixer.music.unpause()
                if btn_next.hovered: next_track()
                if btn_prev.hovered: prev_track()
                if btn_rep.hovered: is_repeating = not is_repeating
                if btn_shuf.hovered: is_shuffled = not is_shuffled

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and query.strip():
                    path = engine.search_and_download(query)
                    if path:
                        current_context = "search"; play_offset = 0
                        pygame.mixer.music.load(path); pygame.mixer.music.play()
                        status = engine.get_current_track_name()
                        current_speed = 1.0
                    query = ""
                elif event.key == pygame.K_BACKSPACE: query = query[:-1]
                # ПРОБЕЛ: Пауза / Возобновление
                elif event.key == pygame.K_SPACE:
                    if pygame.mixer.music.get_busy(): 
                        pygame.mixer.music.pause()
                    else: 
                        pygame.mixer.music.unpause()

                # КЛАВИША L: Следующий трек
                elif event.key == pygame.K_l:
                    next_track()

                # КЛАВИША K: Предыдущий трек
                elif event.key == pygame.K_k:
                    prev_track()
                elif event.key in [pygame.K_UP, pygame.K_DOWN]:
                    if status != "READY TO STREAM":
                        # 1. Находим чистый исходник (без цифр скорости в названии)
                        # Ищем оригинальный файл в папках
                        raw_name = status
                        if "_" in raw_name and any(s in raw_name for s in ["0.5", "1.5", "2.0", "1.25", "0.75"]):
                            # Пытаемся восстановить имя оригинала (очень грубо, но для теста пойдет)
                            raw_name = raw_name.split("_")[0] + ".mp3"
                        
                        p_cache = os.path.join(engine.cache_dir, raw_name)
                        p_dl = os.path.join(engine.download_dir, raw_name)
                        raw_path = p_dl if os.path.exists(p_dl) else p_cache

                        # 2. Считаем позицию
                        curr_ms = pygame.mixer.music.get_pos()
                        actual_pos = play_offset + (max(0, curr_ms) / 1000) * current_speed
                        

                        # 3. Меняем скорость
                        if event.key == pygame.K_UP: current_speed = min(current_speed + 0.25, 2.0)
                        else: current_speed = max(current_speed - 0.25, 0.5)
                        
                        # 4. ПЕРЕЗАПУСК (Критический момент)
                        pygame.mixer.music.stop() # Останавливаем старый поток
                        pygame.mixer.music.unload() # Выгружаем файл из памяти
                        
                        new_path = engine.change_speed(current_speed, current_path=raw_path)
                        
                        if new_path:
                            play_offset = actual_pos
                            pygame.mixer.music.load(new_path)
                            pygame.mixer.music.play(start=play_offset / current_speed)
                elif event.key == pygame.K_LEFT:
                    play_offset = max(0, (play_offset + (pygame.mixer.music.get_pos()/1000)*current_speed) - 5)
                    pygame.mixer.music.play(start=play_offset / current_speed)
                elif event.key == pygame.K_RIGHT:
                    play_offset = min(engine.original_duration, (play_offset + (pygame.mixer.music.get_pos()/1000)*current_speed) + 5)
                    pygame.mixer.music.play(start=play_offset / current_speed)
                else:
                    if event.unicode.isprintable(): query += event.unicode

        # --- АВТОМАТИКА ПЕРЕКЛЮЧЕНИЯ ---
        curr_ms = pygame.mixer.music.get_pos()
        if curr_ms == -1: curr_ms = 0
        actual_time = play_offset + (curr_ms / 1000) * current_speed
        total_sec = engine.original_duration if engine.original_duration > 0 else 1
        
        if actual_time >= total_sec - 0.2: # Почти конец трека
            if is_repeating:
                play_offset = 0
                pygame.mixer.music.play(start=0)
            else:
                next_track() # Сами идем дальше

        # --- ОТРИСОВКА ---
        # Sidebar
        pygame.draw.rect(screen, (15, 15, 25), (0, 0, 280, 600))
        pygame.draw.line(screen, (40, 40, 60), (280, 0), (280, 600), 2)
        screen.blit(font_b.render("FAVORITES", True, RED_ACCENT), (20, 30))
        for i, fav_name in enumerate(engine.favorites[-10:]):
            color = ACCENT if (current_context == "favorites" and fav_name == status) else (180, 180, 180)
            screen.blit(font_s.render(f"♥ {fav_name[:28]}", True, color), (20, 65 + i*22))
        screen.blit(font_b.render("DOWNLOADS", True, ACCENT), (20, 325))
        for i, dl_path in enumerate(engine.downloaded_files[-10:]):
            name = os.path.basename(dl_path)
            color = ACCENT if (current_context == "downloads" and name == status) else (180, 180, 180)
            screen.blit(font_s.render(f"↓ {name[:28]}", True, color), (20, 360 + i*22))

        # Search / Context
        s_rect = pygame.Rect(310, 40, 550, 55)
        pygame.draw.rect(screen, (5, 5, 10), s_rect, border_radius=15)
        pygame.draw.rect(screen, (60, 60, 90), s_rect, 1, border_radius=15)
        q_surf = font_b.render(f"SEARCH: {query}", True, ACCENT)
        screen.blit(q_surf, (335, 53))
        screen.blit(font_s.render(f"PLAYING FROM: {current_context.upper()}", True, (100, 100, 150)), (320, 250))

        # Название и Иконки
        screen.blit(font_b.render(status[:45], True, (255, 255, 255)), (320, 270))
        h_col = RED_ACCENT if status in engine.favorites else (80, 80, 80)
        pygame.draw.circle(screen, h_col, (790, 275), 5); pygame.draw.circle(screen, h_col, (800, 275), 5)
        pygame.draw.polygon(screen, h_col, [(784, 278), (806, 278), (795, 288)])
        d_col = ACCENT if any(os.path.basename(p) == status for p in engine.downloaded_files) else (80, 80, 80)
        pygame.draw.line(screen, d_col, (845, 270), (845, 285), 2); pygame.draw.polygon(screen, d_col, [(840, 280), (850, 280), (845, 288)])

        # Волна
        for i, h in enumerate(wave_points):
            color = ACCENT if (i / len(wave_points)) < (actual_time / total_sec) else (60, 60, 90)
            pygame.draw.rect(screen, color, (320 + i*8, 380 - h//2, 6, h), border_radius=3)

        # Таймер
        cursor_x = 320 + (actual_time / total_sec) * (70 * 8)
        pygame.draw.line(screen, ACCENT, (cursor_x, 340), (cursor_x, 420), 2)
        time_str = f"{int(actual_time//60):02}:{int(actual_time%60):02} / {int(total_sec//60):02}:{int(total_sec%60):02}"
        screen.blit(font_s.render(time_str, True, ACCENT), (320, 425))
        screen.blit(font_m.render(f"{current_speed}x", True, (255, 255, 0)), (830, 425))

        # Пульт
        btn_prev.draw(screen, font_s)
        btn_play.draw(screen, font_s)
        btn_next.draw(screen, font_s)
        btn_rep.draw(screen, font_s, active=is_repeating)
        btn_shuf.draw(screen, font_s, active=is_shuffled)

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()