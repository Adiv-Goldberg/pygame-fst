""" 
about_menu.py
Author: Adiv Goldberg
Date last edited: 2025-06-09
Program: platformer about menu
Description:
-------------
This module implements the about menu for the platformer game. It provides information about the game, including:
- Game title and description.
- Author information.
- Controls and instructions.
- Back button to return to the main menu.
"""
# import the pygame module
import pygame
import tools
import main_menu

# initializes the pygame module
pygame.init()

# creates a screen variable of size 800 x 600
screen = pygame.display.set_mode([tools.SCREEN_X,tools.SCREEN_Y])

# controls the main game while loop
done = False

# sets the frame rate of the program
clock = pygame.time.Clock()

# your GLOBAL variables go here
menu_background = pygame.image.load("about menu.png").convert_alpha() # Load the background image for the about menu
menu_background = pygame.transform.scale(menu_background, (tools.SCREEN_X, tools.SCREEN_Y)) # Scale the background to fit the screen


# MAIN LOOP
def run_about_menu():
    global done
    screen.blit(menu_background, (0, 0)) # Draw the background image onto the screen

    main_menu.input_info, done = tools.check_input() # Check for user input and update the input_info and done variables
     
    screen.blit(main_menu.back_button, main_menu.back_button_pos) # Draw the back button onto the screen
    main_menu.back_button_collide(main_menu.back_button_pos, 50, "main_menu", main_menu.input_info.left_mouse_down, main_menu.input_info.xMouse, main_menu.input_info.yMouse) # Check if the back button is clicked and change the game state to main_menu if it is

    # this line draws everything into the window all at once
    pygame.display.flip()
    # this line limits the frames per second to 60
    clock.tick(60)
    
    return done

if __name__ == "__main__": # Run the about menu if this module is run directly
    while not done:
        run_about_menu()
    pygame.quit()