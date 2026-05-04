import pygame
from persistence import load_leaderboard, save_settings

WHITE, BLACK, GRAY, BLUE, RED = (255, 255, 255), (0, 0, 0), (200, 200, 200), (50, 150, 255), (255, 50, 50)
CENTER_X = 200  # Центр для экрана шириной 400

def draw_text(surface, text, size, x, y, color=BLACK, center=True):
    font = pygame.font.SysFont("arial", size, bold=True)
    text_obj = font.render(text, True, color)
    rect = text_obj.get_rect(center=(x, y)) if center else text_obj.get_rect(topleft=(x, y))
    surface.blit(text_obj, rect)

class Button:
    def __init__(self, y, width, height, text, color=GRAY, hover_color=BLUE):
        self.rect = pygame.Rect(CENTER_X - width//2, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False

    def draw(self, surface):
        pygame.draw.rect(surface, self.hover_color if self.is_hovered else self.color, self.rect, border_radius=10)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=10)
        draw_text(surface, self.text, 24, self.rect.centerx, self.rect.centery, BLACK)

    def check_hover(self, mouse_pos): self.is_hovered = self.rect.collidepoint(mouse_pos)
    def is_clicked(self, event): return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered

def main_menu_screen(screen, settings):
    clock = pygame.time.Clock()
    buttons = [Button(200, 200, 45, "Play"), Button(260, 200, 45, "Leaderboard"), 
               Button(320, 200, 45, "Settings"), Button(380, 200, 45, "Quit", color=RED)]
    
    input_box = pygame.Rect(CENTER_X - 125, 120, 250, 35)
    active, text = False, settings.get("last_username", "Player")

    while True:
        screen.fill(WHITE)
        draw_text(screen, "RACER PRO", 40, CENTER_X, 40, BLUE)
        draw_text(screen, "Username:", 20, CENTER_X, 90, BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN: active = input_box.collidepoint(event.pos)
            if event.type == pygame.KEYDOWN and active:
                if event.key == pygame.K_RETURN: active = False
                elif event.key == pygame.K_BACKSPACE: text = text[:-1]
                elif len(text) < 12: text += event.unicode
                settings["last_username"] = text
                save_settings(settings)

            if buttons[0].is_clicked(event): return "play"
            if buttons[1].is_clicked(event): return "leaderboard"
            if buttons[2].is_clicked(event): return "settings"
            if buttons[3].is_clicked(event): return "quit"

        for btn in buttons:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        color = pygame.Color('dodgerblue2') if active else pygame.Color('lightskyblue3')
        txt_surf = pygame.font.SysFont("arial", 22).render(text, True, color)
        screen.blit(txt_surf, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, color, input_box, 2)
        pygame.display.flip()
        clock.tick(60)

def settings_screen(screen, settings):
    clock = pygame.time.Clock()
    colors, diffs = ["Red", "Blue", "Green", "Yellow"], ["Easy", "Normal", "Hard"]
    buttons = [Button(150, 200, 50, f"Sound: {'ON' if settings['sound'] else 'OFF'}"),
               Button(220, 200, 50, f"Car: {settings['car_color']}"),
               Button(290, 200, 50, f"Diff: {settings['difficulty']}"),
               Button(400, 200, 50, "Back", color=GRAY)]

    while True:
        screen.fill(WHITE)
        draw_text(screen, "SETTINGS", 40, CENTER_X, 50, BLUE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: return "quit"
            if buttons[0].is_clicked(event):
                settings["sound"] = not settings["sound"]
                buttons[0].text = f"Sound: {'ON' if settings['sound'] else 'OFF'}"
                save_settings(settings)
            if buttons[1].is_clicked(event):
                settings["car_color"] = colors[(colors.index(settings["car_color"]) + 1) % len(colors)]
                buttons[1].text = f"Car: {settings['car_color']}"
                save_settings(settings)
            if buttons[2].is_clicked(event):
                settings["difficulty"] = diffs[(diffs.index(settings["difficulty"]) + 1) % len(diffs)]
                buttons[2].text = f"Diff: {settings['difficulty']}"
                save_settings(settings)
            if buttons[3].is_clicked(event): return "menu"

        for btn in buttons:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)
        pygame.display.flip()
        clock.tick(60)

def leaderboard_screen(screen):
    clock = pygame.time.Clock()
    back_btn = Button(500, 200, 50, "Back", color=GRAY)
    board = load_leaderboard()

    while True:
        screen.fill(WHITE)
        draw_text(screen, "TOP 10 SCORES", 30, CENTER_X, 40, BLUE)
        draw_text(screen, "Rank    Name        Score    Dist", 16, 20, 100, center=False)
        pygame.draw.line(screen, BLACK, (20, 125), (380, 125), 2)
        
        for i, entry in enumerate(board):
            draw_text(screen, f"{i+1:2d}.   {entry['name'][:10]:<10}   {entry['score']:<5}   {entry['distance']}m", 16, 20, 140 + i*30, center=False)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: return "quit"
            if back_btn.is_clicked(event): return "menu"

        back_btn.check_hover(pygame.mouse.get_pos())
        back_btn.draw(screen)
        pygame.display.flip()
        clock.tick(60)

def game_over_screen(screen, score, distance, coins):
    clock, buttons = pygame.time.Clock(), [Button(350, 200, 50, "Retry", color=BLUE), Button(420, 200, 50, "Main Menu", color=GRAY)]
    while True:
        screen.fill(WHITE)
        draw_text(screen, "GAME OVER", 40, CENTER_X, 100, RED)
        draw_text(screen, f"Score: {score} | Dist: {distance}m | Coins: {coins}", 20, CENTER_X, 180)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: return "quit"
            if buttons[0].is_clicked(event): return "play"
            if buttons[1].is_clicked(event): return "menu"

        for btn in buttons:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)
        pygame.display.flip()
        clock.tick(60)