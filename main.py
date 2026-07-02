import pygame
import sys
import random
import os
from player import Player
from bullet import Bullet
from alien import Alien, BossAlien
from powerup import PowerUp
from explosion import Explosion
from sounds import (make_shoot_sound, make_explosion_sound,
                    make_powerup_sound, make_boss_hit_sound, make_hit_sound)

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")

# Colors
BLACK  = (0, 0, 0)
WHITE  = (255, 255, 255)
YELLOW = (255, 255, 0)
GRAY   = (150, 150, 150)
PURPLE = (255, 0, 255)
RED    = (255, 0, 0)
BLUE   = (0, 100, 255)
CYAN   = (0, 255, 255)

# Fonts
font       = pygame.font.SysFont(None, 36)
large_font = pygame.font.SysFont(None, 72)
title_font = pygame.font.SysFont(None, 96)

# Frame rate
clock = pygame.time.Clock()
FPS = 60

# High-score file
HIGHSCORE_FILE = "highscore.txt"

def load_highscore():
    if os.path.exists(HIGHSCORE_FILE):
        try:
            with open(HIGHSCORE_FILE, "r") as f:
                return int(f.read().strip())
        except:
            pass
    return 0

def save_highscore(score):
    with open(HIGHSCORE_FILE, "w") as f:
        f.write(str(score))

# Starfield
stars = []
for _ in range(120):
    stars.append([random.randint(0, SCREEN_WIDTH),
                  random.randint(0, SCREEN_HEIGHT),
                  random.uniform(0.5, 2.0)])

def update_stars():
    for star in stars:
        star[1] += star[2]
        if star[1] > SCREEN_HEIGHT:
            star[1] = 0
            star[0] = random.randint(0, SCREEN_WIDTH)

def draw_stars():
    for star in stars:
        pygame.draw.circle(screen, GRAY, (int(star[0]), int(star[1])), 2)

# ── helpers ──────────────────────────────────────────────────────────────────

def create_aliens(rows, cols):
    aliens = []
    for row in range(rows):
        for col in range(cols):
            aliens.append(Alien(100 + col * 60, 50 + row * 60))
    return aliens

