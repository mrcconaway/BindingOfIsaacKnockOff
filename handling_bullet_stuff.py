import pygame
import essential_global_variables



BULLET_SPEED          = 500
BULLET_SIZE           = 15        # x y height of box of bullet
BULLETS_PER_SECOND    = 2
bullet_boost          = 1
BULLET_COOLDOWN       = essential_global_variables.FPS // BULLETS_PER_SECOND
bullet_shot_at        = 0         # tracks when bullet is shot in terms of ticks
bullet_shotQ          = False     # tracks to see if a bullet was shot (so you can't spam in multiple directions)
def generate_bullet(player, player_pos):
    return pygame.Rect(
                       player_pos[0] + 
                                      pygame.Surface.get_width(player)  / 2, 
                       player_pos[1] + 
                                      pygame.Surface.get_height(player) / 2, 
                       BULLET_SIZE, BULLET_SIZE
                       )

laser_E           = []
laser_N           = []
laser_W           = []
laser_S           = []
all_of_the_lasers = []
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


# all_of_the_bullets will store each bullet as a list of length 2 in the format:
#          all_of_the_bullets = [ [bullet_rect_object, "bullet_direction"] ]
# example: all_of_the_bullets = [ [bullet_rect, "E"], [bullet_rect, "NW"], [bullet_rect, "SE"], [bullet_rect, "S"] ]

all_of_the_bullets    = []
