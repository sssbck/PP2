import pygame
import datetime
from tools import (flood_fill, get_rect, draw_square, 
                   draw_right_triangle, draw_eq_triangle, draw_rhombus)

pygame.init()

# Настройки окна
WIDTH, HEIGHT = 1000, 700
UI_HEIGHT = 80  # Высота нашей верхней панели
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS 2: Paint Pro with UI")

# Цвета для рисования и UI
COLORS = {
    'black': (0, 0, 0), 'white': (255, 255, 255),
    'red': (255, 0, 0), 'green': (0, 255, 0),
    'blue': (0, 0, 255), 'yellow': (255, 255, 0),
    'magenta': (255, 0, 255), 'cyan': (0, 255, 255)
}

# Шрифты
ui_font = pygame.font.SysFont('arial', 18, bold=True)
text_tool_font = pygame.font.SysFont('arial', 36)

# Состояние приложения
current_color = COLORS['black']
brush_size = 5
current_tool = 'pencil'
drawing = False
typing = False
current_text = ""
text_pos = None

# Холст (Canvas) - реальная зона для рисования
canvas = pygame.Surface((WIDTH, HEIGHT - UI_HEIGHT))
canvas.fill(COLORS['white'])

# Слой предпросмотра (Preview) - чтобы фигуры не оставляли след при растягивании
preview_layer = pygame.Surface((WIDTH, HEIGHT - UI_HEIGHT), pygame.SRCALPHA)

# --- СОЗДАНИЕ UI ЭЛЕМЕНТОВ ---
# Кнопки инструментов (координаты x, y, w, h)
tools_ui = [
    {"id": "pencil", "rect": pygame.Rect(10, 10, 50, 30), "label": "Pen"},
    {"id": "line", "rect": pygame.Rect(70, 10, 50, 30), "label": "Line"},
    {"id": "fill", "rect": pygame.Rect(130, 10, 50, 30), "label": "Fill"},
    {"id": "text", "rect": pygame.Rect(190, 10, 50, 30), "label": "Text"},
    {"id": "eraser", "rect": pygame.Rect(250, 10, 50, 30), "label": "Eras"},
    
    # Геометрические фигуры (нижний ряд)
    {"id": "square", "rect": pygame.Rect(10, 45, 50, 30), "label": ""},
    {"id": "rect", "rect": pygame.Rect(70, 45, 50, 30), "label": ""},
    {"id": "circle", "rect": pygame.Rect(130, 45, 50, 30), "label": ""},
    {"id": "right_tri", "rect": pygame.Rect(190, 45, 50, 30), "label": ""},
    {"id": "eq_tri", "rect": pygame.Rect(250, 45, 50, 30), "label": ""},
    {"id": "rhombus", "rect": pygame.Rect(310, 45, 50, 30), "label": ""},
]

# Палитра цветов (как на твоем скрине: блок 2x3)
palette_rects = [
    (COLORS['black'], pygame.Rect(390, 15, 25, 25)),
    (COLORS['green'], pygame.Rect(415, 15, 25, 25)),
    (COLORS['blue'], pygame.Rect(440, 15, 25, 25)),
    (COLORS['magenta'], pygame.Rect(390, 40, 25, 25)),
    (COLORS['yellow'], pygame.Rect(415, 40, 25, 25)),
    (COLORS['red'], pygame.Rect(440, 40, 25, 25)),
]

# Кнопки управления размером и очисткой
size_minus_btn = pygame.Rect(630, 25, 30, 30)
size_plus_btn = pygame.Rect(670, 25, 30, 30)
clear_btn = pygame.Rect(730, 25, 80, 30)