def create_boss(wave):
    hp = 20 + (wave // 3 - 1) * 10
    return [BossAlien(SCREEN_WIDTH // 2 - 75, 50, hp)]

def take_damage(player, snd_hit):
    if player.shield_active:
        player.shield_active = False
        snd_hit.play()
        return False
    else:
        player.lives -= 1
        snd_hit.play()
        return player.lives <= 0

def spawn_powerup(x, y, wave):
    types = ['double', 'double', 'pierce', 'life']
    if wave >= 4:
        types.extend(['shield', 'shield'])
    return PowerUp(x, y, random.choice(types))

# ── MENU ──────────────────────────────────────────────────────────────────────

def show_menu(highscore):
    blink_timer = 0
    show_prompt = True
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return  # start game

        update_stars()
        screen.fill(BLACK)
        draw_stars()

        # Title
        title = title_font.render("SPACE", True, CYAN)
        title2 = title_font.render("INVADERS", True, YELLOW)
        screen.blit(title,  (SCREEN_WIDTH // 2 - title.get_width()  // 2, 140))
        screen.blit(title2, (SCREEN_WIDTH // 2 - title2.get_width() // 2, 220))

        # High score
        hs_text = font.render(f"High Score: {highscore}", True, WHITE)
        screen.blit(hs_text, (SCREEN_WIDTH // 2 - hs_text.get_width() // 2, 330))

        # Blinking prompt
        blink_timer += 1
        if blink_timer >= 30:
            show_prompt = not show_prompt
            blink_timer = 0
        if show_prompt:
            prompt = font.render("Press SPACE to Play", True, WHITE)
            screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, 400))

        # Controls hint
        ctrl = font.render("← → to move  |  SPACE to shoot", True, GRAY)
        screen.blit(ctrl, (SCREEN_WIDTH // 2 - ctrl.get_width() // 2, 480))

        pygame.display.flip()
        clock.tick(FPS)

# ── GAME OVER SCREEN ──────────────────────────────────────────────────────────

def show_game_over(score, highscore):
    timer = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

        update_stars()
        screen.fill(BLACK)
        draw_stars()

        go = large_font.render("GAME OVER", True, RED)
        screen.blit(go, (SCREEN_WIDTH // 2 - go.get_width() // 2, 160))

        sc = font.render(f"Score: {score}", True, WHITE)
        screen.blit(sc, (SCREEN_WIDTH // 2 - sc.get_width() // 2, 260))

        hs_color = YELLOW if score >= highscore else WHITE
        hs = font.render(f"High Score: {highscore}", True, hs_color)
        screen.blit(hs, (SCREEN_WIDTH // 2 - hs.get_width() // 2, 300))

        if score >= highscore:
            new_rec = font.render("★ NEW RECORD! ★", True, YELLOW)
            screen.blit(new_rec, (SCREEN_WIDTH // 2 - new_rec.get_width() // 2, 350))

        timer += 1
        if timer > 90:
            prompt = font.render("Press SPACE to Play Again", True, WHITE)
            screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, 430))

        pygame.display.flip()
        clock.tick(FPS)

# ── MAIN GAME ─────────────────────────────────────────────────────────────────

def game_loop(highscore):
    # Load sounds
    snd_shoot    = make_shoot_sound()
    snd_explode  = make_explosion_sound()
    snd_powerup  = make_powerup_sound()
    snd_boss_hit = make_boss_hit_sound()
    snd_hit      = make_hit_sound()

    player         = Player(SCREEN_WIDTH, SCREEN_HEIGHT)
    player_bullets = []
    enemy_bullets  = []
    powerups       = []
    explosions     = []

    wave             = 1
    base_speed       = 2.0
    alien_speed_x    = base_speed
    alien_drop       = 20
    aliens           = create_aliens(5, 10)
    is_boss_wave     = False
    boss_hits_taken  = 0
    score            = 0
    game_over        = False
    paused           = False

    while True:
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_ESCAPE:
                    return highscore # Return to main menu
                elif event.key == pygame.K_p:
                    paused = not paused
                elif event.key == pygame.K_SPACE and len(player_bullets) < 5 and not paused:
                    if player.double_shot:
                        for bx in [player.rect.left, player.rect.right - 5]:
                            player_bullets.append(Bullet(bx, player.rect.top, -7, YELLOW))
                    elif player.pierce_shot:
                        player_bullets.append(Bullet(player.rect.centerx - 5, player.rect.top,
                                                      -7, PURPLE, piercing=True))
                    else:
                        player_bullets.append(Bullet(player.rect.centerx - 2, player.rect.top, -7, YELLOW))
                    snd_shoot.play()

        if not game_over and not paused:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:  player.move_left()
            if keys[pygame.K_RIGHT]: player.move_right()
            player.update()

            # Player bullets
            for b in player_bullets[:]:
                b.update()
                if b.rect.bottom < 0:
                    player_bullets.remove(b)

            # Enemy bullets
            for b in enemy_bullets[:]:
                b.update()
                if b.rect.top > SCREEN_HEIGHT:
                    enemy_bullets.remove(b)
                elif b.rect.colliderect(player.rect):
                    enemy_bullets.remove(b)
                    if take_damage(player, snd_hit):
                        game_over = True

            # Power-ups
            for p in powerups[:]:
                p.update()
                if p.rect.colliderect(player.rect):
                    if p.type == 'double':   player.activate_double_shot(FPS * 10)
                    elif p.type == 'pierce': player.activate_pierce_shot(FPS * 5)
                    elif p.type == 'life':   player.lives += 1
                    elif p.type == 'shield': player.activate_shield()
                    powerups.remove(p)
                    score += 50
                    snd_powerup.play()
                elif p.rect.top > SCREEN_HEIGHT:
                    powerups.remove(p)

            # Move aliens horizontally first
            for a in aliens:
                a.update(alien_speed_x, 0)
                if is_boss_wave and random.random() < 0.025:
                    enemy_bullets.append(Bullet(a.rect.centerx - 2, a.rect.bottom, 5, RED, is_enemy=True))

            # Check wall AFTER moving, so we drop only once per bounce
            hit_wall = any(
                a.rect.right > SCREEN_WIDTH or a.rect.left < 0
                for a in aliens
            )

            if hit_wall:
                alien_speed_x *= -1
                # Clip aliens back inside screen before dropping
                for a in aliens:
                    if a.rect.right > SCREEN_WIDTH:
                        a.rect.right = SCREEN_WIDTH
                    elif a.rect.left < 0:
                        a.rect.left = 0
                # Now drop them down
                for a in aliens:
                    a.update(0, alien_drop)
                    if a.rect.bottom >= player.rect.top:
                        if take_damage(player, snd_hit):
                            game_over = True
                        else:
                            if is_boss_wave:
                                hp = a.hp
                                aliens = create_boss(wave)
                                aliens[0].hp = hp
                                alien_speed_x = (base_speed * 1.5) * (1 if alien_speed_x > 0 else -1)
                            else:
                                aliens = create_aliens(5, 10)
                                alien_speed_x = base_speed * (1 if alien_speed_x > 0 else -1)
                            enemy_bullets.clear()
                        break

            # Bullet-alien collisions
            if not game_over:
                for b in player_bullets[:]:
                    for a in aliens[:]:
                        if b.rect.colliderect(a.rect):
                            if is_boss_wave:
                                a.hp -= 1
                                boss_hits_taken += 1
                                snd_boss_hit.play()
                                explosions.append(Explosion(a.rect.centerx, a.rect.centery, (255, 165, 0)))
                                if boss_hits_taken % 5 == 0:
                                    powerups.append(spawn_powerup(a.rect.centerx, a.rect.bottom, wave))
                                if a.hp <= 0:
                                    explosions.append(Explosion(a.rect.centerx, a.rect.centery, (255, 80, 0)))
                                    aliens.remove(a)
                                    score += 500
                            else:
                                explosions.append(Explosion(a.rect.centerx, a.rect.centery))
                                aliens.remove(a)
                                score += 10
                                snd_explode.play()
                                if random.random() < 0.15:
                                    powerups.append(spawn_powerup(a.rect.centerx, a.rect.centery, wave))

                            if not b.piercing or is_boss_wave:
                                if b in player_bullets:
                                    player_bullets.remove(b)
                                break

            # Explosions
            for e in explosions[:]:
                e.update()
                if e.done:
                    explosions.remove(e)

            # Next wave
            if not aliens and not game_over:
                wave += 1
                base_speed += 0.5
                if wave % 3 == 0:
                    is_boss_wave    = True
                    boss_hits_taken = 0
                    aliens          = create_boss(wave)
                    alien_speed_x   = base_speed * 1.5
                else:
                    is_boss_wave  = False
                    aliens        = create_aliens(5, 10)
                    alien_speed_x = base_speed
                player_bullets.clear()
                enemy_bullets.clear()
                powerups.clear()

        # ── DRAW ──────────────────────────────────────────────────────────────
        update_stars()
        screen.fill(BLACK)
        draw_stars()

        if game_over:
            # Update highscore
            if score > highscore:
                highscore = score
                save_highscore(highscore)
            show_game_over(score, highscore)
            return highscore

        player.draw(screen)
        for p in powerups:    p.draw(screen)
        for b in player_bullets: b.draw(screen)
        for b in enemy_bullets:  b.draw(screen)
        for a in aliens:      a.draw(screen)
        for e in explosions:  e.draw(screen)
        
        if paused:
            pt = large_font.render("PAUSED", True, YELLOW)
            screen.blit(pt, (SCREEN_WIDTH // 2 - pt.get_width() // 2, SCREEN_HEIGHT // 2))

        # UI
        screen.blit(font.render(f"Score: {score}",   True, WHITE), (10, 10))
        wt = font.render(f"Wave: {wave}", True, WHITE)
        screen.blit(wt, (SCREEN_WIDTH // 2 - wt.get_width() // 2, 10))
        lt = font.render(f"Lives: {player.lives}", True, WHITE)
        screen.blit(lt, (SCREEN_WIDTH - lt.get_width() - 10, 10))
        ht = font.render(f"Best: {highscore}", True, YELLOW)
        screen.blit(ht, (SCREEN_WIDTH - ht.get_width() - 10, 40))

        if player.double_shot:
            t = font.render("DOUBLE SHOT!", True, CYAN)
            screen.blit(t, (SCREEN_WIDTH // 2 - t.get_width() // 2, SCREEN_HEIGHT - 30))
        elif player.pierce_shot:
            t = font.render("PIERCING SHOT!", True, PURPLE)
            screen.blit(t, (SCREEN_WIDTH // 2 - t.get_width() // 2, SCREEN_HEIGHT - 30))

        pygame.display.flip()
        clock.tick(FPS)

# ── ENTRY POINT ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    highscore = load_highscore()
    while True:
        show_menu(highscore)
        highscore = game_loop(highscore)
