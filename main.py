import pygame
from sys import exit
import display_option


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - star_time
    """put code above on the surface"""
    score_surf = text_found.render(f'Score : {current_time}', False, (64, 64, 64))
    """crate rect"""
    score_rect = score_surf.get_rect(center=(400, 50))
    """show score"""
    screen.blit(score_surf, score_rect)


"""Start pygame and all of his elements like render etc."""
pygame.init()

"""set width and high"""
screen = pygame.display.set_mode((display_option.screen_resolution))
pygame.display.set_caption(display_option.game_title)
clock = pygame.time.Clock()

# EXAMPLE
"""Test Found"""
"""Font type and font size"""
text_found = pygame.font.Font('game_gallery/font/Pixeltype.ttf', 50)

"""set width and high"""
# EXAMPLE
# test_surface = pygame.Surface((100, 200))
# test_surface.fill('Red')

"""all elements"""
"""all updates"""
"""Regular surface (image) on display on Display surface"""

# Surface
sky_surface = pygame.image.load('game_gallery/graphics/Sky.png').convert()
ground_surface = pygame.image.load('game_gallery/graphics/ground.png').convert()

text_surface = text_found.render("Game Over", False, 'Gold')
text_rect = text_surface.get_rect(center=(400, 50))

# Snails
snail_surface = pygame.image.load('game_gallery/graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surface.get_rect(midbottom=(600, 300))

snail_rect_2 = snail_surface.get_rect(midbottom=(500, 200))
snail_surface_2 = pygame.image.load('game_gallery/graphics/snail/snail1.png').convert_alpha()

# Player
player_surf = pygame.image.load("game_gallery/graphics/Player/player_walk_1.png").convert_alpha()
player_rect = player_surf.get_rect(midbottom=(80, 300))

# intro screen
player_stand = pygame.image.load('game_gallery/graphics/Player/player_stand.png')
"Resize img"
player_stand_scale = pygame.transform.scale(player_stand, (200, 400))
player_stand_rect = player_stand_scale.get_rect(center=(400, 200))

star_time = 0
player_gravity = 0

game_active = True
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            """fallow the  mouse coridants"""
            if event.type == pygame.MOUSEMOTION:
                print(event.pos)
            if event.type == pygame.MOUSEBUTTONDOWN:
                print('mouse down')
                if player_rect.collidepoint(event.pos):
                    player_gravity = -20

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -20
                    print("jump")

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player_rect.x += 20
                    print("right")

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_rect.x -= 20
                    print("left")
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                snail_rect.left = 800
                player_rect.right = 80
                star_time = int(pygame.time.get_ticks() / 1000)
    # Game
    if game_active:
        if game_active:
            screen.blit(sky_surface, (0, 0))
            screen.blit(ground_surface, (0, 300))
            # screen.blit(text_surface, text_rect)
            display_score()

            # snail_rect_2.x -= 3
            if snail_rect_2.right <= 0: snail_rect_2.left = 800
            screen.blit(snail_surface_2, snail_rect_2)

            snail_rect.x -= 5
            if snail_rect.right <= 0: snail_rect.left = 800
            screen.blit(snail_surface, snail_rect)

            # Player
            player_gravity += 1
            player_rect.y += player_gravity

            """Gravity STOP point"""
            if player_rect.bottom >= 300:
                player_rect.bottom = 300

            """Nie rozumiem"""
            if player_rect.top <= 0: player_rect.top = 0
            screen.blit(player_surf, player_rect)

            if snail_rect.colliderect(player_rect) or snail_rect_2.colliderect(player_rect):
                print("Game Over")
                game_active = False
    # Intro
    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand_scale, player_stand_rect)
        screen.blit(text_surface, text_rect)
    pygame.display.update()
    """loop can not run faster then 60 time per second"""
    clock.tick(60)
