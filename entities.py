import pygame
import random
import numpy as np

import essential_global_variables



# player_pos         = [essential_global_variables.WIDTH / 2, essential_global_variables.HEIGHT / 2]
player = pygame.image.load("resources/moon_50x50.png").convert()
PLAYER_WIDTH          = pygame.Surface.get_width(player)
PLAYER_HEIGHT         = pygame.Surface.get_height(player)
PLAYER_SPEED          = 300
player_speed_variable = 0
player_rectangle      = pygame.Rect(
                                    essential_global_variables.player_pos[0],
                                    essential_global_variables.player_pos[1],
                                    PLAYER_WIDTH,
                                    PLAYER_HEIGHT
                                    )


bubbles           = pygame.image.load("resources/Bubbles_50x50.png").convert()
# bubbles_pos       = [essential_global_variables.WIDTH * random.random(), essential_global_variables.HEIGHT * random.random()]
BUBBLES_WIDTH     = pygame.Surface.get_width(bubbles)
BUBBLES_HEIGHT    = pygame.Surface.get_height(bubbles)
BUBBLES_SPEED     = PLAYER_SPEED / 2
BUBBLES_COOLDOWN  = 0 # number of ticks that bubbles is immune after respawning
bubbles_rectangle = pygame.Rect(
                                essential_global_variables.bubbles_pos[0],
                                essential_global_variables.bubbles_pos[1],
                                BUBBLES_WIDTH,
                                BUBBLES_HEIGHT
                                )

def respawn_bubbles(player_pos):
    # copy/pasted from before
    # print("bubbles it hit")
    respawnX = essential_global_variables.WIDTH  * random.random()
    respawnY = essential_global_variables.HEIGHT * random.random()
    # this should work, might need to fine tune the 
    radius = 6*pygame.Surface.get_width(player)
    while (np.sqrt( (respawnX - player_pos[0])**2 + (respawnY - player_pos[1])**2 ) < radius ):
        respawnX = essential_global_variables.WIDTH  * random.random()
        respawnY = essential_global_variables.HEIGHT * random.random()
        # print("respawning bubbles")
    essential_global_variables.bubbles_pos[0] = respawnX
    essential_global_variables.bubbles_pos[1] = respawnY
    essential_global_variables.bubbles_hit_tick = essential_global_variables.total_num_of_ticks

    bubbles_health = essential_global_variables.default_bubbles_health
    return bubbles_health



def health_bar(entity, entity_pos, entity_current_health, entity_max_health):
    height_above_player = 0.5
    health_fraction     = round(entity_current_health / entity_max_health, 3)
    inflate_bar_size_by = 1 # this kind of looks funky when it's != 1
    health_bar_background = pygame.Rect(
                                        entity_pos[0],
                                        entity_pos[1] - height_above_player * entity.height,
                                        inflate_bar_size_by * entity.width,
                                        10
                                        )
    health_bar_foreground = pygame.Rect(
                                        entity_pos[0],
                                        entity_pos[1] - height_above_player * entity.height,
                                        inflate_bar_size_by * health_fraction * entity.width,
                                        10
                                        )

    pygame.draw.rect(essential_global_variables.screen, 
                     essential_global_variables.WHITE, 
                     health_bar_background)
    pygame.draw.rect(essential_global_variables.screen, 
                     essential_global_variables.RED, 
                     health_bar_foreground)

