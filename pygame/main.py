import pygame
import random
import serial
import sys
from ball import Ball
from track import Track
from utils import find_closest_ball

# 初始化Pygame
pygame.init()

# 屏幕设置
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Racing Chlamy")

# 颜色设置
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# 字体设置
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

# 游戏变量
score = 0
game_time = 60
joy_stick=False

# 速度设置
speed = 5

triangle_size = 10
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
    x, y = keys.split()
    x, y = int(x), int(y)
    # 根据按键状态绘制指向不同方向的三角形
    if y > 0:
        draw_triangle(surface, BLACK, triangle_up, (x_offset, y_offset - 10))
    if y < 0:
        draw_triangle(surface, BLACK, triangle_down, (x_offset, y_offset + 10))
    if x < 0:
        draw_triangle(surface, BLACK, triangle_left, (x_offset - 10, y_offset))
    if x > 0:
        draw_triangle(surface, BLACK, triangle_right, (x_offset + 10, y_offset))


# 串口设置
def init_serial():
    global joy_stick
    try:
        ser = serial.Serial('COM8', 9600, timeout=1)
        if ser.is_open:
            joy_stick=True
        return ser
    except serial.SerialException as e:
        print(f"Error: could not open port 'COM8'. {e}")
        return None


def listen_serial(ser):
    if ser and ser.is_open:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            # print(f"Received data: {data}")
            t=data.split()
            if len(t) == 2:
                return data
            else:
                return None
    return None

def move(ball,track,dx,dy):
    ball_rect = pygame.Rect(ball.x + dx - ball.radius, ball.y + dy - ball.radius, ball.radius * 2,ball.radius * 2)
    if 0 < ball.x + dx < screen_width and 0 < ball.y + dy < screen_height and not track.check_collision(ball_rect):
        ball.x += dx
        ball.y += dy


def move_balls(balls, direction,track):
    for ball in balls:
        dx, dy = 0, 0
        if direction == "UP":
            dy = -(speed + random.randint(-1, 1))
        elif direction == "DOWN":
            dy = speed + random.randint(-1, 1)
        elif direction == "LEFT":
            dx = -(speed + random.randint(-1, 1))
        elif direction == "RIGHT":
            dx = speed + random.randint(-1, 1)

        move(ball,track, dx, dy)


