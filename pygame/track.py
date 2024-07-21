import pygame
import random
from ball import Ball

class Track:
    def __init__(self, screen_width, screen_height):
        self.fences = []
        for _ in range(5):
            x = random.randint(screen_width // 2, screen_width - 50)
            y = random.randint(50, screen_height - 50)
            width = random.randint(50, 150)
            height = random.randint(20, 50)
            self.fences.append(pygame.Rect(x, y, width, height))

        self.yellow_balls = []
        for _ in range(10):
            while True:
                x = random.randint(0, screen_width - 20)
                y = random.randint(0, screen_height - 20)
                ball_rect = pygame.Rect(x - 10, y - 10, 20, 20)
                if not any(fence.colliderect(ball_rect) for fence in self.fences):
                    self.yellow_balls.append(Ball((255, 255, 0), x, y))
                    break

    def draw(self, screen):
        for fence in self.fences:
            pygame.draw.rect(screen, (0, 0, 0), fence)
        for ball in self.yellow_balls:
            ball.draw(screen)

    def check_collision(self, ball_rect):
        return any(fence.colliderect(ball_rect) for fence in self.fences)
