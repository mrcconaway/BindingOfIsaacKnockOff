"""
Created on Thu Feb 16 08:16:11 2023

"""

# testing change

import time
import sys
import math
# import numpy as np
import random
import pygame
from pygame.locals import *



pygame.init()
print("\n"*5)  # this is a spacer to make it easier to troubleshoot error messages

# define pygame things and essential global things
SIZE = WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode(SIZE)

TROUBLESHOOTING = False  # determines if print statements will occur after set amount of frames

FPS   = 30
clock = pygame.time.Clock()
dt    = clock.tick(FPS)

SPEED_CORRECTION      = 1 / math.sqrt(2)
PLAYER_SPEED          = 300
player_speed_variable = 0

BUBBLES_SPEED = PLAYER_SPEED / 2
BUBBLES_COOLDOWN  = 0 # number of ticks that bubbles is immune after respawning

BULLET_SPEED       = 500
BULLET_SIZE        = 15        # x y height of box of bullet
BULLETS_PER_SECOND = 5
BULLET_COOLDOWN    = FPS // BULLETS_PER_SECOND
bullet_shot_at     = 0         # tracks when bullet is shot in terms of ticks
bullet_shotQ       = False     # tracks to see if a bullet was shot (so you can't spam in multiple directions)
def generate_bullet():
    return pygame.Rect(
                       player_pos[0] + pygame.Surface.get_width(player)  / 2, 
                       player_pos[1] + pygame.Surface.get_height(player) / 2, 
                       BULLET_SIZE, BULLET_SIZE
                       )

# all_of_the_bullets will store each bullet as a list of length 2 in the format:
#          all_of_the_bullets = [ [bullet_rect_object, "bullet_direction"] ]
# example: all_of_the_bullets = [ [bullet_rect, "E"], [bullet_rect, "NW"], [bullet_rect, "SE"], [bullet_rect, "S"] ]
all_of_the_bullets = []

# define lots of colors
BLACK   = (0,   0,   0)
GRAY    = (127, 127, 127)
WHITE   = (255, 255, 255)
RED     = (255, 0,   0)
GREEN   = (0,   255, 0)
BLUE    = (0,   0,   255)
YELLOW  = (255, 255, 0)
CYAN    = (0,   255, 255)
MAGENTA = (255, 0,   255)


player           = pygame.image.load("resources/moon_50x50.png").convert()
player_pos       = [WIDTH / 2, HEIGHT / 2]
player_rectangle = pygame.Rect(
                               player_pos[0],
                               player_pos[1],
                               50,
                               50
                               )

bubbles           = pygame.image.load("resources/Bubbles_50x50.png").convert()
bubbles_pos       = [WIDTH * random.random(), HEIGHT * random.random()]
bubbles_rectangle = pygame.Rect(
                               bubbles_pos[0],
                               bubbles_pos[1],
                               50,
                               50
                               )


