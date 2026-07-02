import pygame

class Alien:
    def __init__(self, x, y):
        self.width = 40
        self.height = 40
        self.color = (255, 0, 0)
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
        # Load image
        try:
            img = pygame.image.load("alien.jpg").convert()
            img = pygame.transform.scale(img, (self.width, self.height))
            img.set_colorkey((0, 0, 0))
            self.image = img
        except:
            self.image = None

    def update(self, x_change, y_change):
        self.rect.x += x_change
        self.rect.y += y_change

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)

class BossAlien:
    def __init__(self, x, y, hp):
        self.width = 150
        self.height = 150
        self.color = (255, 100, 0)
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.hp = hp
        self.max_hp = hp
        
        # Load image
        try:
            img = pygame.image.load("boss.jpg").convert()
            img = pygame.transform.scale(img, (self.width, self.height))
            img.set_colorkey((0, 0, 0))
            self.image = img
        except:
            self.image = None

    def update(self, x_change, y_change):
        self.rect.x += x_change
        self.rect.y += y_change

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        # Draw HP bar
        hp_ratio = self.hp / self.max_hp
        hp_bar_width = int(self.width * hp_ratio)
        pygame.draw.rect(screen, (255, 0, 0), (self.rect.x, self.rect.y - 10, self.width, 5))
        pygame.draw.rect(screen, (0, 255, 0), (self.rect.x, self.rect.y - 10, hp_bar_width, 5))
