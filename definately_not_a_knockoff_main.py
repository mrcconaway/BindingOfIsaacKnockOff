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
from handling_wall_stuff        import *
from sfx                        import *


print("\n"*5)  # this is a spacer to make it easier to troubleshoot error messages
TROUBLESHOOTING = False  # determines if print statements will occur after set amount of frames
bouncy_bullets  = False

camera     = pygame.math.Vector2((0, 0))





test_matrix = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ,1, 1, 1, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ,1, 1, 1, 1]]

level_1_matrix = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ,1, 1, 1, 1],
                  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                  [1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
                  [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
                  [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
                  [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1],
                  [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1],
                  [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                  [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                  [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1],
                  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
                  [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
                  [1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
                  [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ,1, 1, 1, 1]]

playable_space = map_walls_from_matrix(level_1_matrix)



camera_pos = [player_pos[0], player_pos[1]]
def adjust_for_camera(position):
    return [position[0] - camera_pos[0], position[1] - camera_pos[1]]


# ### Steven's sound corner

# pygame.mixer.init()
# shoot_sound_1 = sfx.get_shooty()
# shoot_sound_2 = sfx.triple_shooty()

# ###

while the_game_is_running:
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_ESCAPE]:
        the_game_is_running = False
    
    camera_smoothness = 20
    camera_pos = [player_pos[0] - (WIDTH  / 2), 
                  player_pos[1] - (HEIGHT / 2)
                  ]
    camera.x   = camera_pos[0] / camera_smoothness
    camera.y   = camera_pos[1] / camera_smoothness
    # pos_on_the_screen = (player_pos[0] - camera_pos[0], player_pos[1] - camera_pos[1])
    
    the_current_game_state = [ pressed_keys, 
                              [player_pos, bubbles_pos, camera_pos], 
                              [player_health, bubbles_health], 
                              [total_num_of_ticks, player_hit_tick, bubbles_hit_tick, bullet_shot_at, triple_shot_tick, timed_laser_tick],
                              [all_of_the_bullets, all_of_the_lasers],
                              player_speed_variable,
                              playable_space
                              ]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            the_game_is_running = False
    
    if player_health <= 0:
        the_game_is_running = False
    if bubbles_health <= 0:
        bubbles_health = respawn_bubbles(player_pos, the_current_game_state)
        times_bubbles_killed += 1
        bubbles_hit_tick = 0
    
    
    for this_bullet in all_of_the_bullets:
        if inside_wall([this_bullet[0].centerx, this_bullet[0].centery], this_bullet[0].width, this_bullet[0].height):
            if bouncy_bullets:
                this_bullet_direction_index = VALID_SHOT_DIRECTIONS.index(this_bullet[1])
                this_bullet_index           = all_of_the_bullets.index(this_bullet)
                
                # test for directly horizontal/vertical collisions first
                if inside_wall(this_bullet[0].midleft, BULLET_SIZE, BULLET_SIZE) or inside_wall(this_bullet[0].midright, BULLET_SIZE, BULLET_SIZE) or inside_wall(this_bullet[0].midtop, BULLET_SIZE, BULLET_SIZE) or inside_wall(this_bullet[0].midbottom, BULLET_SIZE, BULLET_SIZE):
                    all_of_the_bullets[ all_of_the_bullets.index(this_bullet) ][1] = VALID_SHOT_DIRECTIONS[(this_bullet_direction_index + 4)%8 ]
                # then test for diagonal nonsense
                if x_inside_wall(this_bullet[0].topleft, BULLET_SIZE):
                    if this_bullet[1] == "NW":
                        all_of_the_bullets[this_bullet_index][1] = "NE"

            else:
                all_of_the_bullets.remove(this_bullet)

    # hitting bubbles with bullet collisions
    if total_num_of_ticks > (bubbles_hit_tick + BUBBLES_COOLDOWN):
        for b in all_of_the_bullets:
            if pygame.Rect.colliderect(bubbles_rectangle, b[0]):
                bubbles_health -= bullet_damage
                all_of_the_bullets.remove(b)

                bubbles_hit_tick = total_num_of_ticks

    for this_laser in all_of_the_lasers:
        if pygame.Rect.colliderect(bubbles_rectangle, this_laser):
            if bubbles_health > 0:
                bubbles_health -= laser_damage
    all_of_the_lasers = []


    # bubbles-player collision
    if pygame.Rect.colliderect(bubbles_rectangle, player_rectangle) and (total_num_of_ticks > player_hit_tick + PLAYER_IMMUNITY_TIME):
        # print("you're getting hit!")
        if player_shields == 0:
            player_health -= bubbles_damage
        else:
            player_shields -= 1
            player_hit_tick = total_num_of_ticks
        
        print("shields left: "+ str(player_shields))
        print("health left : "+ str(player_health))
        print("bubbles has hit you")
        
        player_hit_tick = total_num_of_ticks

    # power up collisions
    for this_power_up in all_of_the_power_ups:
        if pygame.Rect.colliderect(this_power_up[0], player_rectangle):
            # print("power up collected!")
            if this_power_up[1] == "shield":
                player_shields += 1
                print("shields: "+ str(player_shields))
            if this_power_up[1] == "bullet_speed":
                bullet_boost += 1
                # print("BULLET_BOOST ")
                if (BULLET_COOLDOWN / bullet_boost) <= 1:
                    print("bullet speed maxed out!")
                    try:
                        POWER_UP_TYPES.remove("bullet_speed")
                    except:
                        print("bullet speed already removed")
            if this_power_up[1] == "player_speed":
                player_speed_variable += 50
                # print("player speed up")
            if this_power_up[1] == "laser_beam":
                timed_laser_tick = total_num_of_ticks
                # print("lasers!")
            if this_power_up[1] == "triple_shot":
                triple_shot_tick = total_num_of_ticks
                # print("triple shot!")
            
            all_of_the_power_ups.remove(this_power_up)
    
    
    player_pos = move_player(the_current_game_state)


    updates_from_shoot_bullet = shoot_bullet(the_current_game_state)
    bullet_shot_at            = updates_from_shoot_bullet[0]
    all_of_the_lasers         = updates_from_shoot_bullet[1]
            

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
        bubbles_is_stuck_flag += 1
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
        if thing_to_change == 0:
            bubbles_pos[0] = determine_things_x1 - kick_by
        if thing_to_change == 1:
            bubbles_pos[0] = determine_things_x2 + kick_by
        if thing_to_change == 2:
            bubbles_pos[1] = determine_things_y1 + kick_by
        if thing_to_change == 3:
            bubbles_pos[1] = determine_things_y2 - kick_by
    else:
        bubbles_is_stuck_flag = 0
        bubbles_pos[0] = bubbles_test_position[0]
        bubbles_pos[1] = bubbles_test_position[1]


    if (adjust_bubbles_x != 0) and (adjust_bubbles_y != 0):
        bubbles_pos[0] += SPEED_CORRECTION * adjust_bubbles_x // 1
        bubbles_pos[1] += SPEED_CORRECTION * adjust_bubbles_y // 1
    else:
        bubbles_pos[0] += adjust_bubbles_x
        bubbles_pos[1] += adjust_bubbles_y
    bubbles_pos[0] -= camera_pos[0]
    bubbles_pos[1] -= camera_pos[1]

    

    # power up stuff here
    if total_num_of_ticks > POWER_UP_INITIAL_WAIT:
        if (total_num_of_ticks % POWER_UP_FREQUENCY) == 0:
            generated_power_up_type = POWER_UP_TYPES[np.random.randint( len(POWER_UP_TYPES) )]
            generated_power_up      = generate_power_up()
            while inside_wall([generated_power_up.centerx, generated_power_up.centery], POWER_UP_WIDTH, POWER_UP_HEIGHT):
                # print("trying to generate power up")
                generated_power_up      = generate_power_up()
            all_of_the_power_ups.append([
                                        generated_power_up,
                                        generated_power_up_type
                                        ])
            # print("power_up = "+ str(generated_power_up_type))

    # try and fix player_rect and bubbles_rect here
    player_pos = adjust_for_camera(player_pos)
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
    
    # pygame.draw.rect(screen, GREEN,  player_rectangle )
    # screen.blit(player, (player_pos[0] - camera_pos[0], player_pos[1] - camera_pos[1]))
    # screen.blit(bubbles, adjust_for_camera(bubbles_pos))
    screen.blit(bubbles, bubbles_pos)
    for this_power_up in all_of_the_power_ups:
        this_power_up[0].centerx -= camera_pos[0]
        this_power_up[0].centery -= camera_pos[1]
        if this_power_up[1] == "bullet_speed":
            screen.blit(bullet_speed_icon, 
                        [this_power_up[0].centerx, this_power_up[0].centery]
                        )
        if this_power_up[1] == "shield":
            screen.blit(shield_icon, 
                        [this_power_up[0].centerx, this_power_up[0].centery]
                        )
        if this_power_up[1] == "player_speed":
            screen.blit(speed_boost_icon, 
                        [this_power_up[0].centerx, this_power_up[0].centery]
                        )
        if this_power_up[1] == "laser_beam":
            screen.blit(laser_beam_icon,
                        [this_power_up[0].centerx, this_power_up[0].centery]
                        )
        if this_power_up[1] == "triple_shot":
            screen.blit(triple_shot_icon,
                        [this_power_up[0].centerx, this_power_up[0].centery]
                        )

    #wall stuff here
    for wall in all_of_the_walls:
        wall.x -= camera_pos[0]
        wall.y -= camera_pos[1]
        pygame.draw.rect(screen, BLUE, wall)
    
    move_bullets(all_of_the_bullets, the_current_game_state)

    for this_laser in all_of_the_lasers:
        pygame.draw.rect(screen, RED, this_laser)
    
    # handle bullet hits with entities and health bars:
    if (player_hit_tick + red_box_cooldown  >= total_num_of_ticks) and (total_num_of_ticks > red_box_cooldown):
        pygame.draw.rect(screen, RED,  player_rectangle )
    if (bubbles_hit_tick + red_box_cooldown >= total_num_of_ticks) and (total_num_of_ticks > red_box_cooldown):
        pygame.draw.rect(screen, RED, bubbles_rectangle)
    health_bar(player_rectangle , player_pos , player_health , default_player_health )
    health_bar(bubbles_rectangle, adjust_for_camera(bubbles_pos), bubbles_health, default_bubbles_health)

    
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

print("times bubbles killed: "+ str(times_bubbles_killed))  # currently broken