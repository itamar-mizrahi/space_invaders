import pygame

class Bullet:
    def __init__(self, x, y, speed, color, piercing=False, is_enemy=False):
        self.width = 10 if piercing else 5
        self.height = 20 if piercing else 15
        self.color = color
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.speed = speed
        self.piercing = piercing
        self.is_enemy = is_enemy

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
