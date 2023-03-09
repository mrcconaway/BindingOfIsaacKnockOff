import pygame
import os
import platform

def get_shooty(samplename='laser_short_dry.wav'):
    if platform.system() == "macOS":
        laser_short_dry = pygame.mixer.Sound('./../audio/'+samplename) # this will need to be fixed with os to work on everyones shit
    else:
        laser_short_dry = pygame.mixer.Sound('resources/audio/'+samplename)
    return(laser_short_dry)

def triple_shooty(samplename='laser_lomg_dry.wav'):
    if platform.system() == "macOS":
        laser_short_dry = pygame.mixer.Sound('./../audio/'+samplename) # this will need to be fixed with os to work on everyones shit
    else:
        laser_short_dry = pygame.mixer.Sound('resources/audio/'+samplename)
    return(laser_short_dry)


def shooty(sample):
	sample.play()
	sample.set_volume(0.05)
	return

### Steven's sound corner

pygame.mixer.init()
shoot_sound_1 = get_shooty()
shoot_sound_2 = triple_shooty()

###

	