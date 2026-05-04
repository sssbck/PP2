# game.py
import pygame, random
from config import *

class SnakeGame:
    def __init__(self, username, settings, pb):
        self.username, self.pb = username, pb
        self.snake = [(WIDTH//2, HEIGHT//2)]
        self.dx, self.dy = BLOCK_SIZE, 0
        self.score, self.level = 0, 1
        self.game_over = False
        self.base_speed = 10
        self.current_speed = 10
        self.foods = []
        self.obstacles = []
        self.powerup = None
        self.shield_active = False
        self.pu_timer = 0
        self.settings = settings
        self.generate_obstacles()
        self.spawn_food()

    def generate_obstacles(self):
        self.obstacles = []
        if self.level >= 3:
            for _ in range(self.level * 3):
                while True:
                    obs = (random.randrange(0, WIDTH, BLOCK_SIZE), random.randrange(0, HEIGHT, BLOCK_SIZE))
                    # Проверка: не спавнить на змейке и не блокировать голову (оставляем 3х3 клетки вокруг головы пустыми)
                    dist_x = abs(obs[0] - self.snake[0][0])
                    dist_y = abs(obs[1] - self.snake[0][1])
                    if obs not in self.snake and (dist_x > BLOCK_SIZE * 2 or dist_y > BLOCK_SIZE * 2):
                        self.obstacles.append(obs); break

    def spawn_food(self):
        while len(self.foods) < 3:
            pos = (random.randrange(0, WIDTH, BLOCK_SIZE), random.randrange(0, HEIGHT, BLOCK_SIZE))
            if pos not in self.snake and pos not in self.obstacles:
                f_type = random.choices(['NORMAL', 'BONUS', 'POISON'], weights=[60, 25, 15])[0]
                timer = pygame.time.get_ticks() + 7000 if f_type == 'BONUS' else None
                self.foods.append({'pos': pos, 'type': f_type, 'timer': timer})

    def spawn_powerup(self):
        if not self.powerup:
            pos = (random.randrange(0, WIDTH, BLOCK_SIZE), random.randrange(0, HEIGHT, BLOCK_SIZE))
            if pos not in self.snake and pos not in self.obstacles:
                p_type = random.choice(['SPEED', 'SLOW', 'SHIELD'])
                self.powerup = {'pos': pos, 'type': p_type, 'expires': pygame.time.get_ticks() + 8000}

    def update(self):
        now = pygame.time.get_ticks()
        # Проверка истечения бонусов
        if self.pu_timer and now > self.pu_timer:
            self.current_speed = self.base_speed
            self.pu_timer = 0
        if self.powerup and now > self.powerup['expires']: self.powerup = None

        # Движение
        head = (self.snake[0][0] + self.dx, self.snake[0][1] + self.dy)
        
        # Столкновения
        if head[0]<0 or head[0]>=WIDTH or head[1]<0 or head[1]>=HEIGHT or head in self.snake or head in self.obstacles:
            if self.shield_active: self.shield_active = False
            else: self.game_over = True; return

        self.snake.insert(0, head)
        
        # Логика поедания
        ate = False
        for f in self.foods[:]:
            if head == f['pos']:
                ate = True; self.foods.remove(f)
                if f['type'] == 'POISON': #
                    self.snake = self.snake[:-2]
                    if len(self.snake) <= 1: self.game_over = True
                else:
                    self.score += 25 if f['type'] == 'BONUS' else 10
                break
        
        if self.powerup and head == self.powerup['pos']: #
            p_type = self.powerup['type']
            if p_type == 'SPEED': self.current_speed += 5; self.pu_timer = now + 5000
            elif p_type == 'SLOW': self.current_speed = max(5, self.current_speed - 5); self.pu_timer = now + 5000
            elif p_type == 'SHIELD': self.shield_active = True
            self.powerup = None

        if not ate: self.snake.pop()
        
        # Левел-ап
        if self.score // 50 >= self.level:
            self.level += 1; self.base_speed += 1; self.current_speed = self.base_speed
            self.generate_obstacles()
        
        self.spawn_food()
        if random.random() < 0.01: self.spawn_powerup()

    def draw(self, screen):
        if self.settings['grid']:
            for x in range(0, WIDTH, BLOCK_SIZE): pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
        for obs in self.obstacles: pygame.draw.rect(screen, (100,100,100), (*obs, BLOCK_SIZE, BLOCK_SIZE))
        for f in self.foods: pygame.draw.rect(screen, FOOD_COLORS[f['type']], (*f['pos'], BLOCK_SIZE-2, BLOCK_SIZE-2))
        if self.powerup: pygame.draw.circle(screen, PU_COLORS[self.powerup['type']], (self.powerup['pos'][0]+10, self.powerup['pos'][1]+10), 8)
        for i, s in enumerate(self.snake):
            color = self.settings.get('color', (0, 255, 0)) if i > 0 else WHITE
            if self.shield_active and i % 2 == 0: color = BLUE
            pygame.draw.rect(screen, color, (*s, BLOCK_SIZE-2, BLOCK_SIZE-2))