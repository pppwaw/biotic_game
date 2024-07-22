import pygame

ball_image = pygame.image.load('chong.png')
ball_image = pygame.transform.scale(ball_image, (20, 20))


class Ball:
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y
        self.radius = 10

    def draw(self, screen):
        if self.color == (255, 0, 0):
            screen.blit(ball_image, (self.x - 10, self.y - 10))
        else:
            pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
