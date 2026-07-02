import pygame
import sys
import random
import asyncio
import random
from settings import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space Invaders")
        self.clock = pygame.time.Clock()
        self.highscore = load_highscore()
        
        self.font       = pygame.font.SysFont(None, 36)
        self.large_font = pygame.font.SysFont(None, 72)
        self.title_font = pygame.font.SysFont(None, 96)
        
        self.stars = []
        for _ in range(120):
            self.stars.append([random.randint(0, SCREEN_WIDTH),
                               random.randint(0, SCREEN_HEIGHT),
                               random.uniform(0.5, 2.0)])
                               
        self.state_stack = []

    def update_stars(self):
        for star in self.stars:
            star[1] += star[2]
            if star[1] > SCREEN_HEIGHT:
                star[1] = 0
                star[0] = random.randint(0, SCREEN_WIDTH)

    def draw_stars(self, screen):
        for star in self.stars:
            pygame.draw.circle(screen, GRAY, (int(star[0]), int(star[1])), 2)

    def change_state(self, new_state):
        self.state_stack.append(new_state)

    def change_state_replace(self, new_state):
        if self.state_stack:
            self.state_stack.pop()
        self.state_stack.append(new_state)
        
    def pop_state(self):
        if len(self.state_stack) > 1:
            self.state_stack.pop()
        else:
            pygame.quit()
            sys.exit()

    async def run(self):
        # Local import to avoid circular dependency
        from states.menu import MenuState
        self.change_state(MenuState(self))
        
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                    
            if len(self.state_stack) > 0:
                current_state = self.state_stack[-1]
                current_state.get_events(events)
                current_state.update()
                
                self.update_stars()
                self.screen.fill(BLACK)
                self.draw_stars(self.screen)
                
                current_state.draw(self.screen)
            else:
                pygame.quit(); sys.exit()

            pygame.display.flip()
            self.clock.tick(FPS)
            await asyncio.sleep(0)
