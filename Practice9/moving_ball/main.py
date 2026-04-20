import pygame
import sys
from ball import BallGame, MazeGame

def main():
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mega Game Hub")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 30, bold=True)

    mode = "MENU" # MENU, GAME1, GAME2, GAMEOVER
    game = None
    last_game_type = "" # Чтобы знать, что перезапускать

    while True:
        screen.fill((20, 20, 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if mode == "MENU":
                    if event.key == pygame.K_a:
                        game = BallGame(WIDTH, HEIGHT)
                        mode, last_game_type = "GAME1", "A"
                    elif event.key == pygame.K_s:
                        game = MazeGame(WIDTH, HEIGHT)
                        mode, last_game_type = "GAME2", "S"
                
                elif mode == "GAMEOVER":
                    if event.key == pygame.K_1: # Начать заново
                        if last_game_type == "A": game = BallGame(WIDTH, HEIGHT)
                        else: game = MazeGame(WIDTH, HEIGHT)
                        mode = "GAME1" if last_game_type == "A" else "GAME2"
                    elif event.key == pygame.K_2: # Сменить режим
                        mode = "MENU"
                    elif event.key == pygame.K_3: # Выход
                        pygame.quit()
                        sys.exit()

        if mode == "MENU":
            screen.blit(font.render("ГЛАВНОЕ МЕНЮ", True, (255, 255, 0)), (300, 150))
            screen.blit(font.render("A - Режим Охота (Границы = смерть)", True, (255, 255, 255)), (180, 250))
            screen.blit(font.render("S - Режим Лабиринт (5 карт)", True, (255, 255, 255)), (180, 310))

        elif mode == "GAMEOVER":
            screen.blit(font.render("ИГРА ОКОНЧЕНА!", True, (255, 50, 50)), (280, 150))
            screen.blit(font.render("1. Начать заново", True, (255, 255, 255)), (280, 250))
            screen.blit(font.render("2. Главное меню (Сменить режим)", True, (255, 255, 255)), (280, 300))
            screen.blit(font.render("3. Выйти из игры", True, (255, 255, 255)), (280, 350))

        elif mode in ["GAME1", "GAME2"]:
            keys = pygame.key.get_pressed()
            status = game.update(keys)
            
            if status == "LOST":
                mode = "GAMEOVER"
            elif status == "WIN":
                # Можно добавить экран победы, но пока отправим в меню
                mode = "MENU"
            
            game.draw(screen)
            info = font.render(f"Level: {game.level}", True, (255, 255, 255))
            screen.blit(info, (10, 10))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()