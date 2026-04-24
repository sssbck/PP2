import pygame
import time
import random
import sys # Добавили sys для правильного закрытия игры

# размер окна
window_x = 720
window_y = 480

# определение цветов
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
gold = pygame.Color(255, 215, 0)

# инициализация
pygame.init()

# Инициализирование игрового окно
pygame.display.set_caption('Змейка')
game_window = pygame.display.set_mode((window_x, window_y))

# Контроллер FPS (кадры в секунду)
fps = pygame.time.Clock()

font = pygame.font.Font(None, 30)

# Глобальные переменные игры (объявляем их здесь, чтобы они были доступны везде)
snake_speed = 10.0
snake_position = []
snake_body = []
normal_fruit_pos = []
normal_fruit_active = True
big_fruit_pos = []
big_fruit_active = False
fruits_eaten_count = 0
direction = 'RIGHT'
change_to = 'RIGHT'
score = 0
level = 1

# НОВОЕ: Функция для сброса игры (начать заново)
def restart_game():
    global snake_speed, snake_position, snake_body, normal_fruit_pos
    global normal_fruit_active, big_fruit_pos, big_fruit_active
    global fruits_eaten_count, direction, change_to, score, level

    snake_speed = 10.0 
    snake_position = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]
    
    normal_fruit_pos = [random.randrange(1, (window_x // 10)) * 10,
                        random.randrange(1, (window_y // 10)) * 10]
    normal_fruit_active = True
    
    big_fruit_pos = [-100, -100] 
    big_fruit_active = False
    fruits_eaten_count = 0
    
    direction = 'RIGHT'
    change_to = direction
    score = 0
    level = 1

# НОВОЕ: Меню после проигрыша
def game_over_menu():
    my_font = pygame.font.SysFont('times new roman', 50)
    
    # Очищаем экран
    game_window.fill(black)
    
    # Текст проигрыша
    game_over_surface = my_font.render('Game Over! Score : ' + str(score), True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (window_x / 2, window_y / 4)
    game_window.blit(game_over_surface, game_over_rect)

    # Текст подсказок
    restart_text = font.render("Press 'R' to Restart", True, white)
    quit_text = font.render("Press 'Q' to Quit", True, white)
    
    # Размещаем подсказки на экране
    game_window.blit(restart_text, (window_x / 2 - 80, window_y / 2))
    game_window.blit(quit_text, (window_x / 2 - 70, window_y / 2 + 40))
    
    pygame.display.flip()
    
    # Цикл ожидания нажатия кнопки
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: # Нажали R - рестарт
                    restart_game()
                    waiting = False
                if event.key == pygame.K_q: # Нажали Q - выход
                    pygame.quit()
                    sys.exit()
        fps.tick(15)

# Отображение уровня
def show_level(font, surface, x, y):
    level_text = font.render('Level: ' + str(level), True, white)
    surface.blit(level_text, (x, y))

# Отображение счета
def show_score(font, surface, x, y):
    score_text = font.render('Score: ' + str(score), True, white)
    surface.blit(score_text, (x, y))

# Инициализируем переменные перед первым запуском
restart_game()

# Основной цикл игры
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'

    # Изменение направления движения змеи
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Перемещение змеи
    if direction == 'UP':
        snake_position[1] -= 10
    if direction == 'DOWN':
        snake_position[1] += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
    if direction == 'RIGHT':
        snake_position[0] += 10

    # Механизм роста тела змеи и поедания
    snake_body.insert(0, list(snake_position))
    ate_something = False

    # Проверка: съели ли обычный фрукт
    if snake_position[0] == normal_fruit_pos[0] and snake_position[1] == normal_fruit_pos[1]:
        score += 10
        fruits_eaten_count += 1
        snake_speed += 0.5  # Змея ускоряется
        normal_fruit_active = False
        ate_something = True
        
        # Спавн Большого Фрукта каждые 5 съеденных обычных
        if fruits_eaten_count % 5 == 0:
            big_fruit_active = True
            big_fruit_pos = [random.randrange(1, (window_x // 10)) * 10,
                             random.randrange(1, (window_y // 10)) * 10]

    # Проверка: съели ли БОЛЬШОЙ фрукт
    elif big_fruit_active and snake_position[0] == big_fruit_pos[0] and snake_position[1] == big_fruit_pos[1]:
        score += 50 
        big_fruit_active = False
        ate_something = True

    # Если ничего не съели, убираем хвост
    if not ate_something:
        snake_body.pop()

    # Переспавн обычного фрукта ТОЛЬКО когда его съели
    if not normal_fruit_active:
        normal_fruit_pos = [random.randrange(1, (window_x // 10)) * 10,
                            random.randrange(1, (window_y // 10)) * 10]
        normal_fruit_active = True

    # Увеличение уровня
    if score >= level * 30:
        level += 1

    # Флаг для отслеживания проигрыша в этом кадре
    is_game_over = False

    # Проверка условий завершения игры (выход за границы)
    if snake_position[0] < 0 or snake_position[0] > window_x - 10:
        is_game_over = True
    if snake_position[1] < 0 or snake_position[1] > window_y - 10:
        is_game_over = True
        
    # Проверка столкновения с собственным телом
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            is_game_over = True

    # Если проиграли, вызываем меню и пропускаем отрисовку этого кадра
    if is_game_over:
        game_over_menu()
        continue # Начинаем цикл заново уже с новыми значениями после рестарта

    # Обновление экрана
    game_window.fill(black)

    # Отображение змеи
    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

    # Отображение обычного фрукта
    if normal_fruit_active:
        pygame.draw.rect(game_window, red, pygame.Rect(normal_fruit_pos[0], normal_fruit_pos[1], 10, 10))

    # Отображение большого фрукта
    if big_fruit_active:
        pygame.draw.rect(game_window, gold, pygame.Rect(big_fruit_pos[0]-5, big_fruit_pos[1]-5, 20, 20))

    # Отображение уровня и счета
    show_level(font, game_window, 10, 10)
    show_score(font, game_window, window_x - 120, 10)

    # Обновление экрана
    pygame.display.update()

    # Frame Per Second / Контроль скорости змеи
    fps.tick(int(snake_speed))