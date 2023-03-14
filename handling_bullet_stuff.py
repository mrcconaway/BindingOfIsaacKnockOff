import pygame
import random

from handling_power_up_stuff    import POWER_UP_DURATION
from entities                   import player
from essential_global_variables import FPS, SPEED_CORRECTION, dt, all_of_the_bullets, all_of_the_lasers
import essential_global_variables
from sfx import *




BULLET_SPEED          = 500
BULLET_SIZE           = 15        # x y height of box of bullet
BULLETS_PER_SECOND    = 5
bullet_boost          = 1
BULLET_COOLDOWN       = FPS // BULLETS_PER_SECOND
bullet_shot_at        = 0         # tracks when bullet is shot in terms of ticks
bullet_shotQ          = False     # tracks to see if a bullet was shot (so you can't spam in multiple directions)
bullet_variability    = 0.1

# # all_of_the_bullets will store each bullet as a list of length 2 in the format:
# #          all_of_the_bullets = [ [bullet_rect_object, "bullet_direction"] ]
# # example: all_of_the_bullets = [ [bullet_rect, "E"], [bullet_rect, "NW"], [bullet_rect, "SE"], [bullet_rect, "S"] ]

# all_of_the_bullets    = []

def generate_bullet(player, player_pos):
    return pygame.Rect(
                       player_pos[0] + 
                                      pygame.Surface.get_width(player)  / 2, 
                       player_pos[1] + 
                                      pygame.Surface.get_height(player) / 2, 
                       BULLET_SIZE, BULLET_SIZE
                       )

def shoot_bullet(the_current_game_state):
    bullet_shotQ       = False
    pressed_keys       = the_current_game_state[0]
    player_pos         = the_current_game_state[1][0]
    total_num_of_ticks = the_current_game_state[3][0]
    bullet_shot_at     = the_current_game_state[3][3]
    triple_shot_tick   = the_current_game_state[3][4]
    timed_laser_tick   = the_current_game_state[3][5]
    all_of_the_lasers  = []


    if pressed_keys[pygame.K_UP] or pressed_keys[pygame.K_DOWN] or pressed_keys[pygame.K_LEFT] or pressed_keys[pygame.K_RIGHT]:
        # bullet stuff
        if (total_num_of_ticks > (bullet_shot_at + BULLET_COOLDOWN / bullet_boost)):
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
            
            # see if a laser is being shot
            if ( timed_laser_tick != 0) and ((timed_laser_tick + POWER_UP_DURATION) > total_num_of_ticks):
                if (triple_shot_tick != 0) and ((triple_shot_tick + POWER_UP_DURATION) > total_num_of_ticks):
                    if direction in VALID_LASER_DIRECTIONS:
                        direction = [direction]
                        # print(VALID_LASER_DIRECTIONS.index( direction[0] ))
                        direction.append( VALID_LASER_DIRECTIONS[ VALID_LASER_DIRECTIONS.index( direction[0] ) - 1 ] )
                        try:
                            direction.append( VALID_LASER_DIRECTIONS[ VALID_LASER_DIRECTIONS.index( direction[0] ) + 1 ] )
                        except:
                            direction.append( VALID_LASER_DIRECTIONS[ 0 ] )
                        for i in range(len(direction)):
                            all_of_the_lasers.append(generate_laser(player, player_pos, direction[i]))
                    shooty(shoot_sound_1)
                else:
                    if direction in VALID_LASER_DIRECTIONS:
                        all_of_the_lasers.append(generate_laser(player, player_pos, direction))
                    shooty(shoot_sound_2)
            # if a laser is not being shot, then shoot bullets instead
            elif bullet_shotQ:
                bullet_shot_at = total_num_of_ticks
                if (triple_shot_tick != 0) and ((triple_shot_tick + POWER_UP_DURATION) > total_num_of_ticks):
                    direction = [direction]
                    direction.append( VALID_SHOT_DIRECTIONS[ VALID_SHOT_DIRECTIONS.index( direction[0] ) - 1 ] )
                    try:
                        direction.append( VALID_SHOT_DIRECTIONS[ VALID_SHOT_DIRECTIONS.index( direction[0] ) + 1 ] )
                    except:
                        direction.append( VALID_SHOT_DIRECTIONS[ 0 ] )
                    for i in range(len(direction)):
                        # print(direction[i])
                        all_of_the_bullets.append([
                                            generate_bullet(player, player_pos), 
                                            direction[i]])
                    shooty(shoot_sound_1)
                else:
                    all_of_the_bullets.append([
                                            generate_bullet(player, player_pos), 
                                            direction])
                    shooty(shoot_sound_2)
    
    return [bullet_shot_at, all_of_the_lasers]

