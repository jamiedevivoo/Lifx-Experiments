#!/usr/bin/env python3
# coding=utf-8

# Importing things to make it work
import sys
import pygame
import time
import random
from copy import deepcopy
from time import sleep
from lifxlan import LifxLAN, COLD_WHITE, CYAN, GOLD, GREEN, ORANGE, PINK, PURPLE, RED, WARM_WHITE, WHITE, YELLOW, BLUE

# Some vars / pre game things
DIFFICULTY = 3
START_LENGTH = 8
WAIT = 0.1 / DIFFICULTY
WINNER_TILE_FROM = random.randint(1,30)
WINNER_TILE_TO = WINNER_TILE_FROM+START_LENGTH
RES	= [800, 600]
pygame.init()
SCREEN = pygame.display.set_mode(RES)
pygame.display.set_caption("Tap")

class Mob():

    # This was here from some example code n i'm too scared to delete it
    # Something to do with the pygame popup box thing
    def __init__(self):
        self.headx = 100
        self.heady = 100
        self.length = START_LENGTH
        self.elements = [[self.headx, self.heady]]

def check(f, t, i):

    # f = Winning tile from
    # t = Winning tile to
    # i = Actual tile you hit on ;)
    
    if i >= f and i <= t:

        # Global vars (still don't rly understand these)
        global DIFFICULTY
        global WINNER_TILE_FROM
        global WINNER_TILE_TO
        global START_LENGTH
        global WAIT

        # Update the vars
        DIFFICULTY = DIFFICULTY + 2
        START_LENGTH = START_LENGTH - 1
        WINNER_TILE_FROM = random.randint(1,30)
        WINNER_TILE_TO = WINNER_TILE_FROM+START_LENGTH
        print("WIN!")

        if START_LENGTH == 0:

            # Congrats u won the game
            completeLights()

            #Reset game
            DIFFICULTY = 2
            START_LENGTH = 5
            WAIT = 0.09 / DIFFICULTY
            WINNER_TILE_FROM = random.randint(1,30)
            WINNER_TILE_TO = WINNER_TILE_FROM+START_LENGTH
            time.sleep(3)

        else:
            # You're good
            goodLights()
            time.sleep(1)

    else:
        # You're shit
        print("LOSE")
        DIFFICULTY = DIFFICULTY - 1
        START_LENGTH = START_LENGTH + 1
        WINNER_TILE_FROM = random.randint(1,30)
        WINNER_TILE_TO = WINNER_TILE_FROM+START_LENGTH
        badLights()
        time.sleep(1)
        return

def main():

    # Find the lights (well, assume they exist or otherwise crash :))))
    lifx = LifxLAN(int(1),False)
    multizone_lights = lifx.get_multizone_lights()

    if len(multizone_lights) > 0:

        # Get the lights n stuff
        strip = multizone_lights[0]
        all_zones = strip.get_color_zones()
        original_zones = deepcopy(all_zones)
        zone_count = len(all_zones)     

        devices = lifx.get_lights()
        bulb = devices[0]
        original_power = bulb.get_power()
        bulb.set_power("on")

        # Snake size
        snake_size = zone_count/32 # length of snake in zones
        tail = 0
        head = snake_size - 1

        # COLOURSSS !!!!! 
        randomColours = [CYAN, GREEN, ORANGE, PINK, PURPLE, YELLOW, BLUE]
        snake_color = WHITE
        background_color = RED

        try:
            while True:

                # Keyboard triggers
                for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()
                                elif event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_ESCAPE:
                                        pygame.quit()
                                        sys.exit()
                                    elif event.key == pygame.K_SPACE:
                                        print("SPACE")
                                        check(WINNER_TILE_FROM, WINNER_TILE_TO, tail)

                # Interval of when the snake should move
                time.sleep(WAIT)

                # Case 1: Snake hasn't wrapped around yet
                if head > tail:

                        if tail > 0:
                        
                         strip.set_zone_color(0, tail-1, background_color, 0, True, 0)
                        strip.set_zone_color(tail, head, snake_color, 0, True, 0)

                    
                        if head < zone_count - 1:
                             strip.set_zone_color(head+1, zone_count-1, background_color, 0, True, 1)

                    # Case 2: Snake has started to wrap around
                else:

                        if head > 0:
                            strip.set_zone_color(0, head-1, snake_color, 0, True, 0)
                        strip.set_zone_color(head, tail, background_color, 0, True, 0)

                        if tail < zone_count - 1:
                            strip.set_zone_color(tail+1, zone_count-1, snake_color, 0, True, 1)
                        
                    # update indices for the snake's head and tail
                        tail = (tail+1) % zone_count
                        head = (head+1) % zone_count

                        if tail >= WINNER_TILE_FROM and tail <= WINNER_TILE_TO:
                            strip.set_zone_color(WINNER_TILE_FROM, WINNER_TILE_TO, random.choice(randomColours), 20, True, 1)
                            background_color = random.choice(randomColours)
                        else:
                            strip.set_zone_color(WINNER_TILE_FROM, WINNER_TILE_TO, background_color, 0, True, 1)

        except KeyboardInterrupt:
            return


