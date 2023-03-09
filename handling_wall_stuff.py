import entities
import pygame

all_of_the_walls = []
def build_wall(wall_x, wall_y, wall_LENGTH, wall_HEIGHT):
    if wall_LENGTH <= entities.PLAYER_WIDTH or wall_HEIGHT <= entities.PLAYER_HEIGHT:
        print("warning!")
        print("walls want to be larger than the player for the logic to work")

    wall_rectangle   = pygame.Rect(
                                   wall_x,
                                   wall_y,
                                   wall_LENGTH,
                                   wall_HEIGHT
                                   )
    all_of_the_walls.append( wall_rectangle )
    return wall_rectangle

def inside_wall(position, width, height):
    for wall in all_of_the_walls:
            if (
                (position[0] < (wall.centerx + wall.width/2 )) and (position[0] > (wall.centerx - wall.width/2 ))    or   (position[0] + width  < (wall.centerx + wall.width/2 )) and (position[0] + width  > (wall.centerx - wall.width/2 ))
                ) and (
                (position[1] < (wall.centery + wall.height/2)) and (position[1] > (wall.centery - wall.height/2))    or   (position[1] + height < (wall.centery + wall.height/2)) and (position[1] + height > (wall.centery - wall.height/2))
                ):
                return True
    return False

def x_inside_wall(position_x, width):
    for wall in all_of_the_walls:
            if (
                (position_x[0] < (wall.centerx + wall.width/2 )) and (position_x[0] > (wall.centerx - wall.width/2 ))    or   (position_x[0] + width  < (wall.centerx + wall.width/2 )) and (position_x[0] + width  > (wall.centerx - wall.width/2 ))
                ):
                return True
    return False

def y_inside_wall(position_y, height):
    for wall in all_of_the_walls:
            if (
                (position_y[1] < (wall.centery + wall.height/2)) and (position_y[1] > (wall.centery - wall.height/2))    or   (position_y[1] + height < (wall.centery + wall.height/2)) and (position_y[1] + height > (wall.centery - wall.height/2))
                ):
                return True
    return False


all_of_the_rocks = []
def place_rock(rock_x, rock_y, rock_LENGTH, rock_HEIGHT, breakable: bool):

    rock_rectangle   = pygame.Rect(
                                   rock_x,
                                   rock_y,
                                   rock_LENGTH,
                                   rock_HEIGHT
                                   )
    all_of_the_rocks.append( [rock_rectangle, breakable] )
    return rock_rectangle


