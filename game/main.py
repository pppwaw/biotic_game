import random

import pygame
import sys

from game.ball import Ball
from game.cv import CV
from game.track import Track

# 初始化Pygame
pygame.init()

video_path = r"../video/chlamy_PDMS.avi"
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


def game_screen():
    global score, game_time
    cv = CV(video_path, screen_width, screen_height)
    track = Track(screen_width, screen_height)

    clock = pygame.time.Clock()
    start_ticks = pygame.time.get_ticks()

    running = True
    while running:
        image, boxes = cv.get_image_and_boxes()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    cv.select_left(boxes, image)
                if event.key == pygame.K_RIGHT:
                    cv.select_right(boxes, image)
                if event.key == pygame.K_UP:
                    cv.select_up(boxes, image)
                if event.key == pygame.K_DOWN:
                    cv.select_down(boxes, image)
                if event.key == pygame.K_r:
                    cv.boxes = [cv.boxes[0]]
                    cv.trackers = [cv.trackers[0]]

        if boxes:
            # 吃黄球
            selected_box = cv.box
            for ball in track.yellow_balls:
                if selected_box.colliderect(ball.rect()):
                    score += 10
                    track.yellow_balls.remove(ball)
                    x = random.randint(0, screen_width - 20)
                    y = random.randint(0, screen_height - 20)
                    ball_rect = pygame.Rect(x - 10, y - 10, 20, 20)
                    track.yellow_balls.append(Ball((255, 255, 0), x, y))
                    break

        # 计算剩余时间
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        # if seconds > game_time:
        #     running = False

        # 绘制界面
        # 用image 绘制
        # turn ndarray to surface
        image = pygame.image.frombuffer(image.tobytes(), image.shape[1::-1], "BGR")
        screen.blit(image, (0, 0))
        track.draw(screen)
        for box in boxes:
            box.draw(screen)

        # 绘制分数和进度条
        score_text = small_font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        progress_bar_length = 200
        pygame.draw.rect(screen, BLACK, (screen_width - 220, 10, progress_bar_length, 20), 2)
        pygame.draw.rect(screen, BLACK, (screen_width - 220, 10, int(progress_bar_length * (seconds / game_time)), 20))

        pygame.display.flip()
        clock.tick(30)

    game_over_screen()


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
