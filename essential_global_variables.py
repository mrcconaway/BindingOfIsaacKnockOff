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

# initialize variables for loop
player_shields       = 0
bubbles_hit_tick     = 0
player_hit_tick      = 0
times_bubbles_killed = 0
total_num_of_ticks   = 0
the_game_is_running  = True

previous_player_pos  = [player_pos[0] , player_pos[1] ]
previous_bubbles_pos = [bubbles_pos[0], bubbles_pos[1]]