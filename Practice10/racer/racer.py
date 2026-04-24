#Imports
import pygame, sys
from pygame.locals import *
import random, time

#Initialzing 
pygame.init()

#Setting up FPS 
FPS = 60
FramePerSec = pygame.time.Clock()

#Creating colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#Other Variables for use in the program
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 1
COINSPEED = 3
SCORE = 0
COINS = 0
LEVEL = 1

#Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Загрузка звуков и фона (обернуто в try/except на случай отсутствия файлов)
try:
    background = pygame.image.load("AnimatedStreet.png")
except:
    background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    background.fill(WHITE)

#Create a white screen 
DISPLAYSURF = pygame.display.set_mode((400,600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

# creating an enemy class
class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__() 
        try:
            self.image = pygame.image.load("Enemy.png")
        except:
            self.image = pygame.Surface((40, 60))
            self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40,SCREEN_WIDTH-40), 0)

      def move(self):
        global SCORE
        self.rect.move_ip(0,1 * SPEED)
        if (self.rect.bottom > 800): 
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
"""Здесь определяется класс Enemy, который представляет противников в игре. 
В конструкторе класса загружается изображение противника, 
устанавливается его положение искомого по вертикали в верхней части экрана
 и случайным образом по горизонтали. 
 Метод move() отвечает за движение противника вниз по экрану. 
 Если противник достигает нижнего края экрана, его положение сбрасывается в верхнюю часть экрана."""

# creating a player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        try:
            self.image = pygame.image.load("Player.png")
        except:
            self.image = pygame.Surface((40, 60))
            self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
       
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        
        # Движение влево и вправо
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-10, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(10, 0)
        
        # НОВОЕ: Движение вверх и вниз
        if self.rect.top > 0:
              if pressed_keys[K_UP]:
                  self.rect.move_ip(0, -10)
        if self.rect.bottom < SCREEN_HEIGHT:
              if pressed_keys[K_DOWN]:
                  self.rect.move_ip(0, 10)
        
"""Zдесь определяется класс Player, представляющий игрока. В конструкторе класса загружается изображение игрока,
 устанавливается его положение в центре нижней части экрана. 
Метод move() обрабатывает движение игрока во всех направлениях при нажатии клавиш со стрелками."""

# creating a coin class
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.randomCoin = random.randint(1, 3)
        try:
            self.image = pygame.image.load(f"coin{self.randomCoin}.png")
            self.image = pygame.transform.scale(self.image, (30, 30))
        except:
            self.image = pygame.Surface((30, 30))
            self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40,SCREEN_WIDTH-40), 0)
        """Здесь определяется класс Coin, представляющий монеты в игре. 
В конструкторе класса случайным образом выбирается одно изображение монеты,
 загружается изображение монеты, изменяется его размер,
   устанавливается положение монеты в случайном месте в верхней части экрана."""
    def move(self):
        global COINS
        self.rect.move_ip(0,2 * COINSPEED)
        if (self.rect.bottom > 600): # if our coin will go under the screen it will be respawned
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


# НОВОЕ: Функция для сброса состояния игры при рестарте
def restart_game():
    global SCORE, COINS, LEVEL, SPEED, P1, E1, COIN, enemies, coins, all_sprites
    SCORE = 0
    COINS = 0
    LEVEL = 1
    SPEED = 1

    # Пересоздаем спрайты
    P1 = Player()
    E1 = Enemy()
    COIN = Coin()

    enemies = pygame.sprite.Group()
    enemies.add(E1)
    
    coins = pygame.sprite.Group()
    coins.add(COIN)
    
    all_sprites = pygame.sprite.Group()
    all_sprites.add(P1)
    all_sprites.add(E1)
    all_sprites.add(COIN)

# НОВОЕ: Функция меню проигрыша
def game_over_menu():
    DISPLAYSURF.fill(RED)
    DISPLAYSURF.blit(game_over, (30, 200))
    
    # Текст подсказок
    restart_text = font_small.render("Press 'R' to Restart", True, WHITE)
    quit_text = font_small.render("Press 'Q' to Quit", True, WHITE)
    
    DISPLAYSURF.blit(restart_text, (100, 300))
    DISPLAYSURF.blit(quit_text, (100, 350))
    
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_r: # Рестарт игры
                    restart_game()
                    waiting = False
                if event.key == K_q: # Выход из игры
                    pygame.quit()
                    sys.exit()
        FramePerSec.tick(FPS)

#Setting up Sprites        
P1 = Player()
E1 = Enemy()
COIN = Coin()
coin_dup = 0
#Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()
coins.add(COIN)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(COIN)

def levelAdder():
    global LEVEL
    global SPEED
    if COINS // 4 > LEVEL:
        LEVEL += 1
        SPEED += 3

#Game Loop
while True:
      
    #Cycles through all events occuring  
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    try:
        DISPLAYSURF.blit(background, (0,0))
    except:
        DISPLAYSURF.fill(WHITE)
        
    scores = font_small.render("Score: " + str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10,10))
    collected = font_small.render("Coins: " + str(COINS), True, BLACK)
    DISPLAYSURF.blit(collected, (400 - 120,10))
    levels = font_small.render("Level: " + str(LEVEL), True, BLACK)
    DISPLAYSURF.blit(levels, (400 - 120, 40))
    #Этот блок кода отображает фон игры и текущий счет (SCORE), 
    #количество собранных монет (COINS) и текущий уровень (LEVEL) на экране.
    

    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)
    #Этот блок кода обновляет и перерисовывает все спрайты на экране. Каждый спрайт перемещается 
    #в соответствии с его логикой движения, а затем отображается на экране.
        

    #To be run if collision occurs between Player and Enemy
    if pygame.sprite.spritecollideany(P1, enemies):
          try:
              pygame.mixer.Sound('crash.wav').play()
          except:
              pass # Игнорируем, если звука нет
          time.sleep(0.5) # Небольшая пауза для эффекта
          
          # Вызов функции меню окончания игры
          game_over_menu()

   #Если происходит столкновение между игроком (P1) и врагом (enemies), то игра завершается.
   #Игроку выводится сообщение о проигрыше, затем игра закрывается.

    if pygame.sprite.spritecollideany(P1, coins):
            try:
                pygame.mixer.Sound('collect.wav').play()
            except:
                pass
            for coin in coins:
                coin.kill()
            if COIN.randomCoin == 1:
                COINS += 1
            if COIN.randomCoin == 2:
                COINS += 2
            if COIN.randomCoin == 3:
                COINS += 3
            COIN = Coin()
            coins.add(COIN)
            all_sprites.add(COIN)
            
            #Если игрок сталкивается с монетой, то монета удаляется, игрок получает определенное количество очков 
            #(зависит от типа монеты), и количество собранных монет увеличивается.


    if(len(coins) == 0): # if our coin was collected:
        COIN = Coin()   
        coins.add(COIN)
        all_sprites.add(COIN)
        #Если все монеты были собраны, создается новая монета 
        #и добавляется в группу монет и в общую группу спрайтов.

    levelAdder()

    pygame.display.update()
    FramePerSec.tick(FPS)