import pygame

class Player:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.width = 50
        self.height = 50 # Square image usually
        self.color = (0, 255, 0)
        self.x = self.screen_width // 2 - self.width // 2
        self.y = self.screen_height - self.height - 20
        self.speed = 5
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.lives = 3
        self.double_shot = False
        self.pierce_shot = False
        self.spread_shot = False
        self.powerup_timer = 0
        self.shield_active = False
        
        # Load image
        try:
            img = pygame.image.load("player.jpg").convert()
            img = pygame.transform.scale(img, (self.width, self.height))
            img.set_colorkey((0, 0, 0))
            self.image = img
        except:
            self.image = None

    def move_left(self):
        if self.rect.left > 0:
            self.rect.x -= self.speed

    def move_right(self):
        if self.rect.right < self.screen_width:
            self.rect.x += self.speed

    def update(self):
        if self.double_shot or self.pierce_shot or self.spread_shot:
            self.powerup_timer -= 1
            if self.powerup_timer <= 0:
                self.double_shot = False
                self.pierce_shot = False
                self.spread_shot = False

    def activate_double_shot(self, duration_frames):
        self.double_shot = True
        self.pierce_shot = False
        self.powerup_timer = duration_frames

    def activate_pierce_shot(self, duration_frames):
        self.pierce_shot = True
        self.double_shot = False
        self.spread_shot = False
        self.powerup_timer = duration_frames

    def activate_spread_shot(self, duration_frames):
        self.spread_shot = True
        self.double_shot = False
        self.pierce_shot = False
        self.powerup_timer = duration_frames
        
    def activate_shield(self):
        self.shield_active = True

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
            
        if self.shield_active:
            # Draw blue aura
            pygame.draw.circle(screen, (0, 100, 255), self.rect.center, self.width // 2 + 10, 3)
