#!/usr/bin/env python3
# coding=utf-8
import sys
import random
from lifxlan import LifxLAN, \
    BLUE, COLD_WHITE, CYAN, GOLD, GREEN, ORANGE, PINK, PURPLE, RED, WARM_WHITE, WHITE, YELLOW
from pynput.keyboard import Listener, Key
from copy import deepcopy
from time import sleep

def lightDiscovery():
    # Discover lights
    print("Discovering lights...")
    lifx = LifxLAN(None,False)
    lifx.set_power_all_lights("on", duration=1000, rapid=True)

    # Get devices
    multizone_lights = lifx.get_multizone_lights()

    if len(multizone_lights) > 0:
        strip = multizone_lights[0]
        print("Selected {}".format(strip.get_label()))

        # Light Stuff
        all_zones = strip.get_color_zones()
        original_zones = deepcopy(all_zones)
        zone_count = len(all_zones)

        # Options
        colour_options = [BLUE, COLD_WHITE, CYAN, GOLD, GREEN, ORANGE, PINK, PURPLE, RED, WARM_WHITE, WHITE, YELLOW]
        starting_color = YELLOW
        current_color = starting_color
        background_color = WHITE

        # User Stuff
        user_zone_size = zone_count/6 # length of snake in zones
        current_user_zone_start = (zone_count/2) - (user_zone_size/2)
        current_user_zone_end = current_user_zone_start + user_zone_size

        try:
            while True:
                strip.set_color(background_color)
                strip.set_zone_color(current_user_zone_start, current_user_zone_end, current_color, 500)
                    
                def on_press(key):  # The function that's called when a key is released                    
                    nonlocal current_user_zone_start
                    nonlocal current_user_zone_end
                    nonlocal current_color
                    nonlocal background_color

                    # Get new colour
                    new_color = random.choice(colour_options)
                    while new_color == current_color:
                        new_color = random.choice(colour_options)

                    # If up key is pressed increase the snake size by 1
                    if key == Key.up:
                        current_user_zone_end = min(current_user_zone_end + 1,zone_count)
                        strip.set_zone_color(current_user_zone_start, current_user_zone_end, current_color,200)
                        strip.set_zone_color(0, current_user_zone_start, background_color,200)
                        strip.set_zone_color(current_user_zone_end, zone_count, background_color,200)

                    # If down key is pressed decrease the snake size by 1
                    if key == Key.down:
                        current_user_zone_end = min(current_user_zone_end - 1, zone_count)
                        strip.set_zone_color(current_user_zone_start, current_user_zone_end, current_color,200)
                        strip.set_zone_color(0, current_user_zone_start, background_color,200)
                        strip.set_zone_color(current_user_zone_end, zone_count, background_color,200)

                    # If left arrow key is pressed move the snake left 1
                    if key == Key.left:
                        current_user_zone_start = min(current_user_zone_start + 1, zone_count)
                        current_user_zone_end = min(current_user_zone_end + 1,zone_count)
                        strip.set_zone_color(current_user_zone_start, current_user_zone_end, current_color,200)
                        strip.set_zone_color(0, current_user_zone_start, background_color,200)
                        strip.set_zone_color(current_user_zone_end, zone_count, background_color,200)

                    # If right arrow key is pressed move the snake right 1
                    if key == Key.right:
                        current_user_zone_start = max(current_user_zone_start - 1, 0)
                        current_user_zone_end = max(current_user_zone_end - 1, 0)
                        strip.set_zone_color(current_user_zone_start, current_user_zone_end, current_color,500)
                        strip.set_zone_color(0, current_user_zone_start, background_color,500)
                        strip.set_zone_color(current_user_zone_end, zone_count, background_color,500)

                def on_release(key):  # The function that's called when a key is pressed
                    print("Key released: {0}.".format(key))

                    # If space key is pressed change the snake colour
                    if key == Key.space:
                        print("Space pressed, new color: {0}".format(new_color))
                        strip.set_zone_color(current_user_zone_start, current_user_zone_end, new_color, 500)
                        current_color = new_color
                        # strip.set_color(new_color)

                    # If down right shift key is pressed change the background colour
                    if key == Key.shift_r:
                        strip.set_zone_color(0, current_user_zone_start, new_color,1000)
                        strip.set_zone_color(current_user_zone_end, zone_count, new_color,1000)
                        background_color = new_color

                with Listener(on_press=on_press, on_release=on_release) as listener:  # Create an instance of Listener
                    listener.join()  # Join the listener thread to the main thread to keep waiting for keys


                # try:
                #     while True:
                #         # Case 1: Snake hasn't wrapped around yet
                #         if head > tail:
                #             if tail > 0:
                #                 strip.set_zone_color(0, tail-1, background_color, 0, True, 0)
                #             strip.set_zone_color(tail, head, snake_color, 0, True, 0)
                #             if head < zone_count - 1:
                #                 strip.set_zone_color(head+1, zone_count-1, background_color, 0, True, 1)

                #         # Case 2: Snake has started to wrap around
                #         else:
                #             if head > 0:
                #                 strip.set_zone_color(0, head-1, snake_color, 0, True, 0)
                #             strip.set_zone_color(head, tail, background_color, 0, True, 0)
                #             if tail < zone_count - 1:
                #                 strip.set_zone_color(tail+1, zone_count-1, snake_color, 0, True, 1)

                #         sleep(delay)

        except KeyboardInterrupt:
            # Reset colours to original when the script is stopped
            strip.set_zone_colors(original_zones, 500, True)

if __name__=="__main__":
    lightDiscovery()