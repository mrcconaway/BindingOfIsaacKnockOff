"""
Author: Joshua Maldonado
"""

import numpy as np
import random
import pygame
from pygame.locals import *


from colors import *


pygame.init()

SIZE   = WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode(SIZE)
FPS    = 30

clock = pygame.time.Clock()
dt    = clock.tick(FPS)



friendly_bullets = []
enemy_bullets    = []

def damage_flash(entity):
    damage_rect = pygame.Rect(
                              entity.x,
                              entity.y,
                              entity.width,
                              entity.height
                              )
    pygame.draw.rect(screen, entity.color, damage_rect)

class the_player:
    def __init__(self):
        self.x                 =  WIDTH / 2
        self.y                 = HEIGHT / 2
        self.pos               = [self.x, self.y]
        self.width             = 50
        self.height            = 50
        self.speed             = 300
        self.color             = RED
        self.max_health        = 100
        self.current_health    = self.max_health
        self.bullet_damage     = 25
        self.bullets_per_sec   = 5
        self.bullet_cooldown   = FPS / self.bullets_per_sec
        self.bullet_shot_at    = 0
        self.bullet_spread     = 0.1
        self.hit_tick          = 0
        self.duration          = 2
        self.immunity_tick     = 0
        self.immunity_time     = 1/2 * FPS

        self.power_up_duration = 10 * FPS
        self.shields           = -self.power_up_duration
        self.bullet_speed_tick = -self.power_up_duration
        self.player_speed_tick = -self.power_up_duration
        self.laser_beam_tick   = -self.power_up_duration
        self.triple_shot_tick  = -self.power_up_duration
        self.triple_spread     = 10 * np.pi/180

        self.icon              = pygame.image.load("resources/moon_50x50.png").convert()
        self.rect              = pygame.Rect(
                                             self.x,
                                             self.y,
                                             self.width, 
                                             self.height)
    def test_move(self):
        correct_speed = False
        if (pressed_keys[pygame.K_w] and pressed_keys[pygame.K_a]) or (pressed_keys[pygame.K_w] and pressed_keys[pygame.K_d]) or (pressed_keys[pygame.K_s] and pressed_keys[pygame.K_a]) or (pressed_keys[pygame.K_s] and pressed_keys[pygame.K_d]):
            correct_speed = True
        adjust_speed_by = (correct_speed/np.sqrt(2) + 1*(not correct_speed)) * self.speed / dt

        if pressed_keys[pygame.K_w]:
            test_y -= adjust_speed_by
        if pressed_keys[pygame.K_s]:
            test_y += adjust_speed_by
        if pressed_keys[pygame.K_a]:
            test_x -= adjust_speed_by
        if pressed_keys[pygame.K_d]:
            test_x += adjust_speed_by
        
        try:
            test_y
        except:
            test_y = self.y
        try:
            test_x
        except:
            test_x = self.x
        
        return [test_x, test_y]
    def move(self):
        correct_speed = False
        if (pressed_keys[pygame.K_w] and pressed_keys[pygame.K_a]) or (pressed_keys[pygame.K_w] and pressed_keys[pygame.K_d]) or (pressed_keys[pygame.K_s] and pressed_keys[pygame.K_a]) or (pressed_keys[pygame.K_s] and pressed_keys[pygame.K_d]):
            correct_speed = True
        adjust_speed_by = (correct_speed/np.sqrt(2) + 1*(not correct_speed)) * self.speed / dt

        if pressed_keys[pygame.K_w]:
            self.y -= adjust_speed_by
        if pressed_keys[pygame.K_s]:
            self.y += adjust_speed_by
        if pressed_keys[pygame.K_a]:
            self.x -= adjust_speed_by
        if pressed_keys[pygame.K_d]:
            self.x += adjust_speed_by
        
        self.rect.x = self.x
        self.rect.y = self.y
    def shoot(self):
        self.bullet_cooldown = FPS / self.bullets_per_sec
        if (self.bullet_shot_at + self.bullet_cooldown) > total_num_of_ticks:
            bullet_shotQ = True
        else:
            bullet_shotQ = False
        if pressed_keys[pygame.K_UP] or pressed_keys[pygame.K_DOWN] or pressed_keys[pygame.K_LEFT] or pressed_keys[pygame.K_RIGHT]:
            # bullet stuff
            if (total_num_of_ticks > (self.bullet_shot_at + self.bullet_cooldown)):
                if (pressed_keys[pygame.K_UP] and pressed_keys[pygame.K_RIGHT]) and not bullet_shotQ:
                    # direction    = "NE"
                    direction    = -45 * np.pi / 180
                    bullet_shotQ = True
                if (pressed_keys[pygame.K_UP] and pressed_keys[pygame.K_LEFT]) and not bullet_shotQ:
                    # direction    = "NW"
                    direction    = -135 * np.pi / 180
                    bullet_shotQ = True
                if (pressed_keys[pygame.K_DOWN] and pressed_keys[pygame.K_RIGHT]) and not bullet_shotQ:
                    # direction    = "SE"
                    direction    = -315 * np.pi / 180
                    bullet_shotQ = True
                if (pressed_keys[pygame.K_DOWN] and pressed_keys[pygame.K_LEFT]) and not bullet_shotQ:
                    # direction    = "SW"
                    direction    = -225 * np.pi / 180
                    bullet_shotQ = True
                if pressed_keys[pygame.K_UP] and not bullet_shotQ:
                    # direction    = "N"
                    direction    = - 90 * np.pi / 180
                    bullet_shotQ = True
                if pressed_keys[pygame.K_DOWN] and not bullet_shotQ:
                    # direction    = "S"
                    direction    = - 270 * np.pi / 180
                    bullet_shotQ = True
                if pressed_keys[pygame.K_RIGHT] and not bullet_shotQ:
                    # direction    = "E"
                    direction    = 0 * np.pi / 180
                    bullet_shotQ = True
                if pressed_keys[pygame.K_LEFT] and not bullet_shotQ:
                    # direction    = "W"
                    direction    = 180 * np.pi / 180
                    bullet_shotQ = True
                direction += self.bullet_spread * (2*random.random() - 1)
                self.bullet_shot_at = total_num_of_ticks
                if total_num_of_ticks > (self.power_up_duration + self.triple_shot_tick):
                    the_shot_bullet = bullet(self, direction)
                    friendly_bullets.append(the_shot_bullet)
                else:
                    the_shot_bullet_1 = bullet(self, direction - self.triple_spread)
                    the_shot_bullet_2 = bullet(self, direction)
                    the_shot_bullet_3 = bullet(self, direction + self.triple_spread)

                    friendly_bullets.append(the_shot_bullet_1)
                    friendly_bullets.append(the_shot_bullet_2)
                    friendly_bullets.append(the_shot_bullet_3)
    def hit(self, damage, impact: bool):
        if impact:
            if total_num_of_ticks > (self.immunity_tick + self.immunity_time):
                if self.shields == 0:
                    self.current_health -= damage
                    self.hit_tick        = total_num_of_ticks
                    self.immunity_tick   = total_num_of_ticks
                else:
                    self.shields -= 1
                    pygame.draw.rect(screen, BLUE, self.rect)
        else:
            if self.shields != 0:
                self.current_health -= damage
                self.hit_tick        = total_num_of_ticks
                self.immunity_tick   = total_num_of_ticks
            else:
                self.shields -= 1
                pygame.draw.rect(screen, BLUE, self.rect)
    def paint(self):
        height_above_player = 0.5
        health_fraction     = round(self.current_health / self.max_health, 3)
        inflate_bar_size_by = 1 # this kind of looks funky when it's != 1
        health_bar_background = pygame.Rect(
                                            self.x - (self.width - self.width * inflate_bar_size_by) * (1/4),
                                            self.y - height_above_player * self.height,
                                            inflate_bar_size_by * self.width,
                                            10
                                            )
        health_bar_foreground = pygame.Rect(
                                            self.x - (self.width - self.width * inflate_bar_size_by) * (1/4),
                                            self.y - height_above_player * self.height,
                                            inflate_bar_size_by * health_fraction * self.width,
                                            10
                                            )

        pygame.draw.rect(screen, WHITE, health_bar_background)
        pygame.draw.rect(screen, RED, health_bar_foreground)
        screen.blit(self.icon, [self.x, self.y])
        if ((self.hit_tick + self.duration) >= total_num_of_ticks) and (total_num_of_ticks > self.duration):
            damage_flash(self)
    def draw_rect(self):
        return pygame.draw.rect(screen, CYAN, self.rect)

