# config.py
params = {
    "host": "127.0.0.1",
    "database": "snake_db",
    "user": "postgres",
    "password": "123"  # Установи свой актуальный пароль
}

WIDTH, HEIGHT = 800, 600
BLOCK_SIZE = 20

# Цвета
WHITE, BLACK = (255, 255, 255), (0, 0, 0)
GRAY, LIGHT_GRAY = (50, 50, 50), (200, 200, 200)
GREEN, RED, YELLOW, BLUE = (0, 255, 0), (255, 0, 0), (255, 255, 0), (0, 0, 255)

FOOD_COLORS = {'NORMAL': (255, 100, 100), 'BONUS': YELLOW, 'POISON': (139, 0, 0)}
PU_COLORS = {'SPEED': (0, 255, 255), 'SLOW': (255, 165, 0), 'SHIELD': (255, 0, 255)}