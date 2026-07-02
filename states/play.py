import pygame
import random
from settings import *
from states.base import BaseState
from states.game_over import GameOverState
from states.menu import MenuState
from player import Player
from bullet import Bullet
from alien import Alien, BossAlien
from powerup import PowerUp
from explosion import Explosion
from sounds import (make_shoot_sound, make_explosion_sound,
                    make_powerup_sound, make_boss_hit_sound, make_hit_sound)

def create_aliens(rows, cols):
    aliens = []
    for row in range(rows):
        for col in range(cols):
            aliens.append(Alien(100 + col * 60, 50 + row * 60))
    return aliens

def create_boss(wave):
    hp = 20 + (wave // 3 - 1) * 10
    return [BossAlien(SCREEN_WIDTH // 2 - 75, 50, hp)]

def spawn_powerup(x, y, wave):
    types = ['double', 'double', 'pierce', 'life']
    if wave >= 4:
        types.extend(['shield', 'shield'])
    return PowerUp(x, y, random.choice(types))

class PlayState(BaseState):
    def __init__(self, game):
        super().__init__(game)
        self.snd_shoot    = make_shoot_sound()
        self.snd_explode  = make_explosion_sound()
        self.snd_powerup  = make_powerup_sound()
        self.snd_boss_hit = make_boss_hit_sound()
        self.snd_hit      = make_hit_sound()

        self.player         = Player(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.player_bullets = []
        self.enemy_bullets  = []
        self.powerups       = []
        self.explosions     = []

        self.wave             = 1
        self.base_speed       = 2.0
        self.alien_speed_x    = self.base_speed
        self.alien_drop       = 20
        self.aliens           = create_aliens(5, 10)
        self.is_boss_wave     = False
        self.boss_hits_taken  = 0
        self.score            = 0
        self.paused           = False

    def take_damage(self):
        if self.player.shield_active:
            self.player.shield_active = False
            self.snd_hit.play()
            return False
        else:
            self.player.lives -= 1
            self.snd_hit.play()
            return self.player.lives <= 0

    def get_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.change_state_replace(MenuState(self.game))
                elif event.key == pygame.K_p:
                    self.paused = not self.paused
                elif event.key == pygame.K_SPACE and len(self.player_bullets) < 5 and not self.paused:
                    if self.player.double_shot:
                        for bx in [self.player.rect.left, self.player.rect.right - 5]:
                            self.player_bullets.append(Bullet(bx, self.player.rect.top, -7, YELLOW))
                    elif self.player.pierce_shot:
                        self.player_bullets.append(Bullet(self.player.rect.centerx - 5, self.player.rect.top,
                                                      -7, PURPLE, piercing=True))
                    else:
                        self.player_bullets.append(Bullet(self.player.rect.centerx - 2, self.player.rect.top, -7, YELLOW))
                    self.snd_shoot.play()

    def update(self):
        if self.paused:
            return
            
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:  self.player.move_left()
        if keys[pygame.K_RIGHT]: self.player.move_right()
        self.player.update()

        for b in self.player_bullets[:]:
            b.update()
            if b.rect.bottom < 0:
                self.player_bullets.remove(b)

        for b in self.enemy_bullets[:]:
            b.update()
            if b.rect.top > SCREEN_HEIGHT:
                self.enemy_bullets.remove(b)
            elif b.rect.colliderect(self.player.rect):
                self.enemy_bullets.remove(b)
                if self.take_damage():
                    self.game.change_state_replace(GameOverState(self.game, self.score))
                    return

        for p in self.powerups[:]:
            p.update()
            if p.rect.colliderect(self.player.rect):
                if p.type == 'double':   self.player.activate_double_shot(FPS * 10)
                elif p.type == 'pierce': self.player.activate_pierce_shot(FPS * 5)
                elif p.type == 'life':   self.player.lives += 1
                elif p.type == 'shield': self.player.activate_shield()
                self.powerups.remove(p)
                self.score += 50
                self.snd_powerup.play()
            elif p.rect.top > SCREEN_HEIGHT:
                self.powerups.remove(p)

        for a in self.aliens:
            a.update(self.alien_speed_x, 0)
            if self.is_boss_wave and random.random() < 0.025:
                self.enemy_bullets.append(Bullet(a.rect.centerx - 2, a.rect.bottom, 5, RED, is_enemy=True))

        hit_wall = any(a.rect.right > SCREEN_WIDTH or a.rect.left < 0 for a in self.aliens)

        if hit_wall:
            self.alien_speed_x *= -1
            for a in self.aliens:
                if a.rect.right > SCREEN_WIDTH: a.rect.right = SCREEN_WIDTH
                elif a.rect.left < 0: a.rect.left = 0
            for a in self.aliens:
                a.update(0, self.alien_drop)
                if a.rect.bottom >= self.player.rect.top:
                    if self.take_damage():
                        self.game.change_state_replace(GameOverState(self.game, self.score))
                        return
                    else:
                        if self.is_boss_wave:
                            hp = a.hp
                            self.aliens = create_boss(self.wave)
                            self.aliens[0].hp = hp
                            self.alien_speed_x = (self.base_speed * 1.5) * (1 if self.alien_speed_x > 0 else -1)
                        else:
                            self.aliens = create_aliens(5, 10)
                            self.alien_speed_x = self.base_speed * (1 if self.alien_speed_x > 0 else -1)
                        self.enemy_bullets.clear()
                    break

        for b in self.player_bullets[:]:
            for a in self.aliens[:]:
                if b.rect.colliderect(a.rect):
                    if self.is_boss_wave:
                        a.hp -= 1
                        self.boss_hits_taken += 1
                        self.snd_boss_hit.play()
                        self.explosions.append(Explosion(a.rect.centerx, a.rect.centery, (255, 165, 0)))
                        if self.boss_hits_taken % 5 == 0:
                            self.powerups.append(spawn_powerup(a.rect.centerx, a.rect.bottom, self.wave))
                        if a.hp <= 0:
                            self.explosions.append(Explosion(a.rect.centerx, a.rect.centery, (255, 80, 0)))
                            self.aliens.remove(a)
                            self.score += 500
                    else:
                        self.explosions.append(Explosion(a.rect.centerx, a.rect.centery))
                        self.aliens.remove(a)
                        self.score += 10
                        self.snd_explode.play()
                        if random.random() < 0.15:
                            self.powerups.append(spawn_powerup(a.rect.centerx, a.rect.centery, self.wave))

                    if not b.piercing or self.is_boss_wave:
                        if b in self.player_bullets:
                            self.player_bullets.remove(b)
                        break

        for e in self.explosions[:]:
            e.update()
            if e.done:
                self.explosions.remove(e)

        if not self.aliens:
            self.wave += 1
            self.base_speed += 0.5
            if self.wave % 3 == 0:
                self.is_boss_wave    = True
                self.boss_hits_taken = 0
                self.aliens          = create_boss(self.wave)
                self.alien_speed_x   = self.base_speed * 1.5
            else:
                self.is_boss_wave  = False
                self.aliens        = create_aliens(5, 10)
                self.alien_speed_x = self.base_speed
            self.player_bullets.clear()
            self.enemy_bullets.clear()
            self.powerups.clear()

    def draw(self, screen):
        self.player.draw(screen)
        for p in self.powerups:    p.draw(screen)
        for b in self.player_bullets: b.draw(screen)
        for b in self.enemy_bullets:  b.draw(screen)
        for a in self.aliens:      a.draw(screen)
        for e in self.explosions:  e.draw(screen)
        
        if self.paused:
            pt = self.game.large_font.render("PAUSED", True, YELLOW)
            screen.blit(pt, (SCREEN_WIDTH // 2 - pt.get_width() // 2, SCREEN_HEIGHT // 2))

        screen.blit(self.game.font.render(f"Score: {self.score}",   True, WHITE), (10, 10))
        wt = self.game.font.render(f"Wave: {self.wave}", True, WHITE)
        screen.blit(wt, (SCREEN_WIDTH // 2 - wt.get_width() // 2, 10))
        lt = self.game.font.render(f"Lives: {self.player.lives}", True, WHITE)
        screen.blit(lt, (SCREEN_WIDTH - lt.get_width() - 10, 10))
        ht = self.game.font.render(f"Best: {self.game.highscore}", True, YELLOW)
        screen.blit(ht, (SCREEN_WIDTH - ht.get_width() - 10, 40))

        if self.player.double_shot:
            t = self.game.font.render("DOUBLE SHOT!", True, CYAN)
            screen.blit(t, (SCREEN_WIDTH // 2 - t.get_width() // 2, SCREEN_HEIGHT - 30))
        elif self.player.pierce_shot:
            t = self.game.font.render("PIERCING SHOT!", True, PURPLE)
            screen.blit(t, (SCREEN_WIDTH // 2 - t.get_width() // 2, SCREEN_HEIGHT - 30))
