import pygame
import random

class BallGame:
    """Игра 1: Охота (Проигрыш при касании границ)"""
    def __init__(self, width, height):
        self.WIDTH, self.HEIGHT = width, height
        self.radius = 20
        self.reset()

    def reset(self):
        self.x, self.y = self.WIDTH // 2, self.HEIGHT // 2
        self.speed = 8
        self.level = 1
        self.spawn_target()

    def spawn_target(self):
        self.target = pygame.Rect(random.randint(50, 750), random.randint(50, 550), 30, 30)

    def update(self, keys):
        if keys[pygame.K_UP]: self.y -= self.speed
        if keys[pygame.K_DOWN]: self.y += self.speed
        if keys[pygame.K_LEFT]: self.x -= self.speed
        if keys[pygame.K_RIGHT]: self.x += self.speed
        
        # Проверка проигрыша (касание границ)
        if (self.x - self.radius < 0 or self.x + self.radius > self.WIDTH or 
            self.y - self.radius < 0 or self.y + self.radius > self.HEIGHT):
            return "LOST"

        # Проверка касания цели
        ball_rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius*2, self.radius*2)
        if ball_rect.colliderect(self.target):
            self.level += 1
            self.speed += 1
            self.spawn_target()
        return "ALIVE"

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 215, 0), self.target)
        pygame.draw.circle(screen, (0, 255, 100), (self.x, self.y), self.radius)

class MazeGame:
    """Игра 2: Лабиринт (5 уровней)"""
    def __init__(self, width, height):
        self.WIDTH, self.HEIGHT = width, height
        self.radius = 12
        self.level = 1
        self.max_levels = 5
        self.finish = pygame.Rect(720, 520, 40, 40)
        self.load_level()

    def load_level(self):
        self.x, self.y = 40, 40
        self.speed = 4 + self.level
        # Наборы стен для 5 уровней
        levels_walls = [
            [pygame.Rect(200, 0, 30, 400), pygame.Rect(500, 200, 30, 400)], # Уровень 1
            [pygame.Rect(150, 150, 500, 30), pygame.Rect(150, 400, 500, 30)], # Уровень 2
            [pygame.Rect(0, 200, 600, 30), pygame.Rect(200, 400, 600, 30)], # Уровень 3
            [pygame.Rect(200, 0, 30, 300), pygame.Rect(400, 300, 30, 300), pygame.Rect(600, 0, 30, 300)], # Уровень 4
            [pygame.Rect(100, 100, 30, 400), pygame.Rect(100, 100, 600, 30), pygame.Rect(670, 100, 30, 400)] # Уровень 5
        ]
        self.walls = levels_walls[min(self.level - 1, 4)]

    def update(self, keys):
        if keys[pygame.K_UP]: self.y -= self.speed
        if keys[pygame.K_DOWN]: self.y += self.speed
        if keys[pygame.K_LEFT]: self.x -= self.speed
        if keys[pygame.K_RIGHT]: self.x += self.speed

        player_rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius*2, self.radius*2)
        
        # Столкновение со стеной или границей - ПРОИГРЫШ
        if self.x < 0 or self.x > self.WIDTH or self.y < 0 or self.y > self.HEIGHT:
            return "LOST"
        for wall in self.walls:
            if player_rect.colliderect(wall):
                return "LOST"

        # Финиш
        if player_rect.colliderect(self.finish):
            if self.level >= self.max_levels:
                return "WIN"
            self.level += 1
            self.load_level()
        
        return "ALIVE"

    def draw(self, screen):
        for wall in self.walls:
            pygame.draw.rect(screen, (255, 50, 50), wall)
        pygame.draw.rect(screen, (0, 255, 0), self.finish)
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), self.radius)