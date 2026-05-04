import pygame
import random
import time
import os

SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600
LANES = [70, 200, 330] # 3 полосы для ширины дороги 400px

ASSETS = {}

def init_assets():
    """Загрузка картинок из папки assets. Вызывается один раз перед игрой."""
    def load(name, size):
        # Предполагаем формат .png, если расширение не указано в папке
        path = os.path.join("assets", name + ".png") 
        try:
            return pygame.transform.scale(pygame.image.load(path).convert_alpha(), size)
        except:
            surf = pygame.Surface(size, pygame.SRCALPHA)
            surf.fill((255, 0, 255)) # Заглушка, если файл не найден
            return surf

    ASSETS['bg'] = load("AnimatedStreet", (SCREEN_WIDTH, SCREEN_HEIGHT))
    ASSETS['Enemy'] = load("Enemy", (45, 90))
    ASSETS['Player_Red'] = load("Player_red", (45, 90))
    ASSETS['Player_Blue'] = load("Player_blue", (45, 90))
    ASSETS['Player_Green'] = load("Player_green", (45, 90))
    ASSETS['Player_Yellow'] = load("Player_yellow", (45, 90))
    
    ASSETS['coin1'] = load("coin1", (30, 30))
    ASSETS['coin2'] = load("coin2", (30, 30))
    ASSETS['coin3'] = load("coin3", (30, 30))
    
    ASSETS['nitro'] = load("nitro", (40, 40))
    ASSETS['shield'] = load("shield", (40, 40))
    ASSETS['repair'] = load("repair", (40, 40))

class Entity:
    def __init__(self, image, x, y):
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Player(Entity):
    def __init__(self, color_name):
        super().__init__(ASSETS.get(f'Player_{color_name}', ASSETS['Player_Red']), LANES[1], SCREEN_HEIGHT - 80)
        self.lane = 1
        self.shield_active, self.nitro_active = False, False
        self.powerup_end = 0

    def update(self):
        target_x = LANES[self.lane]
        if self.rect.centerx < target_x: self.rect.centerx += min(15, target_x - self.rect.centerx)
        elif self.rect.centerx > target_x: self.rect.centerx -= min(15, self.rect.centerx - target_x)
        
        if time.time() > self.powerup_end:
            self.shield_active, self.nitro_active = False, False

    def draw(self, surface):
        super().draw(surface)
        if self.shield_active: pygame.draw.circle(surface, (0, 255, 255), self.rect.center, 55, 3)

class Enemy(Entity):
    def __init__(self, speed):
        super().__init__(ASSETS['Enemy'], random.choice(LANES), -50)
        # Враг просто появляется и "стоит" на месте (налетает на тебя со скоростью трассы)
        self.speed = speed

    def update(self): 
        self.rect.y += self.speed

    def update(self): 
        self.rect.y += self.speed

class Coin(Entity):
    def __init__(self, speed):
        # Логика взвешенных монет с разными картинками
        val = random.random()
        if val > 0.9: img, self.value = ASSETS['coin3'], 5
        elif val > 0.6: img, self.value = ASSETS['coin2'], 3
        else: img, self.value = ASSETS['coin1'], 1
        super().__init__(img, random.choice(LANES), -30)
        self.speed = speed
    def update(self): self.rect.y += self.speed

class PowerUp(Entity):
    def __init__(self, speed):
        self.type = random.choice(["nitro", "shield", "repair"])
        super().__init__(ASSETS[self.type], random.choice(LANES), -30)
        self.speed = speed
    def update(self): self.rect.y += self.speed

class Hazard(Entity):
    def __init__(self, speed):
        self.type = random.choice(["oil", "barrier"])
        # Так как ассетов препятствий на скрине нет, рисуем их как поверхности
        surf = pygame.Surface((60, 20) if self.type == "barrier" else (50, 50), pygame.SRCALPHA)
        if self.type == "barrier": surf.fill((255, 140, 0))
        else: pygame.draw.circle(surf, (30, 30, 30), (25, 25), 25)
        super().__init__(surf, random.choice(LANES), -50)
        self.speed = speed
    def update(self): self.rect.y += self.speed


