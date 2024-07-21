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

# 字体设置
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

# 游戏变量
score = 0
game_time = 60

# 速度设置
speed = 5

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
                balls.append(Ball((0, 0, 255), x, y))
                break

    selected_index = 0
    balls[selected_index].color = (255, 0, 0)

    clock = pygame.time.Clock()
    start_ticks = pygame.time.get_ticks()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    balls[selected_index].color = (0, 0, 255)
                    selected_index = find_closest_ball(balls, selected_index, direction="UP")
                    balls[selected_index].color = (255, 0, 0)
                if event.key == pygame.K_DOWN:
                    balls[selected_index].color = (0, 0, 255)
                    selected_index = find_closest_ball(balls, selected_index, direction="DOWN")
                    balls[selected_index].color = (255, 0, 0)
                if event.key == pygame.K_LEFT:
                    balls[selected_index].color = (0, 0, 255)
                    selected_index = find_closest_ball(balls, selected_index, direction="LEFT")
                    balls[selected_index].color = (255, 0, 0)
                if event.key == pygame.K_RIGHT:
                    balls[selected_index].color = (0, 0, 255)
                    selected_index = find_closest_ball(balls, selected_index, direction="RIGHT")
                    balls[selected_index].color = (255, 0, 0)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            balls[selected_index].y -= speed
        if keys[pygame.K_s]:
            balls[selected_index].y += speed
        if keys[pygame.K_a]:
            balls[selected_index].x -= speed
        if keys[pygame.K_d]:
            balls[selected_index].x += speed

        # 边界检查
        if balls[selected_index].x - balls[selected_index].radius < 0:
            balls[selected_index].x = balls[selected_index].radius
        if balls[selected_index].x + balls[selected_index].radius > screen_width:
            balls[selected_index].x = screen_width - balls[selected_index].radius
        if balls[selected_index].y - balls[selected_index].radius < 0:
            balls[selected_index].y = balls[selected_index].radius
        if balls[selected_index].y + balls[selected_index].radius > screen_height:
            balls[selected_index].y = screen_height - balls[selected_index].radius

        # 碰撞检查
        if track.check_collision(pygame.Rect(balls[selected_index].x - balls[selected_index].radius, balls[selected_index].y - balls[selected_index].radius, balls[selected_index].radius * 2, balls[selected_index].radius * 2)):
            if keys[pygame.K_w]:
                balls[selected_index].y += speed
            if keys[pygame.K_s]:
                balls[selected_index].y -= speed
            if keys[pygame.K_a]:
                balls[selected_index].x += speed
            if keys[pygame.K_d]:
                balls[selected_index].x -= speed

        # 吃黄球
        for ball in track.yellow_balls:
            if pygame.Rect(ball.x - ball.radius, ball.y - ball.radius, ball.radius * 2, ball.radius * 2).colliderect(pygame.Rect(balls[selected_index].x - balls[selected_index].radius, balls[selected_index].y - balls[selected_index].radius, balls[selected_index].radius * 2, balls[selected_index].radius * 2)):
                score += 10
                track.yellow_balls.remove(ball)
                while True:
                    x = random.randint(0, screen_width - 20)
                    y = random.randint(0, screen_height - 20)
                    ball_rect = pygame.Rect(x - 10, y - 10, 20, 20)
                    if not track.check_collision(ball_rect):
                        track.yellow_balls.append(Ball((255, 255, 0), x, y))
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