class enemy_1:
    def __init__(self, initial_x, initial_y, test_entity: bool):
        self.x               = initial_x
        self.y               = initial_y
        self.pos             = [self.x, self.y]
        self.width           = 50
        self.height          = 50
        self.speed           = 250
        self.color           = GREEN
        self.max_health      = 50
        self.current_health  = self.max_health
        self.impact_damage   = 20
        self.bullet_damage   = 10
        self.bullets_per_sec = 4
        self.bullet_cooldown = FPS / self.bullets_per_sec
        self.hit_tick        = 0
        self.duration        = 2
        self.is_test_entity  = test_entity
        self.icon            = pygame.image.load("resources/bubbles.png").convert()
        self.rect            = pygame.Rect(
                                           self.x,
                                           self.y,
                                           self.width, 
                                           self.height)
        self.bullet_shot_at = 0
    def move(self, entity):
        flag   = 0
        move_x = 0
        move_y = 0
        if self.x < (entity.x - entity.height / self.height):
            move_x = self.speed // dt
            flag += 1
        if self.x > (entity.x - entity.height / self.height):
            move_x = - self.speed // dt
            flag += 1
        if self.y < (entity.y -  entity.width /  self.width):
            move_y = self.speed // dt
            flag += 1
        if self.y > (entity.y -  entity.width /  self.width):
            move_y = - self.speed // dt
            flag += 1
        
        if flag == 2:
            move_x /= np.sqrt(2)
            move_y /= np.sqrt(2)
        
        self.x += move_x
        self.y += move_y
        
        self.rect.x = self.x
        self.rect.y = self.y
    def shoot(self, entity):
        if (self.bullet_shot_at + self.bullet_cooldown) > total_num_of_ticks:
            bullet_shotQ = True
        else:
            bullet_shotQ = False

        aim_x  = entity.x
        aim_y  = entity.y

        # vector stuff
        r1_vec  = [self.x, self.y]
        r1      = np.sqrt( r1_vec[0]**2 + r1_vec[1]**2 )
        # r1_hat  = [r1_vec[0] / r1, r1_vec[1] / r1]

        r2_vec  = [aim_x, aim_y]
        r2      = np.sqrt( r2_vec[0]**2 + r2_vec[1]**2 )
        # r2_hat  = [r2_vec[0] / r2, r2_vec[1] / r2]

        rPr_vec = [r1_vec[0] - r2_vec[0], r1_vec[1] - r2_vec[1]]
        rPr     = np.sqrt( rPr_vec[0]**2 + rPr_vec[1]**2 )
        theta   = np.arccos( np.dot( [-1, 0], rPr_vec ) / rPr )
        if rPr_vec[1] > 0:
            theta *= (-1)
        if (total_num_of_ticks > (self.bullet_shot_at + self.bullet_cooldown)):
            self.bullet_shot_at = total_num_of_ticks
            the_shot_bullet = bullet(self, theta)
            enemy_bullets.append(the_shot_bullet)
    def hit(self, damage):
        self.current_health -= damage
        self.hit_tick        = total_num_of_ticks
        self.immunity_tick   = total_num_of_ticks
    def paint(self):
        height_above_player = 0.3
        health_fraction     = round(self.current_health / self.max_health, 3)
        inflate_bar_size_by = 1 # this kind of looks funky when it's != 1
        health_bar_background = pygame.Rect(
                                            self.x - (self.width - self.width * inflate_bar_size_by) * (1/4),
                                            self.y - height_above_player * self.height,
                                            inflate_bar_size_by * self.width,
                                            10
                                            )
        health_bar_foreground = pygame.Rect(
                                            self.x - (self.width - self.width * inflate_bar_size_by) * (1/4),
                                            self.y - height_above_player * self.height,
                                            inflate_bar_size_by * health_fraction * self.width,
                                            10
                                            )

        pygame.draw.rect(screen, WHITE, health_bar_background)
        pygame.draw.rect(screen, GREEN, health_bar_foreground)
        screen.blit(self.icon, [self.x, self.y])
        if ((self.hit_tick + self.duration) >= total_num_of_ticks) and (total_num_of_ticks > self.duration):
            damage_flash(self)
    def draw_rect(self):
        pygame.draw.rect(screen, WHITE, self.rect)

