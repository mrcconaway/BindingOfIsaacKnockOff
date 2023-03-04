import pygame
import random

import essential_global_variables


POWER_UP_FREQUENCY     = 1 * essential_global_variables.FPS
POWER_UP_INITIAL_WAIT  = 1 * essential_global_variables.FPS
PLAYER_IMMUNITY_TIME   = 1 * essential_global_variables.FPS
POWER_UP_DURATION      = 5 * essential_global_variables.FPS
POWER_UP_TYPES         = ["shield", "bullet_speed", "player_speed", "laser_beam", "triple_shot","bouncy_bullet"]
timed_laser_tick       = 0
triple_shot_tick       = 0
all_of_the_power_ups   = []
# all_of_the_power_ups will store each bullet as a list of length 2 in the format:
#          all_of_the_power_ups = [ [power_up_rect_object, "power_up_type"] ]
# example: all_of_the_power_ups = [ [power_up_rect, "faster_shooting""], [power_up_rect, "extra_bullets"] ]

power_up               = pygame.image.load("resources/shitty_arrow_40x40.png").convert()
bullet_speed_icon      = pygame.image.load("resources/bullet_speed_power_up_40x40.png").convert()
shield_icon            = pygame.image.load("resources/shield_power_up_40x40.png").convert()
speed_boost_icon       = pygame.image.load("resources/player_speed_power_up_40x40.png").convert()
laser_beam_icon        = pygame.image.load("resources/laser_beam_power_up_40x40.png").convert()
triple_shot_icon       = pygame.image.load("resources/triple_shot_power_up_40x40.png").convert()
bouncy_bullet_icon     = pygame.image.load("resources/bouncy_bullet_power_up_40x40.png").convert()
POWER_UP_WIDTH         = pygame.Surface.get_width(power_up)
POWER_UP_HEIGHT        = pygame.Surface.get_height(power_up)
def generate_power_up():
    power_up_pos       = [(essential_global_variables.WIDTH - POWER_UP_WIDTH) * random.random(), (essential_global_variables.HEIGHT - POWER_UP_HEIGHT) * random.random()]
    power_up_rectangle = pygame.Rect(
                                     power_up_pos[0],
                                     power_up_pos[1],
                                     POWER_UP_WIDTH,
                                     POWER_UP_HEIGHT
                                     )
    return power_up_rectangle