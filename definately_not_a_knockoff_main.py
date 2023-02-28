"""
Created on Thu Feb 16 08:16:11 2023

"""

# import time
# import sys
import math
import numpy as np
import random
import pygame
from pygame.locals import *



from essential_global_variables import *
from entities                   import *
from handling_power_up_stuff    import *
from handling_bullet_stuff      import *
import sfx


print("\n"*5)  # this is a spacer to make it easier to troubleshoot error messages
TROUBLESHOOTING = False  # determines if print statements will occur after set amount of frames

all_of_the_walls = []
def build_wall(wall_x, wall_y, wall_LENGTH, wall_HEIGHT):
    if wall_LENGTH <= PLAYER_WIDTH or wall_HEIGHT <= PLAYER_HEIGHT:
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

build_wall(WIDTH / 4,  HEIGHT / 4,  50 + 1, HEIGHT / 2)
build_wall(WIDTH-300, HEIGHT-300, 200, 200)

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



player_backup_pos  = []
bubbles_backup_pos = []

### Steven's sound corner

pygame.mixer.init()
short_laser = sfx.get_shooty()

###

while the_game_is_running:
    bullet_shotQ           = False
    player_out_of_bounds_x = False
    player_out_of_bounds_y = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            the_game_is_running = False

    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_ESCAPE]:
        the_game_is_running = False
    
    # hitting bubbles with bullet collisions
    if total_num_of_ticks > (bubbles_hit_tick + BUBBLES_COOLDOWN):
        for b in all_of_the_bullets:
            if pygame.Rect.colliderect(bubbles_rectangle, b[0]):
                # # print("bubbles it hit")
                # respawnX = WIDTH  * random.random()
                # respawnY = HEIGHT * random.random()
                # # this should work, might need to fine tune the 
                # radius = 4*pygame.Surface.get_width(player)
                # while (np.sqrt( (respawnX - player_pos[0])**2 + (respawnY - player_pos[1])**2 ) < radius ):
                #     respawnX = WIDTH  * random.random()
                #     respawnY = HEIGHT * random.random()
                #     # print("respawning bubbles")
                # bubbles_pos[0] = respawnX
                # bubbles_pos[1] = respawnY
                # bubbles_hit_tick = total_num_of_ticks
                # times_bubbles_killed += 1
                respawn_bubbles()
                all_of_the_bullets.remove(b)
    

    for this_laser in all_of_the_lasers:
        # print(type(this_laser))
        if pygame.Rect.colliderect(bubbles_rectangle, this_laser):
            # print("laser hitting bubbles")
            respawn_bubbles()
    all_of_the_lasers = []


    # bubbles-player collision
    if pygame.Rect.colliderect(bubbles_rectangle, player_rectangle) and (total_num_of_ticks > player_hit_tick + PLAYER_IMMUNITY_TIME):
        # print("you're getting hit!")
        if player_shields == 0:
            the_game_is_running = False
        else:
            player_shields -= 1
            player_hit_tick = total_num_of_ticks
        
        print("shields left: "+ str(player_shields))
        print("bubbles has killed you")

    # power up collisions
    for this_power_up in all_of_the_power_ups:
        if pygame.Rect.colliderect(this_power_up[0], player_rectangle):
            print("power up collected!")
            if this_power_up[1] == "shield":
                player_shields += 1
                print("shields: "+ str(player_shields))
            if this_power_up[1] == "bullet_speed":
                bullet_boost += 1
                print("BULLET_BOOST ")
                if (BULLET_COOLDOWN / bullet_boost) <= 1:
                    print("bullet speed maxed out!")
                    POWER_UP_TYPES.remove("bullet_speed")
            if this_power_up[1] == "player_speed":
                player_speed_variable += 50
                print("player speed up")
            if this_power_up[1] == "laser_beam":
                timed_laser_tick = total_num_of_ticks
                print("lasers!")
            
            all_of_the_power_ups.remove(this_power_up)
    
    

    # player movement
    # start jank
    correct_speed = False
    if (pressed_keys[pygame.K_w] and pressed_keys[pygame.K_a]) or (pressed_keys[pygame.K_w] and pressed_keys[pygame.K_d]) or (pressed_keys[pygame.K_s] and pressed_keys[pygame.K_a]) or (pressed_keys[pygame.K_s] and pressed_keys[pygame.K_d]):
        correct_speed = True
    # end jank
    adjust_player_speed_by = (correct_speed * SPEED_CORRECTION + 1*(not correct_speed)) * (PLAYER_SPEED + player_speed_variable) // dt
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
    player_test_position = [player_pos[0], player_pos[1]]
    if pressed_keys[pygame.K_w]:
        player_test_position[1] = (player_pos[1] - adjust_player_speed_by * (1 - player_out_of_bounds_y))
    if pressed_keys[pygame.K_s]:
        player_test_position[1] = (player_pos[1] + adjust_player_speed_by * (1 - player_out_of_bounds_y))
    if pressed_keys[pygame.K_a]:
        player_test_position[0] = (player_pos[0] - adjust_player_speed_by * (1 - player_out_of_bounds_x))
    if pressed_keys[pygame.K_d]:
        player_test_position[0] = (player_pos[0] + adjust_player_speed_by * (1 - player_out_of_bounds_x))
    
    
    if inside_wall(player_pos, PLAYER_WIDTH, PLAYER_HEIGHT):
        # print("fixing player position")
        """
        we need to determine which dimension (x or y) is more in the wall and alter only that one!
        do this by brute force for now: """
        determine_things_x1 = player_test_position[0]
        determine_things_x2 = player_test_position[0]
        determine_things_y1 = player_test_position[1]
        determine_things_y2 = player_test_position[1]
        while inside_wall([determine_things_x1, player_test_position[1]], PLAYER_WIDTH, PLAYER_HEIGHT):
            determine_things_x1 -= 1
        while inside_wall([determine_things_x2, player_test_position[1]], PLAYER_WIDTH, PLAYER_HEIGHT):
            determine_things_x2 += 1
        while inside_wall([player_test_position[0], determine_things_y1], PLAYER_WIDTH, PLAYER_HEIGHT):
            determine_things_y1 += 1
        while inside_wall([player_test_position[0], determine_things_y2], PLAYER_WIDTH, PLAYER_HEIGHT):
            determine_things_y2 -= 1
        
        kick_by = 0
        # not change the smallest thing to change:
        list_of_the_tests = [
                             np.abs(determine_things_x1 - player_test_position[0]), 
                             np.abs(determine_things_x2 - player_test_position[0]), 
                             np.abs(determine_things_y1 - player_test_position[1]), 
                             np.abs(determine_things_y2 - player_test_position[1])]
        thing_to_change = list_of_the_tests.index( np.min(list_of_the_tests) )
        # print(list_of_the_tests)
        if thing_to_change == 0:
            # print("moving player RIGHT to remove from wall")
            player_pos[0] = determine_things_x1 - kick_by
        if thing_to_change == 1:
            # print("moving player LEFT to remove from wall")
            player_pos[0] = determine_things_x2 + kick_by
        if thing_to_change == 2:
            # print("moving player DOWN to remove from wall")
            player_pos[1] = determine_things_y1 + kick_by
        if thing_to_change == 3:
            # print("moving player UP to remove from wall")
            player_pos[1] = determine_things_y2 - kick_by
    else:
        player_pos = [player_test_position[0], player_test_position[1]]
    
    
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
            
            if (timed_laser_tick != 0) and ((timed_laser_tick + POWER_UP_DURATION) > total_num_of_ticks):
                if direction in VALID_LASER_DIRECTIONS:
                    all_of_the_lasers.append(generate_laser(player, player_pos, direction))
                    sfx.shooty(short_laser)
            elif bullet_shotQ:
                bullet_shot_at = total_num_of_ticks
                all_of_the_bullets.append([
                                        generate_bullet(player, player_pos), 
                                        direction])
                sfx.shooty(short_laser)
            



    # stuff for bubbles
    # the "< 5" bit here was picked arbitrarily because it seemed to work to get rid of bubble's jitteryness
    # if (abs(bubbles_pos[0] - player_pos[0]) < 5) and (abs(bubbles_pos[1] - player_pos[1]) < 5):
    #     bubbles_pos[0] = player_pos[0]
    #     bubbles_pos[1] = player_pos[1]
    adjust_bubbles_x = 0
    adjust_bubbles_y = 0
    if bubbles_pos[0] < player_pos[0] - pygame.Surface.get_height(player) / pygame.Surface.get_height(bubbles) :
        adjust_bubbles_x += BUBBLES_SPEED // dt
    if bubbles_pos[0] > player_pos[0] + pygame.Surface.get_height(player) / pygame.Surface.get_height(bubbles):
        adjust_bubbles_x -= BUBBLES_SPEED // dt
    if bubbles_pos[1] < player_pos[1] - pygame.Surface.get_width(player)  / pygame.Surface.get_width(bubbles):
        adjust_bubbles_y += BUBBLES_SPEED // dt
    if bubbles_pos[1] > player_pos[1] + pygame.Surface.get_width(player)  / pygame.Surface.get_width(bubbles):
        adjust_bubbles_y -= BUBBLES_SPEED // dt
    
    bubbles_test_position = [bubbles_pos[0], bubbles_pos[1]]
    if inside_wall(bubbles_pos, BUBBLES_WIDTH, BUBBLES_HEIGHT):
        # print("fixing bubbles position")
        """
        we need to determine which dimension (x or y) is more in the wall and alter only that one!
        do this by brute force for now: """
        determine_things_x1 = bubbles_test_position[0]
        determine_things_x2 = bubbles_test_position[0]
        determine_things_y1 = bubbles_test_position[1]
        determine_things_y2 = bubbles_test_position[1]
        while inside_wall([determine_things_x1, bubbles_test_position[1]], BUBBLES_WIDTH, BUBBLES_HEIGHT):
            determine_things_x1 -= 1
        while inside_wall([determine_things_x2, bubbles_test_position[1]], BUBBLES_WIDTH, BUBBLES_HEIGHT):
            determine_things_x2 += 1
        while inside_wall([bubbles_test_position[0], determine_things_y1], BUBBLES_WIDTH, BUBBLES_HEIGHT):
            determine_things_y1 += 1
        while inside_wall([bubbles_test_position[0], determine_things_y2], BUBBLES_WIDTH, BUBBLES_HEIGHT):
            determine_things_y2 -= 1
        
        kick_by = 0
        # not change the smallest thing to change:
        list_of_the_tests = [
                             np.abs(determine_things_x1 - bubbles_test_position[0]), 
                             np.abs(determine_things_x2 - bubbles_test_position[0]), 
                             np.abs(determine_things_y1 - bubbles_test_position[1]), 
                             np.abs(determine_things_y2 - bubbles_test_position[1])]
        thing_to_change = list_of_the_tests.index( np.min(list_of_the_tests) )
        # print(list_of_the_tests)
        if thing_to_change == 0:
            # print("moving bubbles RIGHT to remove from wall")
            bubbles_pos[0] = determine_things_x1 - kick_by
        if thing_to_change == 1:
            # print("moving bubbles LEFT to remove from wall")
            bubbles_pos[0] = determine_things_x2 + kick_by
        if thing_to_change == 2:
            # print("moving bubbles DOWN to remove from wall")
            bubbles_pos[1] = determine_things_y1 + kick_by
        if thing_to_change == 3:
            # print("moving bubbles UP to remove from wall")
            bubbles_pos[1] = determine_things_y2 - kick_by
    else:
        bubbles_pos[0] = bubbles_test_position[0]
        bubbles_pos[1] = bubbles_test_position[1]

    
    # if inside_wall(player_pos,  PLAYER_WIDTH,  PLAYER_HEIGHT ):
    #     print("player inside wall")
    # if inside_wall(bubbles_pos, BUBBLES_WIDTH, BUBBLES_HEIGHT):
    #     print("bubbles inside wall")
    
    if (adjust_bubbles_x != 0) and (adjust_bubbles_y != 0):
        bubbles_pos[0] += SPEED_CORRECTION * adjust_bubbles_x // 1
        bubbles_pos[1] += SPEED_CORRECTION * adjust_bubbles_y // 1
    else:
        bubbles_pos[0] += adjust_bubbles_x
        bubbles_pos[1] += adjust_bubbles_y

    

    # power up stuff here
    if total_num_of_ticks > POWER_UP_INITIAL_WAIT:
        if (total_num_of_ticks % POWER_UP_FREQUENCY) == 0:
            generated_power_up_type = POWER_UP_TYPES[np.random.randint( len(POWER_UP_TYPES) )]
            generated_power_up      = generate_power_up()
            while inside_wall([generated_power_up.centerx, generated_power_up.centery], POWER_UP_WIDTH, POWER_UP_HEIGHT):
                print("trying to generate power up")
                generated_power_up      = generate_power_up()
            all_of_the_power_ups.append([
                                        generated_power_up,
                                        generated_power_up_type
                                        ])
            print("power_up = "+ str(generated_power_up_type))

    # try and fix player_rect and bubbles_rect here
    if previous_player_pos == player_pos:
        player_rectangle = pygame.Rect.move(player_rectangle, 0, 0)
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

    # screen stuff
    screen.fill(BLACK)
    screen.blit(player, player_pos)
    screen.blit(bubbles, bubbles_pos)
    for this_power_up in all_of_the_power_ups:
        if this_power_up[1] == "bullet_speed":
            screen.blit(bullet_speed_icon, 
                        [this_power_up[0].centerx, 
                         this_power_up[0].centery]
                        )
        if this_power_up[1] == "shield":
            screen.blit(shield_icon, 
                        [this_power_up[0].centerx, 
                         this_power_up[0].centery]
                        )
        if this_power_up[1] == "player_speed":
            screen.blit(speed_boost_icon, 
                        [this_power_up[0].centerx, 
                         this_power_up[0].centery]
                        )
        if this_power_up[1] == "laser_beam":
            screen.blit(laser_beam_icon,
                        [this_power_up[0].centerx, 
                         this_power_up[0].centery]
                        )

    #wall stuff here
    for wall in all_of_the_walls:
        pygame.draw.rect(screen, BLUE, wall)
    
    # pygame.draw.rect(screen, GREEN,  player_rectangle )
    # pygame.draw.rect(screen, YELLOW, bubbles_rectangle)

    for this_bullet in all_of_the_bullets:
        if (this_bullet[0].centerx <= 0) or (this_bullet[0].centerx >= WIDTH) or (this_bullet[0].centery <= 0) or (this_bullet[0].centery >= HEIGHT):
            all_of_the_bullets.remove(this_bullet)
        if inside_wall([this_bullet[0].centerx, this_bullet[0].centery], this_bullet[0].width, this_bullet[0].height):
            all_of_the_bullets.remove(this_bullet)
    
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
    
    for this_laser in all_of_the_lasers:
        pygame.draw.rect(screen, RED, this_laser)
    
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