class enemy_2:
    def __init__(self, initial_x, initial_y, test_entity: bool):
        self.x               = initial_x
        self.y               = initial_y
        self.pos             = [self.x, self.y]
        self.width           = 50
        self.height          = 50
        self.speed           = 50
        self.color           = BLUE
        self.max_health      = 200
        self.current_health  = self.max_health
        self.impact_damage   = 50
        self.bullet_damage   = 45
        self.bullets_per_sec = 0.5
        self.bullet_cooldown = FPS / self.bullets_per_sec
        self.hit_tick        = 0
        self.duration        = 2
        self.is_test_entity  = test_entity
        self.icon            = pygame.image.load("resources/pumpkin.png").convert()
        self.rect            = pygame.Rect(
                                           self.x,
                                           self.y,
                                           self.width, 
                                           self.height)
        self.bullet_shot_at = 0
    def move(self, entity):
        flag = 0
        if self.x < (entity.x - entity.height / self.height):
            self.x += self.speed // dt
            flag += 1
        if self.x > (entity.x - entity.height / self.height):
            self.x -= self.speed // dt
            flag += 1
        if self.y < (entity.y -  entity.width /  self.width):
            self.y += self.speed // dt
            flag += 1
        if self.y > (entity.y -  entity.width /  self.width):
            self.y -= self.speed // dt
            flag += 1
        
        # if flag == 2:
        #     self.x /= np.sqrt(2)
        #     self.y /= np.sqrt(2)
        
        self.rect.x = self.x
        self.rect.y = self.y
    def shoot(self, entity):
        if (self.bullet_shot_at + self.bullet_cooldown) > total_num_of_ticks:
            bullet_shotQ = True
        else:
            bullet_shotQ = False

        aim_x  = entity.x
        aim_y  = entity.y

        # vector stuff
        r1_vec  = [self.x, self.y]
        r1      = np.sqrt( r1_vec[0]**2 + r1_vec[1]**2 )
        # r1_hat  = [r1_vec[0] / r1, r1_vec[1] / r1]

        r2_vec  = [aim_x, aim_y]
        r2      = np.sqrt( r2_vec[0]**2 + r2_vec[1]**2 )
        # r2_hat  = [r2_vec[0] / r2, r2_vec[1] / r2]

        rPr_vec = [r1_vec[0] - r2_vec[0], r1_vec[1] - r2_vec[1]]
        rPr     = np.sqrt( rPr_vec[0]**2 + rPr_vec[1]**2 )
        theta = -np.arccos( np.dot( [-1, 0], rPr_vec ) / rPr )
        if rPr_vec[1] < 0:
            theta *= (-1)
        if (total_num_of_ticks > (self.bullet_shot_at + self.bullet_cooldown)):
            self.bullet_shot_at = total_num_of_ticks
            the_shot_bullet = bullet(self, theta)
            enemy_bullets.append(the_shot_bullet)
    def hit(self, damage):
        self.current_health -= damage
        self.hit_tick        = total_num_of_ticks
        self.immunity_tick   = total_num_of_ticks
    def paint(self):
        height_above_player = 0.3
        health_fraction     = round(self.current_health / self.max_health, 3)
        inflate_bar_size_by = 1 # this kind of looks funky when it's != 1
        health_bar_background = pygame.Rect(
                                            self.x - (self.width - self.width * inflate_bar_size_by) * (1/4),
                                            self.y - height_above_player * self.height,
                                            inflate_bar_size_by * self.width,
                                            10
                                            )
        health_bar_foreground = pygame.Rect(
                                            self.x - (self.width - self.width * inflate_bar_size_by) * (1/4),
                                            self.y - height_above_player * self.height,
                                            inflate_bar_size_by * health_fraction * self.width,
                                            10
                                            )

        pygame.draw.rect(screen, WHITE, health_bar_background)
        pygame.draw.rect(screen, GREEN, health_bar_foreground)
        screen.blit(self.icon, [self.x, self.y])
        if ((self.hit_tick + self.duration) >= total_num_of_ticks) and (total_num_of_ticks > self.duration):
            damage_flash(self)
    def draw_rect(self):
        pygame.draw.rect(screen, WHITE, self.rect)

