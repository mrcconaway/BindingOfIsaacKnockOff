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
    if isinstance(entity, the_player):
        pygame.draw.rect(screen,   RED, damage_rect)
    else:
        pygame.draw.rect(screen, GREEN, damage_rect)

class the_player:
    def __init__(self):
        self.x               =  WIDTH / 2
        self.y               = HEIGHT / 2
        self.pos             = [self.x, self.y]
        self.width           = 50
        self.height          = 50
        self.speed           = 300
        self.max_health      = 100
        self.current_health  = self.max_health
        self.bullets_per_sec = 6
        self.bullet_cooldown = FPS / self.bullets_per_sec
        self.hit_tick        = 0
        self.duration        = 2
        self.icon            = pygame.image.load("resources/pumpkin.png").convert()
        self.rect            = pygame.Rect(
                                           self.x,
                                           self.y,
                                           self.width, 
                                           self.height)
        self.bullet_shot_at = 0
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
        if (self.bullet_shot_at + self.bullet_cooldown) > total_num_of_ticks:
            bullet_shotQ = True
        else:
            bullet_shotQ = False
        if pressed_keys[pygame.K_UP] or pressed_keys[pygame.K_DOWN] or pressed_keys[pygame.K_LEFT] or pressed_keys[pygame.K_RIGHT]:
            # bullet stuff
            if (total_num_of_ticks > (self.bullet_shot_at + self.bullet_cooldown)):
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
                self.bullet_shot_at = total_num_of_ticks
                the_shot_bullet = bullet(self, direction)
                if not the_shot_bullet.from_enemy:
                    friendly_bullets.append(the_shot_bullet)
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
        return pygame.draw.rect(screen, WHITE, self.rect)

class enemy_1:
    def __init__(self, initial_x, initial_y):
        self.x               = initial_x
        self.y               = initial_y
        self.pos             = [self.x, self.y]
        self.width           = 50
        self.height          = 50
        self.speed           = 150
        self.max_health      = 50
        self.current_health  = self.max_health
        self.impact_damage   = 20
        self.bullets_per_sec = 2
        self.bullet_cooldown = FPS / self.bullets_per_sec
        self.hit_tick        = 0
        self.duration        = 2
        self.icon            = pygame.image.load("resources/bubbles.png").convert()
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
    def __init__(self, initial_x, initial_y):
        self.x               = initial_x
        self.y               = initial_y
        self.pos             = [self.x, self.y]
        self.width           = 50
        self.height          = 50
        self.speed           = 50
        self.max_health      = 200
        self.current_health  = self.max_health
        self.impact_damage   = 50
        self.bullets_per_sec = 0.2
        self.bullet_cooldown = FPS / self.bullets_per_sec
        self.hit_tick        = 0
        self.duration        = 2
        self.icon            = pygame.image.load("resources/moon_50x50.png").convert()
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
        self.x                    = entity.x +  entity.width / 2 - self.bullet_size / 2
        self.y                    = entity.y + entity.height / 2 - self.bullet_size / 2
        self.direction            = direction
        self.bullet_damage        = 25
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




bad_guys  = []
player    = the_player()
bubbles_1 = enemy_1(300, 500)
bubbles_2 = enemy_1(700, 600)
bubbles_3 = enemy_1(200, 400)
bubbles_4 = enemy_1(  0, 600)
bubbles_5 = enemy_2(200, 200)
bubbles_6 = enemy_2(200, 600)

# append all bad guys to the bad_guys list
i = 1
running = True
while running:
    try:
        eval("bad_guys.append(bubbles_"+ str(i) +")")
    except:
        running = False
    i += 1



print("\n"*5)
global pressed_keys
global total_num_of_ticks
total_num_of_ticks  = 0
the_game_is_running = True
while the_game_is_running:
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_ESCAPE]:
        the_game_is_running = False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            the_game_is_running = False


    # test collisions first, then do stuff with surviving entities
    for this_bullet in friendly_bullets:
        for entity in bad_guys:
            if pygame.Rect.colliderect(entity.rect, this_bullet):
                entity.current_health -= this_bullet.bullet_damage
                friendly_bullets.remove(this_bullet)
                entity.hit_tick = total_num_of_ticks
    for this_bullet in enemy_bullets:
        if pygame.Rect.colliderect(player.rect, this_bullet):
            player.current_health -= this_bullet.bullet_damage
            enemy_bullets.remove(this_bullet)
            player.hit_tick = total_num_of_ticks
 
    for bad_guy in bad_guys:
        if bad_guy.current_health <= 0:
            bad_guys.remove(bad_guy)
    
    for bad_guy in bad_guys:
        if pygame.Rect.colliderect(bad_guy.rect, player.rect):
            player.current_health -= bad_guy.impact_damage



    player.move()
    player.shoot()
    for bad_guy in bad_guys:
        bad_guy.shoot(player)
        bad_guy.move(player)

    screen.fill(BLACK)    

    player.paint()
    for bad_guy in bad_guys:
        bad_guy.paint()
    for this_bullet in friendly_bullets:
        this_bullet.move()
        pygame.draw.rect(screen, RED,   this_bullet)
    for this_bullet in enemy_bullets:
        this_bullet.move()
        pygame.draw.rect(screen, GREEN, this_bullet)

    pygame.display.update()
    pygame.display.flip()
    pygame.time.delay(1000//FPS)
    total_num_of_ticks += 1

    if player.current_health <= 0:
        the_game_is_running = False