def draw_ui():
    """Отрисовка всей верхней панели управления"""
    # Светло-зеленый фон как на скриншоте
    pygame.draw.rect(screen, (225, 255, 225), (0, 0, WIDTH, UI_HEIGHT))
    pygame.draw.line(screen, (150, 150, 150), (0, UI_HEIGHT), (WIDTH, UI_HEIGHT), 2)

    # 1. Отрисовка инструментов
    for t in tools_ui:
        # Темно-серый фон для кнопки (светлее, если выбрано)
        bg_color = (150, 150, 150) if current_tool == t['id'] else (80, 80, 80)
        pygame.draw.rect(screen, bg_color, t['rect'])
        
        # Отрисовка иконок внутри кнопок
        cx, cy = t['rect'].center
        icolor = COLORS['white']
        if t['id'] == 'square': pygame.draw.rect(screen, icolor, (cx-10, cy-10, 20, 20))
        elif t['id'] == 'rect': pygame.draw.rect(screen, icolor, (cx-15, cy-10, 30, 20))
        elif t['id'] == 'circle': pygame.draw.circle(screen, icolor, (cx, cy), 12)
        elif t['id'] == 'eq_tri': pygame.draw.polygon(screen, icolor, [(cx, cy-12), (cx-12, cy+10), (cx+12, cy+10)])
        elif t['id'] == 'right_tri': pygame.draw.polygon(screen, icolor, [(cx-10, cy-12), (cx-10, cy+10), (cx+12, cy+10)])
        elif t['id'] == 'rhombus': pygame.draw.polygon(screen, icolor, [(cx, cy-12), (cx-12, cy), (cx, cy+12), (cx+12, cy)])
        else:
            # Для текста, карандаша и заливки пишем текст
            lbl = ui_font.render(t['label'], True, icolor)
            screen.blit(lbl, lbl.get_rect(center=(cx, cy)))

    # 2. Отрисовка палитры и рамки вокруг выбранного
    for color, rect in palette_rects:
        pygame.draw.rect(screen, color, rect)
        if current_color == color:
            pygame.draw.rect(screen, (0, 0, 0), rect, 3) # Обводка

    # 3. Индикатор текущего цвета (большой квадрат слева от палитры)
    pygame.draw.rect(screen, current_color, (490, 20, 40, 40))
    pygame.draw.rect(screen, (100, 100, 100), (490, 20, 40, 40), 2)

    # 4. Управление размером (Size: X)
    size_txt = ui_font.render(f"Size: {brush_size}", True, (0, 0, 0))
    screen.blit(size_txt, (550, 30))
    
    pygame.draw.rect(screen, (200, 200, 200), size_minus_btn, border_radius=5)
    pygame.draw.rect(screen, (200, 200, 200), size_plus_btn, border_radius=5)
    screen.blit(ui_font.render("-", True, COLORS['black']), size_minus_btn.move(10, 5))
    screen.blit(ui_font.render("+", True, COLORS['black']), size_plus_btn.move(10, 5))

    # 5. Кнопка CLEAR
    pygame.draw.rect(screen, (255, 100, 100), clear_btn, border_radius=5)
    screen.blit(ui_font.render("CLEAR", True, COLORS['white']), clear_btn.move(12, 5))


def handle_ui_click(pos):
    """Проверяет, куда кликнули в панели управления"""
    global current_tool, current_color, brush_size
    
    for t in tools_ui:
        if t['rect'].collidepoint(pos):
            current_tool = t['id']
            return True

    for color, rect in palette_rects:
        if rect.collidepoint(pos):
            current_color = color
            return True

    if size_minus_btn.collidepoint(pos):
        brush_size = max(1, brush_size - 2)
        return True
    if size_plus_btn.collidepoint(pos):
        brush_size = min(50, brush_size + 2)
        return True
    if clear_btn.collidepoint(pos):
        canvas.fill(COLORS['white'])
        return True
        
    return False