class bullet:
    def __init__(self, entity, direction):
        self.speed                = 600
        self.range                = 300        
        self.bullet_size          = 15
        self.color                = entity.color
        self.x                    = entity.x +  entity.width / 2 - self.bullet_size / 2
        self.y                    = entity.y + entity.height / 2 - self.bullet_size / 2
        self.direction            = direction
        self.bullet_damage        = entity.bullet_damage
        self.bullets_per_second   = 5
        self.bullet_cooldown      = FPS // self.bullets_per_second
        # self.bullet_shot_tick   = entity.bullet_shot_at            # tracks when bullet is shot in terms of ticks
        # self.bullet_shotQ       = False                            # tracks to see if a bullet was shot (so you can't spam in multiple directions)
        self.bullet_variability   = 0.1                             # don't go crazy here
        self.x_bullet_variability = round(self.bullet_variability * (2 * random.random() - 1), 4)
        self.y_bullet_variability = round(self.bullet_variability * (2 * random.random() - 1), 4)
        self.rect                 = pygame.Rect(
                                                self.x,
                                                self.y,
                                                self.bullet_size, self.bullet_size
                                                )
        if isinstance(entity, the_player):
            self.from_enemy       = False
        else:
            self.from_enemy       = True
    def move(self):
        if type(self.direction) == str:
            if self.direction == "N":
                self.rect = pygame.Rect.move(self.rect,                           self.x_bullet_variability * self.speed / dt,                                                       -self.speed / dt)
            if self.direction == "S":
                self.rect = pygame.Rect.move(self.rect,                           self.x_bullet_variability * self.speed / dt,                                                        self.speed / dt)
            if self.direction == "E":
                self.rect = pygame.Rect.move(self.rect,                                                       self.speed / dt,                            self.y_bullet_variability * self.speed / dt)
            if self.direction == "W":
                self.rect = pygame.Rect.move(self.rect,                                                     - self.speed / dt,                            self.y_bullet_variability * self.speed / dt)
            if self.direction == "NW":
                self.rect = pygame.Rect.move(self.rect, -(1 / np.sqrt(2)) * self.speed * (1 + self.x_bullet_variability) / dt,  -(1 / np.sqrt(2)) * self.speed * (1 + self.y_bullet_variability) / dt)
            if self.direction == "NE":
                self.rect = pygame.Rect.move(self.rect,  (1 / np.sqrt(2)) * self.speed * (1 + self.x_bullet_variability) / dt,  -(1 / np.sqrt(2)) * self.speed * (1 + self.y_bullet_variability) / dt)
            if self.direction == "SW":
                self.rect = pygame.Rect.move(self.rect, -(1 / np.sqrt(2)) * self.speed * (1 + self.x_bullet_variability) / dt,   (1 / np.sqrt(2)) * self.speed * (1 + self.y_bullet_variability) / dt)
            if self.direction == "SE":
                self.rect = pygame.Rect.move(self.rect,  (1 / np.sqrt(2)) * self.speed * (1 + self.x_bullet_variability) / dt,   (1 / np.sqrt(2)) * self.speed * (1 + self.y_bullet_variability) / dt)
        
        else:
            self.rect = pygame.Rect.move(self.rect, 
                                         self.speed * np.cos(self.direction) / dt,
                                         self.speed * np.sin(self.direction) / dt,
                                         )

