import pygame
import math
import random

# from entities import player_pos, bubbles_pos


the_pygame_init = pygame.init()

SIZE   = WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode(SIZE)
FPS    = 30

clock = pygame.time.Clock()
dt    = clock.tick(FPS)

player_pos  = [WIDTH / 2, HEIGHT / 2]
bubbles_pos = [WIDTH * random.random(), HEIGHT * random.random()]

SPEED_CORRECTION = 1 / math.sqrt(2)

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

default_player_health  = 50
default_bubbles_health = 30
bullet_damage  = 10
laser_damage   = 2
bubbles_damage = 25

# all_of_the_bullets will store each bullet as a list of length 2 in the format:
#          all_of_the_bullets = [ [bullet_rect_object, "bullet_direction"] ]
# example: all_of_the_bullets = [ [bullet_rect, "E"], [bullet_rect, "NW"], [bullet_rect, "SE"], [bullet_rect, "S"] ]

all_of_the_bullets    = []
all_of_the_lasers     = []

# initialize variables for loop
player_shields        = 0
bubbles_hit_tick      = 0
player_hit_tick       = 0
times_bubbles_killed  = 0
total_num_of_ticks    = 0
the_game_is_running   = True
bubbles_health        = default_bubbles_health
player_health         = default_player_health
red_box_cooldown      = 2  # amount of ticks that an entity till flash red once hit
bubbles_is_stuck_flag = 0

previous_player_pos  = [player_pos[0] , player_pos[1] ]
previous_bubbles_pos = [bubbles_pos[0], bubbles_pos[1]]