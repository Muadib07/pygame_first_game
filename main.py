import random

import pygame
from sys import exit
from random import randint
import display_option


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            screen.blit(snail_surface, obstacle_rect)
        return obstacle_list
    else:
        return []


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - star_time
    score_surf = text_font.render(f'Score : {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time


pygame.init()

screen = pygame.display.set_mode(display_option.screen_resolution)
pygame.display.set_caption(display_option.game_title)

clock = pygame.time.Clock()

# Text font
text_font = pygame.font.Font('game_gallery/font/Pixeltype.ttf', 50)

# Surface
sky_surface = pygame.image.load('game_gallery/graphics/Sky.png').convert()
ground_surface = pygame.image.load('game_gallery/graphics/ground.png').convert()

# Game texts in game
game_title_text_surf = text_font.render("Little Runer", False, 'Gold')
game_title_text_rect = game_title_text_surf.get_rect(center=(400, 50))

end_game_text_surf = text_font.render("Game Over", False, 'Gold')
end_game_text_rect = end_game_text_surf.get_rect(center=(400, 50))

start_text_surface = text_font.render("To start the game pres space", False, 'Gold')
start_text_rect = start_text_surface.get_rect(center=(400, 80))

# obstacles
obstacle_rect_list = []

snail_surface = pygame.image.load('game_gallery/graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surface.get_rect(bottomright=(600, 300))

# Player
player_surf = pygame.image.load("game_gallery/graphics/Player/player_walk_1.png").convert_alpha()
player_rect = player_surf.get_rect(midbottom=(80, 300))

# intro screen
player_stand = pygame.image.load('game_gallery/graphics/Player/player_stand.png').convert_alpha()
player_stand_scale = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand_scale.get_rect(center=(400, 200))

# Global settings
star_time = 0
player_gravity = 0
score = 0

game_active = False

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 2000)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -20

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player_rect.x += 20

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_rect.x -= 20

            if event.type == obstacle_timer:
                obstacle_rect_list.append(snail_surface.get_rect(bottomright=(random.randint(900, 1100), 300)))

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                snail_rect.left = 800
                player_rect.right = 80
                star_time = int(pygame.time.get_ticks() / 1000)
        """The second option to implement a loop of opponents """
        # if event.type == obstacle_timer and game_active:
        # obstacle_rect_list.append(snail_surface.get_rect(bottomright=randint(900, 1100)))

    # Game
    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        score = display_score()

        # obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)


        # Player
        player_gravity += 1
        player_rect.y += player_gravity

        if player_rect.bottom >= 300:
            player_rect.bottom = 300

        if player_rect.top <= 0:
            player_rect.top = 0
        screen.blit(player_surf, player_rect)

        if snail_rect.colliderect(player_rect):
            print("Game Over")
            game_active = False
    # Intro
    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand_scale, player_stand_rect)

        score_message = text_font.render(f'yours score is {score}', False, "Gold")
        score_message_rect = score_message.get_rect(center=(400, 330))

        if score == 0:
            screen.blit(game_title_text_surf, game_title_text_rect)
            screen.blit(start_text_surface, start_text_rect)

        else:
            screen.blit(end_game_text_surf, end_game_text_rect)
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    """loop can not run faster then 60 time per second"""
    clock.tick(60)
