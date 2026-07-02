import pygame
from settings import *
from states.base import BaseState

class GameOverState(BaseState):
    def __init__(self, game, score):
        super().__init__(game)
        self.score = score
        self.timer = 0
        if self.score > self.game.highscore:
            self.game.highscore = self.score
            save_highscore(self.game.highscore)

    def get_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                from states.play import PlayState
                self.game.change_state_replace(PlayState(self.game))

    def update(self):
        self.timer += 1

    def draw(self, screen):
        go = self.game.large_font.render("GAME OVER", True, RED)
        screen.blit(go, (SCREEN_WIDTH // 2 - go.get_width() // 2, 160))

        sc = self.game.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(sc, (SCREEN_WIDTH // 2 - sc.get_width() // 2, 260))

        hs_color = YELLOW if self.score >= self.game.highscore else WHITE
        hs = self.game.font.render(f"High Score: {self.game.highscore}", True, hs_color)
        screen.blit(hs, (SCREEN_WIDTH // 2 - hs.get_width() // 2, 300))

        if self.score >= self.game.highscore and self.score > 0:
            new_rec = self.game.font.render("★ NEW RECORD! ★", True, YELLOW)
            screen.blit(new_rec, (SCREEN_WIDTH // 2 - new_rec.get_width() // 2, 350))

        if self.timer > 90:
            prompt = self.game.font.render("Press SPACE to Play Again", True, WHITE)
            screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, 430))
