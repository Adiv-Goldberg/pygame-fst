""" 
level_editor_menu.py
Author: Adiv Goldberg
Date last edited: 2025-06-09
Program: platformer level editor
Description:
-------------
This module implements the level editor for the platformer game. It provides a user-friendly interface for creating and editing levels, including:
- A grid of tiles to place and manipulate.
- Tools for adding, removing, and modifying tiles.
- A button to save the current level.
- Back button to return to the main menu.
"""
# import the pygame module
import pygame
import tools
import main_menu
from main_menu import Menu_Buttons

# initializes the pygame module
pygame.init()

# creates a screen variable of size 800 x 600
screen = pygame.display.set_mode([tools.SCREEN_X,tools.SCREEN_Y])

# controls the main game while loop
done = False

# sets the frame rate of the program
clock = pygame.time.Clock()

# your GLOBAL variables go here
menu_background = pygame.image.load("level editor menu.png").convert_alpha() # Load the background image for the level editor menu
menu_background = pygame.transform.scale(menu_background, (tools.SCREEN_X, tools.SCREEN_Y)) # Scale the background to fit the screen

play_img = pygame.image.load("menu icons/play circle.png").convert_alpha() # Load the play button image
play_length = 225
play_img = pygame.transform.scale(play_img, (play_length,play_length)) # Scale the play button image to fit the button size

new_img = pygame.image.load("menu icons/new white.png").convert_alpha() # Load the new level button image
new_length = 125
new_img = pygame.transform.scale(new_img, (new_length,new_length)) # Scale the new level button image to fit the button size

load_img = pygame.image.load("menu icons/load white.png").convert_alpha() # Load the load level button image
load_length = 125
load_img = pygame.transform.scale(load_img, (load_length,load_length)) # Scale the load level button image to fit the button size

lem_buttons = [ # List of buttons for the level editor menu
    Menu_Buttons(281, 217,play_img, 5, play_length), #play button, type 5
    Menu_Buttons(62, 301,new_img, 6, new_length), #edit new button, type 6
    Menu_Buttons(613, 296,load_img, 7, load_length) #load and edit button, type 7
]


# MAIN LOOP
def run_level_editor_menu(): #while loop for the level editor menu
    global screen, menu_background, play_img, play_length, new_img, new_length, load_img, load_length, lem_buttons, done
    
    screen.blit(menu_background, (0, 0)) # Draw the background image onto the screen
        
    tools.cloud_x = tools.draw_clouds(tools.cloud_img, tools.cloud_x) # Draw clouds on the screen and update their position

    main_menu.input_info, done = tools.check_input() # Check for user input and update the input_info and done variables
    
    screen.blit(main_menu.back_button, main_menu.back_button_pos) # Draw the back button onto the screen
    main_menu.back_button_collide(main_menu.back_button_pos, 50, "play_menu", main_menu.input_info.left_mouse_down, main_menu.input_info.xMouse, main_menu.input_info.yMouse) # Check if the back button is clicked and change the game state to play_menu if it is
    
    for button in lem_buttons:
        button.go() # Call the go method for each button in the lem_buttons list to handle their actions

    # this line draws everything into the window all at once
    pygame.display.flip()
    # this line limits the frames per second to 60
    clock.tick(60)
    
    return done
    
if __name__ == "__main__": # Run the level editor menu if this module is run directly
    while not done:
        run_level_editor_menu()
    pygame.quit()