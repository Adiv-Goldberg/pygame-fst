""" 
main_menu.py
Author: Adiv Goldberg
Date last edited: 2025-06-09
Program: platformer main menu
Description:
-------------
This module implements the main menu and navigation system for the platformer level editor. It provides a user-friendly interface for accessing different sections of the program, including:
- Main menu with options to play the game, access information, visit the in-game shop, and enter the level editor.
- Button classes for interactive menu elements with distinct actions.
- File handling integration allowing users to load existing levels directly from the main menu for gameplay or editing.
- Background and visual elements for an engaging main menu experience.
"""
# import the pygame module
import pygame

# will make it easier to use pygame functions
import gameplay
import level_editor
import tools
import tkinter as tk
from tkinter import filedialog

# initializes the pygame module
pygame.init()

# creates a screen variable of size 800 x 600
screen = pygame.display.set_mode([tools.SCREEN_X,tools.SCREEN_Y])

# controls the main game while loop
done = False

# sets the frame rate of the program
clock = pygame.time.Clock()

#CLASSES
class Menu_Buttons:
    def __init__(self, x, y, img, type, length):
        """
        Initializes a menu button with the specified attributes.

        Args:
            x (int): The x-coordinate of the button.
            y (int): The y-coordinate of the button.
            img (pygame.Surface): The image representing the button.
            type (int): The type of the button (e.g., play, settings).
            length (int): The length/width of the button (assuming square buttons).
        """
        self.x = x
        self.y = y
        self.img = img
        self.type = type
        self.length = length
    
    def go(self):
        """Handles the button's functionality when clicked.
        """
        self.draw()
        self.selection()
    
    def draw(self):
        """Draws the button on the screen.
        """
        screen.blit(self.img, (self.x, self.y))
        
    def selection(self):
        """Handles the button's selection logic.
        """
        if input_info.left_mouse_down and pygame.Rect(self.x, self.y, self.length, self.length).collidepoint(input_info.xMouse, input_info.yMouse): # if clicked
            if self.type in [5,7]: #if its load/edit or load a play level
                root = tk.Tk()
                root.withdraw()
                file_path = filedialog.askopenfilename( #Open file selector
                    defaultextension=".adiv",  # Default file extension for opened files
                    filetypes=[("Adiv Level Files", "*.adiv"), ("All Files", "*.*")],  # File type filters
                    title="Open Level File"  # Dialog window title
                )
                root.destroy()

                if self.type == 5 and file_path[-5:] == ".adiv": #load and play the level
                    gameplay.load_level(file_path)
                    tools.game_state = "gameplay"
                elif self.type == 7: #load and edit the level
                    level_editor.load_level_e(file_path)
                    tools.game_state = "level_editor"
            
            elif self.type == 1: #if its the play button
                tools.game_state = "play_menu"
            elif self.type == 2: #if its the about button
                tools.game_state = "about_menu"
            elif self.type == 3: #if its the shop button
                tools.game_state = "skin_shop"
            elif self.type == 4: #if its the level editor button
                tools.game_state = "level_editor_menu"
            elif self.type == 6: #if its the new level button
                level_editor.load_level_e(None)
                tools.game_state = "level_editor"
    
        



# your FUNCTIONS go here
def back_button_collide(pos, len, change_to, lm, xm, ym):
    """Checks for collision between the back button and the mouse cursor.

    Args:
        pos (tuple): The (x, y) position of the button.
        len (int): The length/width of the button (assuming square buttons).
        change_to (str): The game state to change to when the button is clicked.
        lm (bool): Whether the left mouse button is pressed.
        xm (int): The x-coordinate of the mouse cursor.
        ym (int): The y-coordinate of the mouse cursor.

    Returns:
        bool: True if the button is clicked, False otherwise.
    """
    x, y = pos
    collide = lm and pygame.Rect(x,y,len,len).collidepoint(xm, ym) # if the left mouse button is pressed and the mouse is over the button
    if collide:
        tools.game_state = change_to # change the game state to the specified one
    return collide

# your GLOBAL variables go here
menu_background = pygame.image.load("main menu.png").convert_alpha() # Load the main menu background image
menu_background = pygame.transform.scale(menu_background, (tools.SCREEN_X, tools.SCREEN_Y)) #scale it

play_img = pygame.image.load("menu icons/play circle.png").convert_alpha() # Load the play button image
play_length = 225
play_img = pygame.transform.scale(play_img, (play_length,play_length)) # Scale the play button image to the specified length

settings_img = pygame.image.load("menu icons/info white.png").convert_alpha() # Load the settings button image
settings_length = 125
settings_img = pygame.transform.scale(settings_img, (settings_length,settings_length)) # Scale the settings button image to the specified length

shop_img = pygame.image.load("menu icons/shop white.png").convert_alpha() # Load the shop button image
shop_length = 125
shop_img = pygame.transform.scale(shop_img, (shop_length,shop_length)) # Scale the shop button image to the specified length

mm_buttons = [ # List of menu buttons with their positions, images, types, and lengths into the class
    Menu_Buttons(279, 229,play_img, 1, play_length), #play button, type 1
    Menu_Buttons(72, 311,settings_img, 2, settings_length), #settings button, type 2
    Menu_Buttons(590, 304,shop_img, 3, shop_length) #shop button, type 3
]

back_button = pygame.image.load("menu icons/undo.png").convert_alpha() # Load the back button image
back_button = pygame.transform.scale(back_button, (50, 50)) # Scale the back button images
back_button_pos = (15, 15)

input_info = None #user inputs

# MAIN LOOP
def run_main_menu():
    global screen, menu_background, mm_buttons, input_info, done, clock
    screen.blit(menu_background, (0, 0)) # Draw the main menu background
    
    tools.cloud_x = tools.draw_clouds(tools.cloud_img, tools.cloud_x) # Draw the clouds on the main menu background
    
    input_info, done = tools.check_input() # Check for user inputs and update the input_info variable

    for button in mm_buttons: 
        button.go() # Call the go method of each button in the mm_buttons list to draw and handle their functionality

    # this line draws everything into the window all at once
    pygame.display.flip()
    # this line limits the frames per second to 60
    clock.tick(60)
    
    return done
        
if __name__ == "__main__": #run program if in main module for testing
    while not done:
        run_main_menu()
    pygame.quit()