def move_bullets(bullet_list, the_current_game_state):
    camera_pos = the_current_game_state[1][2]
    for i in range(len(bullet_list)):
        if len(bullet_list[i]) == 2:
            # the (2 * random.random() - 1) is stolen from some clever fellow on stack overflow. Its purpose is to generate a random float between -1 and 1
            x_bullet_variability = bullet_variability * (2 * random.random() - 1)
            y_bullet_variability = bullet_variability * (2 * random.random() - 1)

            if bullet_list[i][1] == "N":
                bullet_list[i][0] = pygame.Rect.move(bullet_list[i][0],                            x_bullet_variability * BULLET_SPEED / dt,                                                  -BULLET_SPEED / dt)
            if bullet_list[i][1] == "S":
                bullet_list[i][0] = pygame.Rect.move(bullet_list[i][0],                            x_bullet_variability * BULLET_SPEED / dt,                                                   BULLET_SPEED / dt)
            if bullet_list[i][1] == "E":
                bullet_list[i][0] = pygame.Rect.move(bullet_list[i][0],                                                   BULLET_SPEED / dt,                            y_bullet_variability * BULLET_SPEED / dt)
            if bullet_list[i][1] == "W":
                bullet_list[i][0] = pygame.Rect.move(bullet_list[i][0],                                                 - BULLET_SPEED / dt,                            y_bullet_variability * BULLET_SPEED / dt)
            if bullet_list[i][1] == "NW":
                bullet_list[i][0] = pygame.Rect.move(bullet_list[i][0], - SPEED_CORRECTION * BULLET_SPEED * (1 + x_bullet_variability) / dt, - SPEED_CORRECTION * BULLET_SPEED * (1 + y_bullet_variability) / dt)
            if bullet_list[i][1] == "NE":
                bullet_list[i][0] = pygame.Rect.move(bullet_list[i][0],   SPEED_CORRECTION * BULLET_SPEED * (1 + x_bullet_variability) / dt, - SPEED_CORRECTION * BULLET_SPEED * (1 + y_bullet_variability) / dt)
            if bullet_list[i][1] == "SW":
                bullet_list[i][0] = pygame.Rect.move(bullet_list[i][0], - SPEED_CORRECTION * BULLET_SPEED * (1 + x_bullet_variability) / dt,   SPEED_CORRECTION * BULLET_SPEED * (1 + y_bullet_variability) / dt)
            if bullet_list[i][1] == "SE":
                bullet_list[i][0] = pygame.Rect.move(bullet_list[i][0],   SPEED_CORRECTION * BULLET_SPEED * (1 + x_bullet_variability) / dt,   SPEED_CORRECTION * BULLET_SPEED * (1 + y_bullet_variability) / dt)

            bullet_list[i].append(x_bullet_variability)
            bullet_list[i].append(y_bullet_variability)
        else:
            x_bullet_variability = bullet_list[i][2]
            y_bullet_variability = bullet_list[i][3]

            if bullet_list[i][1] == "N":
                bullet_list[i][0] = pygame.Rect.move(bullet_list[i][0],                            x_bullet_variability * BULLET_SPEED / dt,                                                  -BULLET_SPEED / dt)
            if bullet_list[i][1] == "S":
                bullet_list[i][0] = pygame.Rect.move(bullet_list[i][0],                            x_bullet_variability * BULLET_SPEED / dt,                                                   BULLET_SPEED / dt)
            if bullet_list[i][1] == "E":
                bullet_list[i][0] = pygame.Rect.move(bullet_list[i][0],                                                   BULLET_SPEED / dt,                            y_bullet_variability * BULLET_SPEED / dt)
            if bullet_list[i][1] == "W":
                bullet_list[i][0] = pygame.Rect.move(bullet_list[i][0],                                                 - BULLET_SPEED / dt,                            y_bullet_variability * BULLET_SPEED / dt)
            if bullet_list[i][1] == "NW":
                bullet_list[i][0] = pygame.Rect.move(bullet_list[i][0], - SPEED_CORRECTION * BULLET_SPEED * (1 + x_bullet_variability) / dt, - SPEED_CORRECTION * BULLET_SPEED * (1 + y_bullet_variability) / dt)
            if bullet_list[i][1] == "NE":
                bullet_list[i][0] = pygame.Rect.move(bullet_list[i][0],   SPEED_CORRECTION * BULLET_SPEED * (1 + x_bullet_variability) / dt, - SPEED_CORRECTION * BULLET_SPEED * (1 + y_bullet_variability) / dt)
            if bullet_list[i][1] == "SW":
                bullet_list[i][0] = pygame.Rect.move(bullet_list[i][0], - SPEED_CORRECTION * BULLET_SPEED * (1 + x_bullet_variability) / dt,   SPEED_CORRECTION * BULLET_SPEED * (1 + y_bullet_variability) / dt)
            if bullet_list[i][1] == "SE":
                bullet_list[i][0] = pygame.Rect.move(bullet_list[i][0],   SPEED_CORRECTION * BULLET_SPEED * (1 + x_bullet_variability) / dt,   SPEED_CORRECTION * BULLET_SPEED * (1 + y_bullet_variability) / dt)
    
        # pygame.draw.rect(essential_global_variables.screen, essential_global_variables.RED, all_of_the_bullets[i][0])
        all_of_the_bullets[i][0].x -= camera_pos[0]
        all_of_the_bullets[i][0].y -= camera_pos[1]
        pygame.draw.rect(essential_global_variables.screen, essential_global_variables.RED, all_of_the_bullets[i][0] )


