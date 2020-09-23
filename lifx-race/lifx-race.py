#!/usr/bin/env python3
# coding=utf-8
import sys
import random
from lifxlan import LifxLAN, \
    BLUE, COLD_WHITE, CYAN, GOLD, GREEN, ORANGE, PINK, PURPLE, RED, WARM_WHITE, WHITE, YELLOW
from pynput.keyboard import Listener, Key
from copy import deepcopy
from time import sleep 
import threading
import pyttsx3

space_pressed = False
race_won = False

def keyboard_listener():
    global space_pressed
    
    def on_press(key): 
        global space_pressed
        if key == Key.space:
            if space_pressed:
                space_pressed = False
            else:
                space_pressed = True

    with Listener(on_press=on_press) as listener:  # Create an instance of Listener
        listener.join()  # Join the listener thread to the main thread to keep waiting for keys

def lightDiscovery():
    global space_pressed
    global race_won
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
        start_position = 1
        player_size = 1
        background_colour = [0,0,0,2500]
        flag_colour = GOLD
        transition_duration = 0
        colours = [[BLUE,ORANGE],[GREEN,PURPLE],[PINK,WHITE],[RED,YELLOW]]

        def race_introductions(player_name):
            race_introductions = [
                player_name+", you're up next", 
                player_name+", you're up!", 
                player_name+", are you oiled and primed?", 
                player_name+", this could be the race of legends.", 
                "Your turn next, "+player_name,
                "Get your fingers ready, "+player_name,
                "Can you feel victory, "+player_name,
                "On your marks " + player_name + " you're next.",
                "go "+player_name
            ]
            return random.choice(race_introductions)

        def winner_announcements(player_name):
            winner_announcements = [
                "Stop the race! We have a Winner! Congratulations "+player_name+". You have Won.",
                player_name + " " + player_name + " " + player_name + " " + player_name + " " + "You are the winner. Congratulations."
            ]
            return random.choice(winner_announcements)

        # Player Object
        class Player:
            def __init__(self, name):
                self.name = name
                self.colour = WHITE
                self.checkpoint_colour = WHITE
                self.position = start_position
                self.direction = "forwards"                
                self.indicator = self.position
                self.speed = 0.2
                self.race_size = 5
                self.fallback_distance = 1

            def randomRaceConditions(self):
                self.randomDirection()
                self.randomSpeed()
                self.randomRaceSize()
                self.randomFallbackDistance()

            def randomDirection(self):
                self.direction = random.choice(["forwards","backwards"])

            def randomSpeed(self):
                self.speed = random.choice([0.15,0.14,0.12,0.11,0.1,0.08,0.06,0.05])

            def randomRaceSize(self):
                self.race_size = random.choice([2,3,4,5])

            def randomFallbackDistance(self):
                self.fallback_distance = random.choice([0,1])

        # Player variables
        players = [Player("Adam"),Player("Oliver"),Player("Jamie")]

        # Assign player colours
        i = 0
        while i < len(players):
            print(players[i].name, " is ", colours[i][0])
            players[i].colour = colours[i][0]
            players[i].checkpoint_colour = colours[i][1]
            i += 1


        # Set background colour and end flag
        strip.set_color(background_colour)
        strip.set_zone_color(zone_count-1, zone_count-1, flag_colour, transition_duration)

        engine = pyttsx3.init()
        engine.say("On your marks, Get set, Go")
        engine.runAndWait()

        try:
            while True:

                if race_won:
                    print("Race Won")
                    break

                for player in players:
                    print(player.name, " loop started")
                    player.randomRaceConditions()
                    strip.set_color(background_colour)
                    engine = pyttsx3.init()
                    engine.say(race_introductions(player.name))
                    engine.runAndWait()
                    
                    while True:
                        if space_pressed:
                            print("Loop Stopped")
                            space_pressed = False
                            break

                        race_start_position = max(player.position - player.fallback_distance,0)
                        race_checkpoint_position = min(player.position + player.race_size, zone_count)

                        print(player.name, player.direction, player.position, player.indicator, " | ", race_start_position, " - ", race_checkpoint_position, "Race Conditions: ", player.speed, player.race_size, player.fallback_distance)
                        
                        # Background
                        strip.set_zone_color(race_start_position,max(player.indicator-1, 0), background_colour, 0, rapid=True, apply=1)
                        strip.set_zone_color(min(player.indicator+1,zone_count),race_checkpoint_position,background_colour, 1, rapid=True, apply=1)
                        
                        # Other player indicator
                        for competingPlayer in players:
                            if competingPlayer.name != player.name:
                                strip.set_zone_color(competingPlayer.position, competingPlayer.position, competingPlayer.colour, 0, rapid=True, apply=1)

                        # Checkpoint & Start
                        strip.set_zone_color(min(race_checkpoint_position+1,zone_count),min(race_checkpoint_position+1, zone_count), player.checkpoint_colour, 0, rapid=True, apply=1)
                        strip.set_zone_color(max(race_start_position-1,0),max(race_start_position-1, 0), player.checkpoint_colour, 0, rapid=True, apply=1)
            
                        # Player indicator
                        strip.set_zone_color(player.indicator, min(player.indicator+player_size-1,1), player.colour, transition_duration, rapid=True, apply=1)

                        # Check if the indicator is about to escape the raze zone
                        if all([player.direction == "forwards", player.indicator + 1 > race_checkpoint_position]):
                            player.direction = "backwards"

                        if all([player.direction == "backwards", player.indicator - 1 < race_start_position]):
                            player.direction = "forwards"

                        # Move the indicator in the correct direction by one 
                        if player.direction == "forwards":
                            player.indicator += 1

                        if player.direction == "backwards":
                            player.indicator -= 1

                        sleep(player.speed)
                    print("Race loop ended")
                    
                    player.position = player.indicator

                    if player.position >= 30:
                        strip.set_zone_color(0,zone_count, background_colour, 0)
                        strip.set_zone_color(0,zone_count, player.colour, 5000)
                        race_won = True
                        engine = pyttsx3.init()
                        engine.say(winner_announcements(player.name))
                        engine.runAndWait()
                        break
        
        
                    strip.set_color(background_colour,500)
                    
                    topPlayer = players[0]

                    # Other player indicator
                    for competingPlayer in players:
                        strip.set_zone_color(competingPlayer.position, competingPlayer.position, competingPlayer.colour, 0, rapid=True, apply=1)
                        if competingPlayer.position > topPlayer.position:
                            topPlayer = competingPlayer
                
                    engine = pyttsx3.init()
                    engine.say( topPlayer.name + " is in the lead")
                    engine.runAndWait()

                    sleep(1.5)
                    strip.set_color(background_colour,100)
                    sleep(0.5)
                    continue
                print("layer loop ended")

        except KeyboardInterrupt:
            # Reset colours to original when the script is stopped
            strip.set_zone_colors(original_zones, 500, True)

def main():
    thread2 = threading.Thread(target=keyboard_listener, args=())
    thread2.start()
    lightDiscovery()

if __name__=="__main__":
    main()