def run_game(screen, settings):
    clock = pygame.time.Clock()
    init_assets() # Загружаем картинки перед стартом

    base_speed = {"Easy": 3, "Normal": 5, "Hard": 8}.get(settings["difficulty"], 5)
    current_speed = base_speed
    
    player = Player(settings["car_color"])
    enemies, coins, hazards, powerups = [], [], [], []
    score, distance, coin_count, bg_y = 0, 0, 0, 0
    timer = 0
    
    running = True
    while running:
        clock.tick(60)
        timer += 1
        actual_speed = current_speed * 1.5 if player.nitro_active else current_speed
        distance += actual_speed / 100.0
        
        if distance > 50 and base_speed < 12: current_speed = base_speed + (int(distance) // 50)

        

        for event in pygame.event.get():
            if event.type == pygame.QUIT: return "quit", score, distance, coin_count
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and player.lane > 0: player.lane -= 1
                if event.key == pygame.K_RIGHT and player.lane < 2: player.lane += 1

        # Спавн        
        # 1. Враги (Увеличили количество на Easy, чтобы было кого обгонять)
        # На Easy машина появится примерно каждые 150 кадров, на Hard - каждые 70.
        enemy_rate = max(30, int(400 / current_speed) + 20)
        if timer % enemy_rate == 0:
            enemies.append(Enemy(actual_speed))

        # 2. Препятствия (Уменьшили духоту на Hard)
        # Теперь минимальный порог - 80 кадров (раньше было 40). У тебя всегда будет окно для перестроения!
        hazard_rate = max(80, int(1000 / current_speed))
        if timer % hazard_rate == 0:
            hazards.append(Hazard(actual_speed))

        # 3. Монеты (Стабильный поток)
        coin_rate = max(30, int(600 / current_speed))
        if timer % coin_rate == 0:
            coins.append(Coin(actual_speed))

        # 4. Поверапы
        if timer % 500 == 0:
            powerups.append(PowerUp(actual_speed))

        # Обновление и коллизии
        player.update()
        for lst in (enemies, hazards, coins, powerups):
            for item in lst[:]:
                item.update()
                if item.rect.y > SCREEN_HEIGHT: lst.remove(item)
        #  Враги застревают на всех препятствиях ---
        for e in enemies:
            for h in hazards:
                if e.rect.colliderect(h.rect):
                    # Враг теряет свою скорость и начинает ехать со скоростью дороги (останавливается)
                    e.speed = actual_speed
                    
                    # Если это физический барьер, упираемся в него бампером, чтобы не "проехать" внутрь текстуры
                    if h.type == "barrier":
                        e.rect.bottom = h.rect.top

        for e in enemies[:]:
            if e.rect.colliderect(player.rect):
                if player.shield_active: player.shield_active = False; enemies.remove(e)
                else: return "game_over", int(score + distance), int(distance), coin_count
        
        for h in hazards[:]:
            if h.rect.colliderect(player.rect):
                if h.type == "barrier":
                    if player.shield_active: player.shield_active = False; hazards.remove(h)
                    else: return "game_over", int(score + distance), int(distance), coin_count
                elif h.type == "oil":
                    player.lane = random.choice([0, 1, 2])
                    hazards.remove(h)

        for c in coins[:]:
            if c.rect.colliderect(player.rect):
                score += c.value * 10
                coin_count += c.value
                current_speed += 0.05 # Ускорение от монет
                coins.remove(c)

        for p in powerups[:]:
            if p.rect.colliderect(player.rect):
                if p.type == "nitro": player.nitro_active, player.powerup_end = True, time.time() + 4
                elif p.type == "shield": player.shield_active, player.powerup_end = True, time.time() + 10
                elif p.type == "repair": enemies.clear(); hazards.clear()
                powerups.remove(p)

        # Отрисовка скроллящегося фона AnimatedStreet
        bg_y = (bg_y + actual_speed) % SCREEN_HEIGHT
        screen.blit(ASSETS['bg'], (0, bg_y))
        screen.blit(ASSETS['bg'], (0, bg_y - SCREEN_HEIGHT))
        
        for item in hazards + coins + powerups + enemies: item.draw(screen)
        player.draw(screen)
        
        # --- Отрисовка HUD и Текста ---
        font = pygame.font.SysFont("arial", 20, bold=True)
        
        # Основная статистика (Счет, Дистанция, Монеты)
        # Рисуем черную подложку для читаемости
        pygame.draw.rect(screen, (0, 0, 0, 150), (5, 5, 120, 70), border_radius=5)
        screen.blit(font.render(f"Score: {int(score + distance)}", True, (255,255,255)), (10, 10))
        screen.blit(font.render(f"Dist: {int(distance)}m", True, (255,255,255)), (10, 30))
        screen.blit(font.render(f"Coins: {coin_count}", True, (255,215,0)), (10, 50))

        # --- ИНДИКАТОРЫ POWER-UP (Progress Bars) ---
        current_time = time.time()
        
        # 1. Индикатор НИТРО (Оранжевый)
        if player.nitro_active:
            time_left = player.powerup_end - current_time
            if time_left > 0:
                # Максимальное время нитро - 4 секунды. Высчитываем процент.
                bar_width = int((time_left / 4.0) * 150)
                
                screen.blit(font.render("NITRO", True, (255, 140, 0)), (SCREEN_WIDTH - 160, 10))
                # Фоновая полоска (серая)
                pygame.draw.rect(screen, (100, 100, 100), (SCREEN_WIDTH - 160, 35, 150, 10))
                # Заполненная полоска (оранжевая), которая уменьшается
                pygame.draw.rect(screen, (255, 140, 0), (SCREEN_WIDTH - 160, 35, max(0, bar_width), 10))
            else:
                player.nitro_active = False

        # 2. Индикатор ЩИТА (Голубой)
        if player.shield_active:
            time_left = player.powerup_end - current_time
            if time_left > 0:
                # Максимальное время щита - 10 секунд.
                bar_width = int((time_left / 10.0) * 150)
                
                # Сдвигаем вниз, если нитро тоже активно, чтобы полоски не накладывались
                y_offset = 60 if player.nitro_active else 10
                
                screen.blit(font.render("SHIELD", True, (0, 255, 255)), (SCREEN_WIDTH - 160, y_offset))
                pygame.draw.rect(screen, (100, 100, 100), (SCREEN_WIDTH - 160, y_offset + 25, 150, 10))
                pygame.draw.rect(screen, (0, 255, 255), (SCREEN_WIDTH - 160, y_offset + 25, max(0, bar_width), 10))
            else:
                player.shield_active = False

        pygame.display.flip()