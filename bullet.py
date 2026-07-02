import pygame

class Bullet:
    def __init__(self, x, y, speed, color, piercing=False, is_enemy=False, speed_x=0):
        self.width = 10 if piercing else 5
        self.height = 20 if piercing else 15
        self.color = color
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.speed = speed
        self.speed_x = speed_x
        self.piercing = piercing
        self.is_enemy = is_enemy

    def update(self):
        self.rect.y += self.speed
        self.rect.x += self.speed_x

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
