import pygame

pygame.init() 

painting = []
timer = pygame.time.Clock()
fps = 60 
activeColor = (0, 0, 0)
activeShape = 0
activeSize = 15 
w = 800 
h = 600 

screen = pygame.display.set_mode([w, h]) # Set Screen
pygame.display.set_caption("Paint") # Set Window Title

def drawDisplay():
    pygame.draw.rect(screen, (229,255,204), [0, 0, w, 86]) #Display
    pygame.draw.line(screen, 'gray', [0, 85], [w, 85]) #Line separator
    
    rect = [pygame.draw.rect(screen, (96, 96, 96), [10, 10, 70, 70]), 0]
    pygame.draw.rect(screen, 'white', [20, 20, 50, 50])
    circ = [pygame.draw.rect(screen, (96, 96, 96), [100, 10, 70, 70]), 1]
    pygame.draw.circle(screen, 'white', [135, 45], 30)
    triangle = [pygame.draw.rect(screen, (96, 96, 96), [200, 10, 70, 70]), 2]
    pygame.draw.polygon(screen, 'white', ((235,20),(260,70),(210,70)))
    rhomb = [pygame.draw.rect(screen, (96, 96, 96), [300, 10, 70, 70]), 3]
    pygame.draw.polygon(screen, 'white', ((335,15),(360,45),(335,75),(310,45)))
    right_triangle = [pygame.draw.rect(screen, (96, 96, 96), [400, 10, 70, 70]), 4]
    pygame.draw.polygon(screen, 'white', ((410,20),(410,70),(460,70)))
    
    #Colors
    blue = [pygame.draw.rect(screen, (0, 0, 255), [w - 35, 10, 25, 25]), (0, 0, 255)]
    red = [pygame.draw.rect(screen, (255, 0, 0), [w - 35, 35, 25, 25]), (255, 0, 0)]
    green = [pygame.draw.rect(screen, (0, 255, 0), [w - 60, 10, 25, 25]), (0, 255, 0)]
    yellow = [pygame.draw.rect(screen, (255, 255, 0), [w - 60, 35, 25, 25]), (255, 255, 0)]
    black = [pygame.draw.rect(screen, (0, 0, 0), [w - 85, 10, 25, 25]), (0, 0, 0)]
    purple = [pygame.draw.rect(screen, (255, 0, 255), [w - 85, 35, 25, 25]), (255, 0, 255)]

    # Сдвинули ластик чуть правее, чтобы освободить место
    eraser = [pygame.draw.rect(screen, (253, 166, 215), [560, 20, 50, 50]), (255, 255, 255)] #Eraser

    # Выводим текущий размер на экран (тоже немного сдвинули)
    font = pygame.font.SysFont(None, 24)
    size_text = font.render(f"Size: {activeSize}", True, (0, 0, 0))
    screen.blit(size_text, (630, 35))

    # ИСПРАВЛЕННАЯ КНОПКА CLEAR: меньше размером и стоит на свободном месте (x = 480)
    clear_btn = pygame.draw.rect(screen, (255, 100, 100), [480, 25, 65, 40], border_radius=5)
    clear_font = pygame.font.SysFont(None, 22) # Шрифт поменьше для маленькой кнопки
    clear_text = clear_font.render("CLEAR", True, (255, 255, 255))
    screen.blit(clear_text, (488, 38)) # Идеально отцентрированный текст

    return [blue, red, green, yellow, black, purple, eraser], [rect, circ, triangle, rhomb, right_triangle], clear_btn

def drawPaint(paints):
    for paint in paints:
        color, pos, shape, size = paint 
        x, y = pos
        
        if shape == 1:
            pygame.draw.circle(screen, color, pos, size)
        elif shape == 0:
            pygame.draw.rect(screen, color, [x - size, y - size, size * 2, size * 2])
        elif shape == 2:
            pygame.draw.polygon(screen, color, ((x - size, y + size), (x, y - size), (x + size, y + size)))
        elif shape == 3:
            pygame.draw.polygon(screen, color, ((x, y - int(size*1.3)), (x + size, y), (x, y + int(size*1.3)), (x - size, y)))
        elif shape == 4:
            pygame.draw.polygon(screen, color, ((x - size, y - int(size*1.5)), (x + int(size*1.5), y + size), (x - size, y + size)))

def draw():
    global activeColor, activeShape, mouse, activeSize
    if mouse[1] > 100:
        x, y = mouse
        size = activeSize
        
        if activeShape == 0:
            pygame.draw.rect(screen, activeColor, [x - size, y - size, size * 2, size * 2])
        elif activeShape == 1:
            pygame.draw.circle(screen, activeColor, mouse, size)
        elif activeShape == 2:
            pygame.draw.polygon(screen, activeColor, ((x - size, y + size), (x, y - size), (x + size, y + size)))
        elif activeShape == 3:
            pygame.draw.polygon(screen, activeColor, ((x, y - int(size*1.3)), (x + size, y), (x, y + int(size*1.3)), (x - size, y)))
        elif activeShape == 4:
            pygame.draw.polygon(screen, activeColor, ((x - size, y - int(size*1.5)), (x + int(size*1.5), y + size), (x - size, y + size)))

run = True
while run:
    timer.tick(fps) #FPS
    screen.fill('white') # Fill Screen
    
    colors, shape, clear_btn = drawDisplay() 

    mouse = pygame.mouse.get_pos()
    draw()
    click = pygame.mouse.get_pressed()[0] # Get Mouse Button Pressed
    
    if click and mouse[1] > 100:
        painting.append((activeColor, mouse, activeShape, activeSize)) 
        
    drawPaint(painting)

    for event in pygame.event.get(): # Set quit event
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_SPACE: 
                painting = []
            
            if event.key == pygame.K_UP:
                activeSize += 2
            if event.key == pygame.K_DOWN and activeSize > 2:
                activeSize -= 2

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4: 
                activeSize += 2
            if event.button == 5 and activeSize > 2: 
                activeSize -= 2
            
            if event.button == 1: 
                if clear_btn.collidepoint(event.pos):
                    painting = [] 
                
                for i in colors:
                    if i[0].collidepoint(event.pos):
                        activeColor = i[1]
                for i in shape:
                    if i[0].collidepoint(event.pos):
                        activeShape = i[1]
                        
    pygame.display.flip() 
    
pygame.quit()