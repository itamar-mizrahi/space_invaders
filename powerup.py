import pygame

class PowerUp:
    def __init__(self, x, y, type):
        self.width = 15
        self.height = 15
        self.type = type
        if self.type == 'double':
            self.color = (0, 255, 255) # Cyan
        elif self.type == 'life':
            self.color = (0, 255, 0) # Green
        elif self.type == 'pierce':
            self.color = (255, 0, 255) # Purple
        elif self.type == 'shield':
            self.color = (0, 100, 255) # Blue
        else:
            self.color = (255, 255, 255) # White fallback
            
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.speed = 3

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
