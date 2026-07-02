import pygame

class Explosion:
    def __init__(self, x, y, color=(255, 165, 0)):
        self.x = x
        self.y = y
        self.color = color
        self.radius = 5
        self.max_radius = 35
        self.alpha = 255
        self.done = False

    def update(self):
        self.radius += 3
        self.alpha = max(0, int(255 * (1 - self.radius / self.max_radius)))
        if self.radius >= self.max_radius:
            self.done = True

    def draw(self, screen):
        if not self.done:
            surf = pygame.Surface((self.max_radius * 2 + 10, self.max_radius * 2 + 10), pygame.SRCALPHA)
            color_with_alpha = (*self.color, self.alpha)
            pygame.draw.circle(surf, color_with_alpha, (self.max_radius + 5, self.max_radius + 5), self.radius, 4)
            screen.blit(surf, (self.x - self.max_radius - 5, self.y - self.max_radius - 5))
