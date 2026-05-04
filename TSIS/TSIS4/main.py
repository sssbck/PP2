# main.py
import pygame, sys, json, os
from config import *
from db import init_db, save_score, get_top_10, get_pb
from game import SnakeGame

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 25, bold=True)
init_db()

# В main.py исправь функцию:
def load_settings():
    if os.path.exists("settings.json"):
        try:
            with open("settings.json", "r") as f:
                data = json.load(f)
                # Проверка: если ключа нет, добавляем его вручную
                if 'grid' not in data: data['grid'] = True 
                return data
        except:
            pass
    # Если файла нет или он сломан, возвращаем стандарт
    return {"color": (0, 255, 0), "grid": True, "sound": True}

class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x - w//2, y, w, h)
        self.text = text
    def draw(self, surf):
        h = self.rect.collidepoint(pygame.mouse.get_pos())
        pygame.draw.rect(surf, LIGHT_GRAY if h else GRAY, self.rect, border_radius=10)
        t = font.render(self.text, True, BLACK if h else WHITE)
        surf.blit(t, t.get_rect(center=self.rect.center))
        return h

state, username = "MENU", ""
settings = load_settings()

while True:
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT: pygame.quit(); sys.exit()
    
    screen.fill(BLACK)
    
    if state == "MENU": #
        play_btn, lb_btn, set_btn = Button(400, 300, 200, 45, "PLAY"), Button(400, 360, 200, 45, "LEADERBOARD"), Button(400, 420, 200, 45, "SETTINGS")
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_BACKSPACE: username = username[:-1]
                else: username += e.unicode
            if e.type == pygame.MOUSEBUTTONDOWN:
                if play_btn.draw(screen) and username: game = SnakeGame(username, settings, get_pb(username)); state = "PLAY"
                if lb_btn.draw(screen): state = "LB"
                if set_btn.draw(screen): state = "SET"
        play_btn.draw(screen); lb_btn.draw(screen); set_btn.draw(screen)
        t = font.render(f"NAME: {username}", True, YELLOW)
        screen.blit(t, (300, 230))

    elif state == "PLAY":
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP and game.dy == 0: game.dx, game.dy = 0, -BLOCK_SIZE
                if e.key == pygame.K_DOWN and game.dy == 0: game.dx, game.dy = 0, BLOCK_SIZE
                if e.key == pygame.K_LEFT and game.dx == 0: game.dx, game.dy = -BLOCK_SIZE, 0
                if e.key == pygame.K_RIGHT and game.dx == 0: game.dx, game.dy = BLOCK_SIZE, 0
        game.update()
        game.draw(screen)
        info = font.render(f"Score: {game.score} | Lvl: {game.level} | PB: {game.pb}", True, WHITE)
        screen.blit(info, (10, 10))
        if game.game_over: save_score(username, game.score, game.level); state = "GAME_OVER"
        clock.tick(game.current_speed); pygame.display.flip(); continue

    elif state == "GAME_OVER": #
        retry = Button(400, 350, 180, 45, "RETRY")
        menu = Button(400, 410, 180, 45, "MENU")
        if retry.draw(screen) and any(e.type == pygame.MOUSEBUTTONDOWN for e in events): 
            game = SnakeGame(username, settings, get_pb(username)); state = "PLAY"
        if menu.draw(screen) and any(e.type == pygame.MOUSEBUTTONDOWN for e in events): state = "MENU"
        retry.draw(screen); menu.draw(screen)
        font_big = pygame.font.SysFont("arial", 50, True)
        screen.blit(font_big.render("GAME OVER", True, RED), (280, 150))

    elif state == "LB": #
        data = get_top_10()
        for i, row in enumerate(data):
            txt = font.render(f"{i+1}. {row[0]} - {row[1]} pts (Lvl {row[2]})", True, WHITE)
            screen.blit(txt, (250, 100 + i*35))
        back = Button(400, 520, 150, 40, "BACK")
        if back.draw(screen) and any(e.type == pygame.MOUSEBUTTONDOWN for e in events): state = "MENU"
        back.draw(screen)

    elif state == "SET": #
        grid_txt = f"GRID: {'ON' if settings['grid'] else 'OFF'}"
        grid_btn = Button(400, 250, 250, 45, grid_txt)
        save_btn = Button(400, 450, 200, 45, "SAVE & BACK")
        if grid_btn.draw(screen) and any(e.type == pygame.MOUSEBUTTONDOWN for e in events): settings['grid'] = not settings['grid']
        if save_btn.draw(screen) and any(e.type == pygame.MOUSEBUTTONDOWN for e in events):
            with open("settings.json", "w") as f: json.dump(settings, f)
            state = "MENU"
        grid_btn.draw(screen); save_btn.draw(screen)

    pygame.display.flip()
    clock.tick(60)