all_of_the_power_ups = []
POWER_UP_TYPES       = ["shield", "bullet_speed", "player_speed", "laser_beam", "triple_shot"]
class power_up:
    def __init__(self, power_up_type: str, initial_x, initial_y):
        self.x               = initial_x
        self.y               = initial_y
        self.pos             = [self.x, self.y]
        self.width           = 40
        self.height          = 40
        self.hit_tick        = 0
        self.power_up_type   = power_up_type
        self.icon            = eval("pygame.image.load(\"resources/"+ self.power_up_type +"_icon.png\").convert()")
        self.rect            = pygame.Rect(
                                           self.x,
                                           self.y,
                                           self.width, 
                                           self.height)
        all_of_the_power_ups.append(self)
    def collect_power_up(self):
        if self.power_up_type == "shield":
            player.shields += 1
        if self.power_up_type == "bullet_speed":
            player.bullet_speed_tick = total_num_of_ticks
            player.bullets_per_sec  += 2
        if self.power_up_type == "player_speed":
            player.speed += 100
        if self.power_up_type == "laser_beam":
            print("laser beams currently not working")
        if self.power_up_type == "triple_shot":
            player.triple_shot_tick = total_num_of_ticks
    def paint(self):
        screen.blit(self.icon, self.pos)
    def draw_rect(self):
        pygame.draw.rect(screen, WHITE, self.rect)

