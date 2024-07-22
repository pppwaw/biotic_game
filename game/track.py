import pygame
import random
from ball import Ball

class Track:
    def __init__(self, screen_width, screen_height):
        self.yellow_balls = []
        for _ in range(100):
            # while True:
                x = random.randint(0, screen_width - 20)
                y = random.randint(0, screen_height - 20)
                ball_rect = pygame.Rect(x - 10, y - 10, 20, 20)
                # if not any(fence.colliderect(ball_rect) for fence in self.fences):
                self.yellow_balls.append(Ball((255, 255, 0), x, y))
                # break

    def draw(self, screen):
        for ball in self.yellow_balls:
            ball.draw(screen)