# --- ГЛАВНЫЙ ЦИКЛ ---
clock = pygame.time.Clock()
running = True
start_pos = None
last_pos = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Сохранение (Ctrl+S) - сохраняет только сам холст (без кнопок)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
            ts = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            pygame.image.save(canvas, f"canvas_{ts}.png")
            print(f"Canvas saved: canvas_{ts}.png")

        # Логика ввода текста
        if typing and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                canvas.blit(text_tool_font.render(current_text, True, current_color), text_pos)
                typing = False
            elif event.key == pygame.K_ESCAPE:
                typing = False
            elif event.key == pygame.K_BACKSPACE:
                current_text = current_text[:-1]
            else:
                current_text += event.unicode

        # Клики мышкой
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if event.pos[1] < UI_HEIGHT:
                # Кликнули по панели инструментов
                handle_ui_click(event.pos)
                typing = False # Сбросить текст, если кликнули в меню
            else:
                # Кликнули по холсту (нужно скорректировать координаты по оси Y)
                canvas_pos = (event.pos[0], event.pos[1] - UI_HEIGHT)
                start_pos = canvas_pos
                last_pos = canvas_pos
                drawing = True

                if current_tool == 'fill':
                    flood_fill(canvas, start_pos[0], start_pos[1], current_color)
                    drawing = False
                elif current_tool == 'text':
                    typing = True
                    current_text = ""
                    text_pos = start_pos
                    drawing = False

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if drawing:
                drawing = False
                canvas_pos = (event.pos[0], event.pos[1] - UI_HEIGHT)
                
                # Финальная отрисовка на постоянный холст
                if current_tool == 'line': pygame.draw.line(canvas, current_color, start_pos, canvas_pos, brush_size)
                elif current_tool == 'rect': pygame.draw.rect(canvas, current_color, get_rect(start_pos, canvas_pos), brush_size)
                elif current_tool == 'circle':
                    r = get_rect(start_pos, canvas_pos)
                    pygame.draw.circle(canvas, current_color, r.center, min(r.width, r.height)//2, brush_size)
                elif current_tool == 'square': draw_square(canvas, current_color, start_pos, canvas_pos, brush_size)
                elif current_tool == 'right_tri': draw_right_triangle(canvas, current_color, start_pos, canvas_pos, brush_size)
                elif current_tool == 'eq_tri': draw_eq_triangle(canvas, current_color, start_pos, canvas_pos, brush_size)
                elif current_tool == 'rhombus': draw_rhombus(canvas, current_color, start_pos, canvas_pos, brush_size)

        elif event.type == pygame.MOUSEMOTION:
            if drawing:
                canvas_pos = (event.pos[0], event.pos[1] - UI_HEIGHT)
                if current_tool == 'pencil':
                    pygame.draw.line(canvas, current_color, last_pos, canvas_pos, brush_size)
                    last_pos = canvas_pos
                elif current_tool == 'eraser':
                    pygame.draw.line(canvas, COLORS['white'], last_pos, canvas_pos, brush_size * 4)
                    last_pos = canvas_pos

    # --- ОТРИСОВКА КАДРА ---
    screen.fill((200, 200, 200)) # Задник
    screen.blit(canvas, (0, UI_HEIGHT)) # Кладем холст ниже UI
    
    # Слой предпросмотра (Preview)
    preview_layer.fill((0, 0, 0, 0)) # Очищаем прозрачный слой
    if drawing:
        mouse_pos = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1] - UI_HEIGHT)
        if current_tool == 'line': pygame.draw.line(preview_layer, current_color, start_pos, mouse_pos, brush_size)
        elif current_tool == 'rect': pygame.draw.rect(preview_layer, current_color, get_rect(start_pos, mouse_pos), brush_size)
        elif current_tool == 'circle':
            r = get_rect(start_pos, mouse_pos)
            pygame.draw.circle(preview_layer, current_color, r.center, min(r.width, r.height)//2, brush_size)
        elif current_tool == 'square': draw_square(preview_layer, current_color, start_pos, mouse_pos, brush_size)
        elif current_tool == 'right_tri': draw_right_triangle(preview_layer, current_color, start_pos, mouse_pos, brush_size)
        elif current_tool == 'eq_tri': draw_eq_triangle(preview_layer, current_color, start_pos, mouse_pos, brush_size)
        elif current_tool == 'rhombus': draw_rhombus(preview_layer, current_color, start_pos, mouse_pos, brush_size)

    # Предпросмотр текста
    if typing and text_pos:
        txt_surf = text_tool_font.render(current_text + "|", True, current_color)
        preview_layer.blit(txt_surf, text_pos)

    # Накладываем превью поверх холста
    screen.blit(preview_layer, (0, UI_HEIGHT))
    
    # Рисуем UI панель самой верхней
    draw_ui()

    pygame.display.flip()
    clock.tick(120)

pygame.quit()