all_of_the_walls = []
class wall:
    def __init__(self, initial_x, initial_y, width, height, stops_bullets: bool, breakable: bool):
        self.x             = initial_x
        self.y             = initial_y
        self.width         = width
        self.height        = height
        self.center_x      = initial_x +  width / 2
        self.center_y      = initial_y + height / 2
        self.stops_bullets = stops_bullets
        self.breakable     = breakable
        self.health        = 3 * player.bullet_damage  # this is to make it such that it ALWAYS takes 3 bullets from the player to break a wall (at least from the wall's init)
        self.rect          = pygame.Rect(
                                         initial_x,
                                         initial_y,
                                         width,
                                         height
                                         )
        all_of_the_walls.append(self)
    def inside(self, entity):
        if pygame.Rect.colliderect(self.rect, entity.rect):
            return True
        else:
            return False
    def draw_rect(self):
        pygame.draw.rect(screen, WHITE, self.rect)



player      = the_player()
test_player = the_player()

bad_guys       = []
bubbles_1      = enemy_1(100, 200, False)
test_bubbles_1 = enemy_1(100, 200, True)
bubbles_2      = enemy_1( 50,  50, False)
test_bubbles_2 = enemy_1( 50,  50, True)
bubbles_6      = enemy_1(100,   0, False)
test_bubbles_6 = enemy_1(100,   0, True)
bubbles_3      = enemy_2(200, 200, False)
test_bubbles_3 = enemy_2(200, 200, True)
bubbles_4      = enemy_2(300, 350, False)
test_bubbles_4 = enemy_2(300, 350, True)
bubbles_5      = enemy_2(400, 300, False)
test_bubbles_5 = enemy_2(400, 300, True)

power_up_1 = power_up("bullet_speed", 540, 740)
power_up_2 = power_up("player_speed", 250, 450)
power_up_3 = power_up("shield", 200, 500)
power_up_4 = power_up("triple_shot", 700, 650)

wall_1 = wall(600, 500, 50, 200, True, False)

# append all bad guys to the bad_guys list
i = 1
appending = True
while appending:
    try:
        eval("bad_guys.append(bubbles_"+ str(i) +")")
        eval("bad_guys.append(test_bubbles_"+ str(i) +")")
    except:
        appending = False
    i += 1



