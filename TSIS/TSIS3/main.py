import pygame
import os
from persistence import load_settings, save_score
from ui import main_menu_screen, settings_screen, leaderboard_screen, game_over_screen
from racer import run_game, SCREEN_WIDTH, SCREEN_HEIGHT

def main():
    pygame.init()
    pygame.mixer.init() # Инициализация звукового движка
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("TSIS 3: Racer Pro")

    settings = load_settings()
    
    # Загрузка и запуск фоновой музыки
    try:
        # Пытаемся загрузить музыку (предполагаем расширение .mp3 или .wav)
        music_path = os.path.join("assets", "background_music.mp3")
        if not os.path.exists(music_path):
            music_path = os.path.join("assets", "background_music.wav")
        
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(0.5)
        if settings["sound"]:
            pygame.mixer.music.play(-1) # -1 означает зациклить
    except Exception as e:
        print(f"Music file warning: {e}")

    current_state = "menu"
    last_score, last_dist, last_coins = 0, 0, 0

    while True:
        if current_state == "menu":
            current_state = main_menu_screen(screen, settings)
            
        elif current_state == "settings":
            old_sound_state = settings["sound"]
            current_state = settings_screen(screen, settings)
            
            # Динамическое включение/выключение музыки
            if settings["sound"] and not old_sound_state:
                pygame.mixer.music.play(-1)
            elif not settings["sound"] and old_sound_state:
                pygame.mixer.music.stop()
            
        elif current_state == "leaderboard":
            current_state = leaderboard_screen(screen)
            
        elif current_state == "play":
            result = run_game(screen, settings)
            if result[0] == "quit":
                break
            elif result[0] == "game_over":
                _, last_score, last_dist, last_coins = result
                save_score(settings["last_username"], last_score, last_dist)
                current_state = "game_over"
                
        elif current_state == "game_over":
            current_state = game_over_screen(screen, last_score, last_dist, last_coins)
            
        elif current_state == "quit":
            break

    pygame.quit()

if __name__ == "__main__":
    main()