previous_player_pos  = [player_pos[0],  player_pos[1] ]
previous_bubbles_pos = [bubbles_pos[0], bubbles_pos[1]]
bubbles_hit_tick     = 0
total_num_of_ticks   = 0
the_game_is_running  = True
times_bubbles_killed = 0
while the_game_is_running:
    bullet_shotQ = False
    player_out_of_bounds_x = False
    player_out_of_bounds_y = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            the_game_is_running = False

    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_ESCAPE]:
        the_game_is_running = False
    


    if total_num_of_ticks > (bubbles_hit_tick + BUBBLES_COOLDOWN):
        for b in all_of_the_bullets:
            remove_index = -1
            this_bullet = b[0]
            if pygame.Rect.colliderect(bubbles_rectangle, this_bullet):
                # print("bubbles it hit")
                remove_index = b
                bubbles_pos[0] = WIDTH  * random.random()
                bubbles_pos[1] = HEIGHT * random.random()
                bubbles_hit_tick = total_num_of_ticks
                times_bubbles_killed += 1
            if (remove_index != -1):
                all_of_the_bullets.remove(remove_index)
                

    else:
        # print("bubbles currently immune")
        None

    if pygame.Rect.colliderect(bubbles_rectangle, player_rectangle):
        # print("you're getting hit!")
        the_game_is_running = False


    # player movement
    # start jank
    correct_speed = False
    if (pressed_keys[pygame.K_w] and pressed_keys[pygame.K_a]) or (pressed_keys[pygame.K_w] and pressed_keys[pygame.K_d]) or (pressed_keys[pygame.K_s] and pressed_keys[pygame.K_a]) or (pressed_keys[pygame.K_s] and pressed_keys[pygame.K_d]):
        correct_speed = True
    # end jank
    adjust_player_speed_by = (correct_speed * SPEED_CORRECTION + 1*(not correct_speed)) * PLAYER_SPEED // dt
    if (player_pos[0] < 0):
        player_out_of_bounds_x = True
        player_pos[0] = 1
    if (player_pos[0] > WIDTH - pygame.Surface.get_width(player)):
        player_out_of_bounds_x = True
        player_pos[0] = WIDTH - pygame.Surface.get_width(player) - 1
    if (player_pos[1] < 0):
        player_out_of_bounds_y = True
        player_pos[1] = 1
    if (player_pos[1] > HEIGHT - pygame.Surface.get_height(player)):
        player_out_of_bounds_y = True
        player_pos[1] = HEIGHT - pygame.Surface.get_height(player) - 1
    if pressed_keys[pygame.K_w]:
        player_pos[1] -= adjust_player_speed_by * (1 - player_out_of_bounds_y)
    if pressed_keys[pygame.K_s]:
        player_pos[1] += adjust_player_speed_by * (1 - player_out_of_bounds_y)
    if pressed_keys[pygame.K_a]:
        player_pos[0] -= adjust_player_speed_by * (1 - player_out_of_bounds_x)
    if pressed_keys[pygame.K_d]:
        player_pos[0] += adjust_player_speed_by * (1 - player_out_of_bounds_x)
    

    # bullet stuff
    if total_num_of_ticks > (bullet_shot_at + BULLET_COOLDOWN):
        if (pressed_keys[pygame.K_UP] and pressed_keys[pygame.K_RIGHT]) and not bullet_shotQ:
            direction    = "NE"
            bullet_shotQ = True
        if (pressed_keys[pygame.K_UP] and pressed_keys[pygame.K_LEFT]) and not bullet_shotQ:
            direction    = "NW"
            bullet_shotQ = True
        if (pressed_keys[pygame.K_DOWN] and pressed_keys[pygame.K_RIGHT]) and not bullet_shotQ:
            direction    = "SE"
            bullet_shotQ = True
        if (pressed_keys[pygame.K_DOWN] and pressed_keys[pygame.K_LEFT]) and not bullet_shotQ:
            direction    = "SW"
            bullet_shotQ = True
        if pressed_keys[pygame.K_UP] and not bullet_shotQ:
            direction    = "N"
            bullet_shotQ = True
        if pressed_keys[pygame.K_DOWN] and not bullet_shotQ:
            direction    = "S"
            bullet_shotQ = True
        if pressed_keys[pygame.K_RIGHT] and not bullet_shotQ:
            direction    = "E"
            bullet_shotQ = True
        if pressed_keys[pygame.K_LEFT] and not bullet_shotQ:
            direction    = "W"
            bullet_shotQ = True
        if bullet_shotQ:
            bullet_shot_at = total_num_of_ticks
            all_of_the_bullets.append([generate_bullet(), direction])

    # stuff for bubbles
    # the "< 5" bit here was picked arbitrarily because it seemed to work to get rid of bubble's jitteryness
    if (abs(bubbles_pos[0] - player_pos[0]) < 5) and (abs(bubbles_pos[1] - player_pos[1]) < 5):
        bubbles_pos[0] = player_pos[0]
        bubbles_pos[1] = player_pos[1]
    else:
        adjust_bubbles_x = 0
        adjust_bubbles_y = 0
        if bubbles_pos[0] < player_pos[0]:
            adjust_bubbles_x += BUBBLES_SPEED // dt
        if bubbles_pos[0] > player_pos[0]:
            adjust_bubbles_x -= BUBBLES_SPEED // dt
        if bubbles_pos[1] < player_pos[1]:
            adjust_bubbles_y += BUBBLES_SPEED // dt
        if bubbles_pos[1] > player_pos[1]:
            adjust_bubbles_y -= BUBBLES_SPEED // dt
        
        if (adjust_bubbles_x != 0) and (adjust_bubbles_y != 0):
            bubbles_pos[0] += SPEED_CORRECTION * adjust_bubbles_x // 1
            bubbles_pos[1] += SPEED_CORRECTION * adjust_bubbles_y // 1
        else:
            bubbles_pos[0] += adjust_bubbles_x
            bubbles_pos[1] += adjust_bubbles_y


    # try and fix player_rect and bubbles_rect here
    if previous_player_pos == player_pos:
        player_rectangle  = pygame.Rect.move(player_rectangle, 0, 0)
    else:
        player_rectangle  = pygame.Rect.move(
                                             player_rectangle, 
                                             (player_pos[0] - previous_player_pos[0]), 
                                             (player_pos[1] - previous_player_pos[1])
                                             )
    if previous_bubbles_pos == bubbles_pos:
        bubbles_rectangle = pygame.Rect.move(bubbles_rectangle, 0, 0)
    else:
        bubbles_rectangle = pygame.Rect.move(
                                             bubbles_rectangle, 
                                             bubbles_pos[0] - previous_bubbles_pos[0], 
                                             bubbles_pos[1] - previous_bubbles_pos[1])
    # pygame.draw.rect(screen, BLUE,   player_rectangle )
    # pygame.draw.rect(screen, YELLOW, bubbles_rectangle)

    # screen stuff
    screen.fill(BLACK)
    screen.blit(player, player_pos)
    screen.blit(bubbles, bubbles_pos)
    # pygame.draw.rect(screen, BLUE,   player_rectangle )
    # pygame.draw.rect(screen, YELLOW, bubbles_rectangle)

    for this_bullet in all_of_the_bullets:
        if (this_bullet[0].centerx <= 0) or (this_bullet[0].centerx >= WIDTH) or (this_bullet[0].centery <= 0) or (this_bullet[0].centery >= HEIGHT):
            all_of_the_bullets.remove(this_bullet)
        # if (this_bullet[0].centerx == bubbles_pos[0]) and (this_bullet[0].centery == bubbles_pos[0]):
        #     all_of_the_bullets.remove(this_bullet)
        # if pygame.Rect.colliderect(bubbles_rectangle, player_rectangle):
        #     all_of_the_bullets.remove(this_bullet)


    
    for i in range(len(all_of_the_bullets)):
        if all_of_the_bullets[i][1] == "N":
            all_of_the_bullets[i][0] = pygame.Rect.move(all_of_the_bullets[i][0], 0, -BULLET_SPEED / dt)
        if all_of_the_bullets[i][1] == "S":
            all_of_the_bullets[i][0] = pygame.Rect.move(all_of_the_bullets[i][0], 0,  BULLET_SPEED / dt)
        if all_of_the_bullets[i][1] == "E":
            all_of_the_bullets[i][0] = pygame.Rect.move(all_of_the_bullets[i][0],  BULLET_SPEED / dt, 0)
        if all_of_the_bullets[i][1] == "W":
            all_of_the_bullets[i][0] = pygame.Rect.move(all_of_the_bullets[i][0], -BULLET_SPEED / dt, 0)
        if all_of_the_bullets[i][1] == "NW":
            all_of_the_bullets[i][0] = pygame.Rect.move(all_of_the_bullets[i][0], -SPEED_CORRECTION * BULLET_SPEED / dt, -SPEED_CORRECTION * BULLET_SPEED / dt)
        if all_of_the_bullets[i][1] == "NE":
            all_of_the_bullets[i][0] = pygame.Rect.move(all_of_the_bullets[i][0],  SPEED_CORRECTION * BULLET_SPEED / dt, -SPEED_CORRECTION * BULLET_SPEED / dt)
        if all_of_the_bullets[i][1] == "SW":
            all_of_the_bullets[i][0] = pygame.Rect.move(all_of_the_bullets[i][0], -SPEED_CORRECTION * BULLET_SPEED / dt,  SPEED_CORRECTION * BULLET_SPEED / dt)
        if all_of_the_bullets[i][1] == "SE":
            all_of_the_bullets[i][0] = pygame.Rect.move(all_of_the_bullets[i][0],  SPEED_CORRECTION * BULLET_SPEED / dt,  SPEED_CORRECTION * BULLET_SPEED / dt)
        
        pygame.draw.rect(screen, RED, all_of_the_bullets[i][0])
    
    pygame.display.update()
    if TROUBLESHOOTING:
        if (total_num_of_ticks % 5 == 0):
            print("player pos = ("+ str(
                                        round(player_pos[0], 4)
                                        )+", "+str(
                                                round(player_pos[1], 4)
                                                ) +")")
            print("previous player pos = ("+ str(
                                        round(previous_player_pos[0], 4)
                                        )+", "+str(
                                                round(previous_player_pos[1], 4)
                                                ) +")")
            print("number of bullets: "+ str(len(all_of_the_bullets)))

    pygame.time.delay(1000//FPS)
    total_num_of_ticks  += 1
    previous_player_pos  = [player_pos[0],  player_pos[1] ]
    previous_bubbles_pos = [bubbles_pos[0], bubbles_pos[1]]
#
print("")
print("")
print("- - - done - - -")
print("")

print("times bubbles killed: "+ str(times_bubbles_killed))