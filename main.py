import pygame
import sys

# 初始化Pygame
pygame.init()

# 屏幕设置
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("WASD Indicator")

# 颜色设置
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 三角形顶点坐标
triangle_size = 20
triangle_up = [(0, -triangle_size), (-triangle_size, triangle_size), (triangle_size, triangle_size)]
triangle_down = [(0, triangle_size), (-triangle_size, -triangle_size), (triangle_size, -triangle_size)]
triangle_left = [(-triangle_size, 0), (triangle_size, -triangle_size), (triangle_size, triangle_size)]
triangle_right = [(triangle_size, 0), (-triangle_size, -triangle_size), (-triangle_size, triangle_size)]

def draw_triangle(surface, color, points, position):
    points = [(x + position[0], y + position[1]) for x, y in points]
    pygame.draw.polygon(surface, color, points)

def draw_key_indicator(surface, keys):
    x_offset = 40
    y_offset = screen_height - 60

    # 根据按键状态绘制指向不同方向的三角形
    if keys[pygame.K_w]:
        draw_triangle(surface, GREEN, triangle_up, (x_offset, y_offset))
    if keys[pygame.K_s]:
        draw_triangle(surface, GREEN, triangle_down, (x_offset, y_offset))
    if keys[pygame.K_a]:
        draw_triangle(surface, GREEN, triangle_left, (x_offset, y_offset))
    if keys[pygame.K_d]:
        draw_triangle(surface, GREEN, triangle_right, (x_offset, y_offset))

def game_loop():
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        screen.fill(WHITE)
        draw_key_indicator(screen, keys)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    game_loop()