def game_screen():
    global score, game_time,joy_stick

    # 创建蓝球和红球
    track = Track(screen_width, screen_height)
    balls = []
    for _ in range(10):
        while True:
            x = random.randint(50, screen_width // 2 - 50)
            y = random.randint(50, screen_height - 50)
            ball_rect = pygame.Rect(x - 10, y - 10, 20, 20)
            if not track.check_collision(ball_rect):
                balls.append(Ball(BLUE, x, y))
                break

    selected_index = 0
    balls[selected_index].color = RED

    clock = pygame.time.Clock()
    start_ticks = pygame.time.get_ticks()

    pre = None
    ser = init_serial()  # 初始化串口

    running = True
    while running:
        for ball in balls:
            dx = random.randint(-5, 5)
            dy = random.randint(-5, 5)
            move(ball,track,dx,dy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    balls[selected_index].color = (0, 0, 255)
                    selected_index = find_closest_ball(balls, selected_index, "UP")
                    balls[selected_index].color = (255, 0, 0)
                if event.key == pygame.K_DOWN:
                    balls[selected_index].color = (0, 0, 255)
                    selected_index = find_closest_ball(balls, selected_index, "DOWN")
                    balls[selected_index].color = (255, 0, 0)
                if event.key == pygame.K_LEFT:
                    balls[selected_index].color = (0, 0, 255)
                    selected_index = find_closest_ball(balls, selected_index, "LEFT")
                    balls[selected_index].color = (255, 0, 0)
                if event.key == pygame.K_RIGHT:
                    balls[selected_index].color = (0, 0, 255)
                    selected_index = find_closest_ball(balls, selected_index, "RIGHT")
                    balls[selected_index].color = (255, 0, 0)

        keys = pygame.key.get_pressed()
        data = listen_serial(ser)
        if data:
            print(data)
            x, y = data.split()
            x, y = int(x), int(y)
            if y > 0:
                move_balls(balls, "UP",track)
            if y < 0:
                move_balls(balls, "DOWN",track)
            if x < 0:
                move_balls(balls, "LEFT",track)
            if x > 0:
                move_balls(balls, "RIGHT",track)

        if joy_stick:
            if keys[pygame.K_w]:
                move_balls(balls, "UP", track)
            if keys[pygame.K_s]:
                move_balls(balls, "DOWN", track)
            if keys[pygame.K_a]:
                move_balls(balls, "LEFT", track)
            if keys[pygame.K_d]:
                move_balls(balls, "RIGHT", track)

        # 边界检查
        for ball in balls:
            if ball.x - ball.radius < 0:
                ball.x = ball.radius
            if ball.x + ball.radius > screen_width:
                ball.x = screen_width - ball.radius
            if ball.y - ball.radius < 0:
                ball.y = ball.radius
            if ball.y + ball.radius > screen_height:
                ball.y = screen_height - ball.radius

        # 碰撞检查
        for ball in balls:
            ball_rect = pygame.Rect(ball.x - ball.radius, ball.y - ball.radius, ball.radius * 2, ball.radius * 2)
            if track.check_collision(ball_rect):
                if keys[pygame.K_w]:
                    ball.y += speed
                if keys[pygame.K_s]:
                    ball.y -= speed
                if keys[pygame.K_a]:
                    ball.x += speed
                if keys[pygame.K_d]:
                    ball.x -= speed

        # 吃黄球
        for ball in track.yellow_balls:
            if pygame.Rect(ball.x - ball.radius, ball.y - ball.radius, ball.radius * 2, ball.radius * 2).colliderect(
                    pygame.Rect(balls[selected_index].x - balls[selected_index].radius,
                                balls[selected_index].y - balls[selected_index].radius,
                                balls[selected_index].radius * 2, balls[selected_index].radius * 2)):
                score += 10
                track.yellow_balls.remove(ball)
                while True:
                    x = random.randint(0, screen_width - 20)
                    y = random.randint(0, screen_height - 20)
                    ball_rect = pygame.Rect(x - 10, y - 10, 20, 20)
                    if not track.check_collision(ball_rect):
                        track.yellow_balls.append(Ball(YELLOW, x, y))
                        break

        # 计算剩余时间
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        if seconds > game_time:
            running = False

        # 绘制界面
        screen.fill(WHITE)
        for ball in balls:
            ball.draw(screen)
        track.draw(screen)

        # 绘制分数和进度条
        score_text = small_font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        progress_bar_length = 200
        pygame.draw.rect(screen, BLACK, (screen_width - 220, 10, progress_bar_length, 20), 2)
        pygame.draw.rect(screen, BLACK, (screen_width - 220, 10, int(progress_bar_length * (seconds / game_time)), 20))

        if data:
            draw_key_indicator(screen, data)
            pre = data
        elif pre is not None:
            draw_key_indicator(screen, pre)
        pygame.display.flip()
        clock.tick(60)

    if joy_stick:
        ser.close()
        joy_stick=False
    game_over_screen()


# 创建游戏结束界面
def game_over_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                main()

        screen.fill(WHITE)
        game_over_text = font.render("Game Over", True, BLACK)
        score_text = small_font.render(f"Score: {score}", True, BLACK)
        restart_text = small_font.render("Press Enter to Restart", True, BLACK)

        screen.blit(game_over_text, (screen_width // 2 - 150, screen_height // 2 - 50))
        screen.blit(score_text, (screen_width // 2 - 50, screen_height // 2 + 10))
        screen.blit(restart_text, (screen_width // 2 - 150, screen_height // 2 + 50))

        pygame.display.flip()


# 创建开始界面
def main():
    global score, game_time
    score = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_screen()

        screen.fill(WHITE)
        title_text = font.render("Racing Chlamy", True, BLACK)
        start_text = small_font.render("Press Enter to Start", True, BLACK)

        screen.blit(title_text, (screen_width // 2 - 200, screen_height // 2 - 50))
        screen.blit(start_text, (screen_width // 2 - 150, screen_height // 2 + 10))

        pygame.display.flip()


if __name__ == "__main__":
    main()
