import pygame
from settings import *
from states.base import BaseState

class MenuState(BaseState):
    def __init__(self, game):
        super().__init__(game)
        self.blink_timer = 0
        self.show_prompt = True

    def get_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # Local import to avoid circular dependency
                from states.play import PlayState
                self.game.change_state_replace(PlayState(self.game))

    def update(self):
        self.blink_timer += 1
        if self.blink_timer >= 30:
            self.show_prompt = not self.show_prompt
            self.blink_timer = 0

    def draw(self, screen):
        title = self.game.title_font.render("SPACE", True, CYAN)
        title2 = self.game.title_font.render("INVADERS", True, YELLOW)
        screen.blit(title,  (SCREEN_WIDTH // 2 - title.get_width()  // 2, 140))
        screen.blit(title2, (SCREEN_WIDTH // 2 - title2.get_width() // 2, 220))

        hs_text = self.game.font.render(f"High Score: {self.game.highscore}", True, WHITE)
        screen.blit(hs_text, (SCREEN_WIDTH // 2 - hs_text.get_width() // 2, 330))

        if self.show_prompt:
            prompt = self.game.font.render("Press SPACE to Play", True, WHITE)
            screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, 400))

        ctrl = self.game.font.render("← → to move  |  SPACE to shoot", True, GRAY)
        screen.blit(ctrl, (SCREEN_WIDTH // 2 - ctrl.get_width() // 2, 480))