laser_E           = []
laser_N           = []
laser_W           = []
laser_S           = []
# all_of_the_lasers = []
def generate_laser(player, player_pos, direction):
    if direction in VALID_LASER_DIRECTIONS:
        if direction == "E":
            laser = pygame.Rect(
                                (player_pos[0] + pygame.Surface.get_width(player)  / 2),
                                (player_pos[1] + pygame.Surface.get_height(player) / 2), 
                                (essential_global_variables.WIDTH - (player_pos[0] + pygame.Surface.get_width(player) / 2)), BULLET_SIZE
                                )
            laser_E.append(laser)
        if direction == "W":
            laser = pygame.Rect(
                                0,
                                (player_pos[1] + pygame.Surface.get_height(player) / 2), 
                                (player_pos[0] + pygame.Surface.get_width(player)  / 2), BULLET_SIZE
                                )
            laser_W.append(laser)
        if direction == "N":
            laser = pygame.Rect(
                                (player_pos[0] + pygame.Surface.get_width(player)  / 2),
                                0, 
                                BULLET_SIZE, (player_pos[1] + pygame.Surface.get_height(player) / 2)
                                )
            laser_N.append(laser)
        if direction == "S":
            laser = pygame.Rect(
                                (player_pos[0] + pygame.Surface.get_width(player)  / 2),
                                (player_pos[1] + pygame.Surface.get_height(player) / 2), 
                                BULLET_SIZE, essential_global_variables.HEIGHT - player_pos[1] + pygame.Surface.get_width(player) / 2
                                )
            laser_S.append(laser)
        return laser
    else:
        print("not a laser")

VALID_SHOT_DIRECTIONS  = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
VALID_LASER_DIRECTIONS = ["N", "E", "S", "W"]

