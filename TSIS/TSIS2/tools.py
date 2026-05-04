import pygame
import math

def flood_fill(surface, x, y, fill_color):
    """
    Мгновенная заливка (DFS Stack) с правильной проверкой типов цветов.
    """
    w, h = surface.get_size()
    if not (0 <= x < w and 0 <= y < h):
        return

    # Блокируем холст и получаем массив пикселей
    pixel_array = pygame.PixelArray(surface)

    # ИСПРАВЛЕНИЕ: Берем исходный цвет прямо из числового массива!
    target_color = pixel_array[x, y] 
    
    # Конвертируем наш новый цвет тоже в число
    fill_color_mapped = surface.map_rgb(fill_color)

    # Если кликнули по тому же цвету - ничего не делаем
    if target_color == fill_color_mapped:
        pixel_array.close()
        return

    stack = [(x, y)]

    while stack:
        cx, cy = stack.pop()

        if pixel_array[cx, cy] == target_color:
            pixel_array[cx, cy] = fill_color_mapped

            # Проверяем границы и добавляем соседей в стек
            if cx > 0: stack.append((cx - 1, cy))
            if cx < w - 1: stack.append((cx + 1, cy))
            if cy > 0: stack.append((cx, cy - 1))
            if cy < h - 1: stack.append((cx, cy + 1))

    # Обязательно закрываем массив
    pixel_array.close()

# --- Shape Drawing Helpers ---

def get_rect(start_pos, end_pos):
    x = min(start_pos[0], end_pos[0])
    y = min(start_pos[1], end_pos[1])
    width = abs(start_pos[0] - end_pos[0])
    height = abs(start_pos[1] - end_pos[1])
    return pygame.Rect(x, y, width, height)

def draw_square(surface, color, start_pos, end_pos, width):
    rect = get_rect(start_pos, end_pos)
    side = min(rect.width, rect.height)
    square_rect = pygame.Rect(rect.x, rect.y, side, side)
    pygame.draw.rect(surface, color, square_rect, width)

def draw_right_triangle(surface, color, start_pos, end_pos, width):
    # Top-left to Bottom-right approach
    p1 = start_pos
    p2 = (start_pos[0], end_pos[1])
    p3 = end_pos
    pygame.draw.polygon(surface, color, [p1, p2, p3], width)

def draw_eq_triangle(surface, color, start_pos, end_pos, width):
    rect = get_rect(start_pos, end_pos)
    p1 = (rect.centerx, rect.top)
    p2 = (rect.left, rect.bottom)
    p3 = (rect.right, rect.bottom)
    pygame.draw.polygon(surface, color, [p1, p2, p3], width)

def draw_rhombus(surface, color, start_pos, end_pos, width):
    rect = get_rect(start_pos, end_pos)
    p1 = (rect.centerx, rect.top)
    p2 = (rect.right, rect.centery)
    p3 = (rect.centerx, rect.bottom)
    p4 = (rect.left, rect.centery)
    pygame.draw.polygon(surface, color, [p1, p2, p3, p4], width)