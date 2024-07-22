import pygame
import random
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

# 速度设置
speed = 5

def move_balls(balls, direction):
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

        if 0 < ball.x + dx < screen_width and 0 < ball.y + dy < screen_height:
            ball.x += dx
            ball.y += dy

def draw_direction_arrows(screen, direction):
    arrow_length = 50
    arrow_width = 10
    if direction == "UP":
        pygame.draw.polygon(screen, BLACK, [(screen_width // 2, screen_height // 2 - arrow_length),
                                            (screen_width // 2 - arrow_width, screen_height // 2 - arrow_width),
                                            (screen_width // 2 + arrow_width, screen_height // 2 - arrow_width)])
    elif direction == "DOWN":
        pygame.draw.polygon(screen, BLACK, [(screen_width // 2, screen_height // 2 + arrow_length),
                                            (screen_width // 2 - arrow_width, screen_height // 2 + arrow_width),
                                            (screen_width // 2 + arrow_width, screen_height // 2 + arrow_width)])
    elif direction == "LEFT":
        pygame.draw.polygon(screen, BLACK, [(screen_width // 2 - arrow_length, screen_height // 2),
                                            (screen_width // 2 - arrow_width, screen_height // 2 - arrow_width),
                                            (screen_width // 2 - arrow_width, screen_height // 2 + arrow_width)])
    elif direction == "RIGHT":
        pygame.draw.polygon(screen, BLACK, [(screen_width // 2 + arrow_length, screen_height // 2),
                                            (screen_width // 2 + arrow_width, screen_height // 2 - arrow_width),
                                            (screen_width // 2 + arrow_width, screen.height // 2 + arrow_width)])

def game_screen():
    global score, game_time

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

    direction = None  # 初始方向为空

    running = True
    while running:
        for ball in balls:

            dx = random.randint(-5, 5)
            dy = random.randint(-5, 5)
            ball_rect = pygame.Rect(ball.x +dx - ball.radius, ball.y + dy - ball.radius, ball.radius * 2, ball.radius * 2)
            if 0 < ball.x + dx < screen_width and 0 < ball.y + dy < screen_height and not track.check_collision(ball_rect) :
                ball.x += dx
                ball.y += dy

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    direction = "UP"
                if event.key == pygame.K_DOWN:
                    direction = "DOWN"
                if event.key == pygame.K_LEFT:
                    direction = "LEFT"
                if event.key == pygame.K_RIGHT:
                    direction = "RIGHT"
                if event.key == pygame.K_SPACE:
                    balls[selected_index].color = BLUE if balls[selected_index].color == RED else RED
                    selected_index = find_closest_ball(balls, selected_index, direction)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            move_balls(balls, "UP")
        if keys[pygame.K_s]:
            move_balls(balls, "DOWN")
        if keys[pygame.K_a]:
            move_balls(balls, "LEFT")
        if keys[pygame.K_d]:
            move_balls(balls, "RIGHT")

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
                    pygame.Rect(balls[selected_index].x - balls[selected_index].radius, balls[selected_index].y - balls[selected_index].radius, balls[selected_index].radius * 2, balls[selected_index].radius * 2)):
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

        if direction:
            draw_direction_arrows(screen, direction)

        # 绘制分数和进度条
        score_text = small_font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        progress_bar_length = 200
        pygame.draw.rect(screen, BLACK, (screen_width - 220, 10, progress_bar_length, 20), 2)
        pygame.draw.rect(screen, BLACK, (screen_width - 220, 10, int(progress_bar_length * (seconds / game_time)), 20))

        pygame.display.flip()
        clock.tick(60)

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