# Flash some green :)
def goodLights():

    lifx = LifxLAN(int(1),False)
    devices = lifx.get_lights()
    bulb = devices[0]
    bulb.set_color(GREEN)

    def toggle_device_power(device, interval=0.5, num_cycles=3):
        rapid = True if interval < 1 else False
        for i in range(num_cycles):
            device.set_power("on", rapid)
            sleep(interval)
            device.set_power("off", rapid)
            sleep(interval)
            device.set_power("on", rapid)

    def toggle_light_color(light, interval=1, num_cycles=1):
        rapid = True if interval < 1 else False
        for i in range(num_cycles):
            light.set_color(GREEN, rapid=rapid)

        toggle_device_power(bulb, 0.2)
        toggle_light_color(bulb, 0.2)

# Flash some red :(
def badLights():

    lifx = LifxLAN(int(1),False)
    devices = lifx.get_lights()
    bulb = devices[0]
    bulb.set_color(RED)

    def toggle_device_power(device, interval=0.5, num_cycles=3):
        rapid = True if interval < 1 else False
        for i in range(num_cycles):
            device.set_power("on", rapid)
            sleep(interval)
            device.set_power("off", rapid)
            sleep(interval)
            device.set_power("on", rapid)

    def toggle_light_color(light, interval=1, num_cycles=1):
        rapid = True if interval < 1 else False
        for i in range(num_cycles):
            light.set_color(RED, rapid=rapid)

        toggle_device_power(bulb, 0.2)
        toggle_light_color(bulb, 0.2)

# Flash some rainbow :))
def completeLights():

    lifx = LifxLAN(int(1),False)
    devices = lifx.get_lights()
    bulb = devices[0]

    # get original state
    print("Turning on all lights...")
    original_power = bulb.get_power()
    original_color = bulb.get_color()
    bulb.set_power("on")

    print("Flashy fast rainbow")
    rainbow(bulb, 0.1)

    print("Smooth slow rainbow")
    rainbow(bulb, 1, smooth=True)

    print("Restoring original power and color...")
    # restore original power
    bulb.set_power(original_power)
    # restore original color
    sleep(0.5) # for looks
    bulb.set_color(original_color)

def rainbow(bulb, duration_secs=0.5, smooth=False):
    colors = [RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, PURPLE, PINK]
    transition_time_ms = duration_secs*1000 if smooth else 0
    rapid = True if duration_secs < 1 else False
    for color in colors:
        bulb.set_color(color, transition_time_ms, rapid)
        sleep(duration_secs)

# Setup
if __name__ == "__main__":
    SNAKE = Mob()
    main()
    goodLights()
    completeLights()