import random

import pygame
from sys import exit
from random import randint
import display_option


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            if obstacle_rect.bottom == 300:
                obstacle_rect.x -= 5
                screen.blit(snail_surface, obstacle_rect)
            else:
                obstacle_rect.x -= 7
                screen.blit(fly_surface, obstacle_rect)
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else:
        return []


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - star_time
    score_surf = text_font.render(f'Score : {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time


def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True


def player_animation():
    global player_surf, player_index
    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk): player_index = 0
        player_surf = player_walk[int(player_index)]


pygame.init()

screen = pygame.display.set_mode(display_option.screen_resolution)
pygame.display.set_caption(display_option.game_title)

clock = pygame.time.Clock()

text_font = pygame.font.Font('game_gallery/font/Pixeltype.ttf', 50)

sky_surface = pygame.image.load('game_gallery/graphics/Sky.png').convert()
ground_surface = pygame.image.load('game_gallery/graphics/ground.png').convert()

game_title_text_surf = text_font.render("Little Runer", False, 'Gold')
game_title_text_rect = game_title_text_surf.get_rect(center=(400, 50))

end_game_text_surf = text_font.render("Game Over", False, 'Gold')
end_game_text_rect = end_game_text_surf.get_rect(center=(400, 50))

start_text_surface = text_font.render("To start the game pres space", False, 'Gold')
start_text_rect = start_text_surface.get_rect(center=(400, 80))

obstacle_rect_list = []

snail_frame_1 = pygame.image.load('game_gallery/graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('game_gallery/graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_frame_index = 0
snail_surface = snail_frames[snail_frame_frame_index]

fly_frame_1 = pygame.image.load('game_gallery/graphics/Fly/Fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('game_gallery/graphics/Fly/Fly2.png').convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surface = fly_frames[fly_frame_index]

player_walk_1 = pygame.image.load("game_gallery/graphics/Player/player_walk_1.png").convert_alpha()
player_walk_2 = pygame.image.load("game_gallery/graphics/Player/player_walk_2.png").convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load("game_gallery/graphics/Player/jump.png").convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_walk_1.get_rect(midbottom=(80, 300))
player_gravity = 0

player_stand = pygame.image.load('game_gallery/graphics/Player/player_stand.png').convert_alpha()
player_stand_scale = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand_scale.get_rect(center=(400, 200))

star_time = 0
score = 0

game_active = False

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 2000)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 300)

jump_sound = pygame.mixer.Sound('game_gallery/audio/jump.mp3')
jump_sound.set_volume(0.1)
bg_music = pygame.mixer.Sound('game_gallery/audio/music.wav')

bg_music.play(loops=-1)
bg_music.set_volume(0.1)
bg_music.play()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -20
                    jump_sound.play()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player_rect.x += 20

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_rect.x -= 20
            if game_active:
                if event.type == obstacle_timer:
                    if randint(0, 2):
                        obstacle_rect_list.append(snail_surface.get_rect(bottomright=(random.randint(900, 1100), 300)))
                    else:
                        obstacle_rect_list.append(fly_surface.get_rect(bottomright=(random.randint(900, 1100), 210)))

                if event.type == snail_animation_timer:
                    if snail_frame_frame_index == 0:
                        snail_frame_frame_index = 1
                    else:
                        snail_frame_frame_index = 0
                    snail_surface = snail_frames[snail_frame_frame_index]

                if event.type == fly_animation_timer:
                    if fly_frame_index == 0:
                        fly_frame_index = 1
                    else:
                        fly_frame_index = 0
                    fly_surface = fly_frames[fly_frame_index]

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                player_rect.right = 80
                star_time = int(pygame.time.get_ticks() / 1000)

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
        if player_rect.bottom >= 300: player_rect.bottom = 300
        player_animation()
        screen.blit(player_surf, player_rect)

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand_scale, player_stand_rect)
        obstacle_rect_list.clear()

        player_rect.midbottom = (80, 300)
        player_gravity = 0

        score_message = text_font.render(f'yours score is {score}', False, "Gold")
        score_message_rect = score_message.get_rect(center=(400, 330))

        if score == 0:
            screen.blit(game_title_text_surf, game_title_text_rect)
            screen.blit(start_text_surface, start_text_rect)

        else:
            screen.blit(end_game_text_surf, end_game_text_rect)
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)
