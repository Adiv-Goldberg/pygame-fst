""" 
main.py
Author: Adiv Goldberg
Date last edited: 2025-06-09
Program: platformer main module
Description:
-------------
This module implements the main functionality for the platformer game. It provides a user-friendly interface for accessing different game modes, including:
- A main menu for starting the game or accessing other options.
- A gameplay mode for playing the game.
- A level editor for creating and editing levels.
- A play menu for selecting and starting levels.
- An about menu for displaying information about the game.
- A skin shop for customizing the player's character.
"""
# import the pygame module
import pygame
import gameplay, level_editor, main_menu, play_menu, level_editor_menu, about_menu, skin_shop
import tools

# initializes the pygame module
pygame.init()

# creates a screen variable of size 800 x 600
screen = pygame.display.set_mode([tools.SCREEN_X,tools.SCREEN_Y])

# controls the main game while loop
done = False

# sets the frame rate of the program
clock = pygame.time.Clock()

# your GLOBAL variables go here

pygame.mixer.music.load("sound/music/intro Theme.mp3")

pygame.display.set_caption("Adiv's Platformer")

if __name__ == "__main__": # if this is the file its being run from, then run the main loop
    # MAIN LOOP
    while not done:
        # makes the background the colour WHITE
        screen.fill(tools.WHITE)

        #run different files depending on the game state
        if tools.game_state == "main_menu":
            done = main_menu.run_main_menu()
        elif tools.game_state == "gameplay":
            done = gameplay.run_gameplay()
        elif tools.game_state == "update_play_menu":
            done = play_menu.update_play_menu()
        elif tools.game_state == "play_menu":
            done = play_menu.run_play_menu()
        elif tools.game_state == "level_editor":
            done = level_editor.run_level_editor()
        elif tools.game_state == "level_editor_menu":
            done = level_editor_menu.run_level_editor_menu()
        elif tools.game_state == "about_menu":
            done = about_menu.run_about_menu()
        elif tools.game_state == "skin_shop":
            done = skin_shop.run_skin_shop()
        
        # if its in the listed game states or level complete is playing, play the music, otherwise stop it
        if tools.game_state in ["main_menu", "play_menu", "about_menu", "level_editor_menu", "skin_shop"] and not gameplay.level_complete_se.get_num_channels():
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(-1)
        else:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
    pygame.quit()