# print("\n"*5)
global pressed_keys
global total_num_of_ticks
previous_player_pos = [player.x, player.y]
total_num_of_ticks  = 0
the_game_is_running = True
while the_game_is_running:
    test_player.speed = player.speed

    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_ESCAPE]:
        the_game_is_running = False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            the_game_is_running = False


    # test collisions first, then do stuff with surviving entities
    # bullet collisions
    for this_bullet in friendly_bullets:
        for bad_guy in bad_guys:
            if pygame.Rect.colliderect(bad_guy.rect, this_bullet) and not bad_guy.is_test_entity:
                bad_guy.hit(this_bullet.bullet_damage)
                bad_guys[ bad_guys.index(bad_guy) + 1 ].hit(this_bullet.bullet_damage)
                try:
                    friendly_bullets.remove(this_bullet)
                except:
                    # print("bullet not removed")
                    None
    for this_bullet in enemy_bullets:
        if pygame.Rect.colliderect(player.rect, this_bullet):
            player.hit(this_bullet.bullet_damage, False)
            enemy_bullets.remove(this_bullet)
 
    # wall collisions
    for this_wall in all_of_the_walls:
        # bullet stuff
        for this_bullet in enemy_bullets:
            if this_wall.inside(this_bullet):
                enemy_bullets.remove(this_bullet)
        for this_bullet in friendly_bullets:
            if this_wall.inside(this_bullet):
                friendly_bullets.remove(this_bullet)
        
        # player stuff
        stuck   = False  # keeps track of if the test_player is currently stuck
        stuck_x = False  # flag to see if x was causing problems
        stuck_y = False  # same flag but for y
        test_player.move()
        if this_wall.inside(test_player):
            stuck = True
        if stuck:
            # test_player.x = player.x
            # test_player.y = player.y

            # test x movement:
            test_player.move()
            if this_wall.inside(test_player):
                stuck_x = True

                if stuck and (player.x > test_player.x):
                    test_player.x = player.x
                    while (player.x >= test_player.x - player.speed / FPS) and (player.x <= test_player.x + player.speed / FPS):
                        test_player.x += 1
                        if this_wall.inside(test_player):
                            stuck = False
                            print("+fixed")
                
                if stuck and (player.x < test_player.x):
                    test_player.x = player.x
                    while (player.x >= test_player.x - player.speed / FPS) and (player.x <= test_player.x + player.speed / FPS):
                        test_player.x -= 1
                        if this_wall.inside(test_player):
                            stuck = False
                            print("-fixed")
            if stuck:
                print("stuck not fixed . . .")
                print("")
        
        player.move()
        if stuck_x:
            player.x = test_player.x
        elif stuck_y:
            player.y = test_player.y
        test_player.x = player.x
        test_player.y = player.y
        
        for i in range(len(bad_guys)):
            bad_guy = bad_guys[i]
            if bad_guy.is_test_entity:
                bad_guy.move(player)
            else:
                if this_wall.inside(bad_guys[i + 1]):
                    # print("enemy inside wall")
                    bad_guys[i+1].x = bad_guy.x
                    bad_guys[i+1].y = bad_guy.y
                else:
                    bad_guy.move(player)
    
    # removing health
    for bad_guy in bad_guys:
        if bad_guy.current_health <= 0:
            bad_guys.remove(bad_guy)
    
    # bad guys colliding with player
    for bad_guy in bad_guys:
        if not bad_guy.is_test_entity:
            if pygame.Rect.colliderect(bad_guy.rect, player.rect):
                player.hit(bad_guy.impact_damage, True)
    
    # player colliding with power ups
    for this_power_up in all_of_the_power_ups:
        if pygame.Rect.colliderect(this_power_up.rect, player.rect):
            this_power_up.collect_power_up()
            all_of_the_power_ups.remove(this_power_up)


    # shooting from player and enemies
    player.shoot()
    for bad_guy in bad_guys:
        if not bad_guy.is_test_entity:
            bad_guy.shoot(player)



    # drawing images (and some movement for loop efficiency)
    screen.fill(BLACK)
    player.paint()
    test_player.draw_rect()
    for bad_guy in bad_guys:
        if not bad_guy.is_test_entity:
            bad_guy.paint()
        # else:
        #     bad_guy.draw_rect()
    for this_power_up in all_of_the_power_ups:
        this_power_up.paint()
    for this_bullet in friendly_bullets:
        this_bullet.move()
        pygame.draw.rect(screen, this_bullet.color, this_bullet)
    for this_bullet in enemy_bullets:
        this_bullet.move()
        pygame.draw.rect(screen, this_bullet.color, this_bullet)
    for this_wall in all_of_the_walls:
        this_wall.draw_rect()

    pygame.display.update()
    pygame.display.flip()
    pygame.time.delay(1000//FPS)
    total_num_of_ticks += 1

    if player.current_health <= 0:
        the_game_is_running = False
    


