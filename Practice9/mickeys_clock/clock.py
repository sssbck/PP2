import pygame
import datetime
from datetime import timedelta, timezone
import sys

class ClockLogic:
    def __init__(self):
        # --- Настройки окна ---
        self.WIDTH = 800
        self.HEIGHT = 800
        self.FPS = 60
        
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Mickey Mouse Clock")
        self.clock = pygame.time.Clock() 
        
        # --- Загрузка и подготовка графики ---
        try:
            # Фон
            self.bg = pygame.image.load("images/mickey_bg.png").convert_alpha()
            self.bg = pygame.transform.scale(self.bg, (self.WIDTH, self.HEIGHT))
            
            # Стрелки (загружаются в оригинальном размере)
            self.min_hand_img = pygame.image.load("images/mickey_r.PNG").convert_alpha()
            self.sec_hand_img = pygame.image.load("images/mickey_l.PNG").convert_alpha()
            
            # НОВАЯ СТРЕЛКА: Часовая (убедись, что файл существует!)
            self.hour_hand_img = pygame.image.load("images/mickey_h.PNG").convert_alpha()
            
        except FileNotFoundError as e:
            print(f"ОШИБКА ЗАГРУЗКИ: {e}")
            print("Убедись, что у тебя есть файлы mickey_r.PNG, mickey_l.PNG и mickey_h.PNG в папке images!")
            pygame.quit()
            sys.exit()

        # --- Настройки часовых поясов ---
        self.TIME_ZONES = {
            "Almaty (UTC+5)": 5,
            "London (UTC+0)": 0,
            "New York (UTC-5)": -5,
            "Tokyo (UTC+9)": 9
        }
        self.zone_names = list(self.TIME_ZONES.keys())
        self.zone_index = 0
        self.current_offset = self.TIME_ZONES[self.zone_names[self.zone_index]]

    def get_rotated_image(self, image, angle, offset_x, offset_y):
        """
        Вращает картинку вокруг смещенного центра (пивота).
        """
        rotated_image = pygame.transform.rotate(image, angle)
        offset = pygame.math.Vector2(offset_x, offset_y).rotate(-angle)
        rect = rotated_image.get_rect(center=(self.WIDTH // 2 - offset.x, self.HEIGHT // 2 - offset.y))
        return rotated_image, rect

    def run(self):
        """Основной цикл приложения"""
        running = True
        while running:
            # --- 1. Логика времени ---
            utc_now = datetime.datetime.now(timezone.utc)
            current_time = utc_now + timedelta(hours=self.current_offset)
            
            hours = current_time.hour % 12  # Переводим в 12-часовой формат
            minutes = current_time.minute
            seconds = current_time.second
            
            # Углы для стрелок (отрицательные для вращения по часовой)
            sec_angle = -seconds * 6
            min_angle = -minutes * 6 - (seconds / 10)
            # Часовая стрелка сдвигается на 30 градусов за час + 0.5 градуса за каждую минуту для плавности
            hour_angle = -(hours * 30 + minutes * 0.5)

            # --- 2. Обработка событий ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.zone_index = (self.zone_index + 1) % len(self.zone_names)
                        self.current_offset = self.TIME_ZONES[self.zone_names[self.zone_index]]
                    if event.key == pygame.K_LEFT:
                        self.zone_index = (self.zone_index - 1) % len(self.zone_names)
                        self.current_offset = self.TIME_ZONES[self.zone_names[self.zone_index]]

            # --- 3. Отрисовка кадра ---
            self.screen.fill((150, 150, 150))
            self.screen.blit(self.bg, (0, 0))
            
            # УМНАЯ КАЛИБРОВКА 70/30 ДЛЯ ВСЕХ ТРЕХ СТРЕЛОК
            min_h = self.min_hand_img.get_height()
            sec_h = self.sec_hand_img.get_height()
            hour_h = self.hour_hand_img.get_height()
            
            # Смещаем центр на 20% вниз (0.2)
            min_pivot_y = min_h * 0.4 
            sec_pivot_y = sec_h * 0.35  
            hour_pivot_y = hour_h * 0.4
            
            rot_hour, rect_hour = self.get_rotated_image(self.hour_hand_img, hour_angle, 0, hour_pivot_y)
            rot_min, rect_min = self.get_rotated_image(self.min_hand_img, min_angle, 0, min_pivot_y)
            rot_sec, rect_sec = self.get_rotated_image(self.sec_hand_img, sec_angle, 0, sec_pivot_y)
            
            # Рисуем послойно: сначала часы (внизу), потом минуты, потом секунды (на самом верху)
            self.screen.blit(rot_hour, rect_hour)
            self.screen.blit(rot_min, rect_min)
            self.screen.blit(rot_sec, rect_sec)

            # Текст с городом
            font = pygame.font.SysFont("Arial", 24, bold=True)
            info_text = font.render(f"Zone: {self.zone_names[self.zone_index]}", True, (0, 0, 0))
            self.screen.blit(info_text, (10, 10))

            pygame.display.flip()
            self.clock.tick(self.FPS)

        pygame.quit()