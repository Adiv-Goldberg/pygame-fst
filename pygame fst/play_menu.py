""" 
play_menu.py
Author: Adiv Goldberg
Date last edited: 2025-06-09
Program: platformer play menu
Description:
-------------
This module implements the play menu for the platformer game. It provides a user-friendly interface for accessing different gameplay options, including:
- Start game button to begin a new game session.
- Load game button to continue a previously saved game.
- Options button to adjust game settings such as audio and controls.
- Back button to return to the main menu.
"""
# import the pygame module
import pygame
import skin_shop
import tools
import main_menu
from main_menu import Menu_Buttons

# will make it easier to use pygame functions
import gameplay

# initializes the pygame module
pygame.init()

# creates a screen variable of size 800 x 600
screen = pygame.display.set_mode([tools.SCREEN_X,tools.SCREEN_Y])

# controls the main game while loop
done = False

# sets the frame rate of the program
clock = pygame.time.Clock()

#CLASSES
class Deafault_Levels:
    def __init__(self, x, y, img, level, length, completed, best_time):
        """ Initializes a level square with the specified attributes.

        Args:
            x (float): The x-coordinate of the level square.
            y (float): The y-coordinate of the level square.
            img (Surface): The image representing the level square.
            level (int): The level number.
            length (float): The length of the level square.
            completed (bool): Whether the level is completed.
            best_time (float): The best time for completing the level.
        """
        self.x = x
        self.y = y
        self.length = length
        self.img = pygame.transform.scale(img, (self.length, self.length))
        self.completed = completed
        self.best_time = best_time
        self.level_num = level
        
    def go(self):
        """
        Run the main actions for the level square.
        """
        self.draw()
        self.selection()
    
    def draw(self):
        """Draw the level square on the screen.
        """
        global checkmark_img
        screen.blit(self.img, (self.x, self.y))
        if self.completed:
            if self.best_time is not None: # If the level is completed
                time_text = skin_shop.retro_font_15.render(f"{round(self.best_time,1)} s", True, tools.BLACK) # Render the best time text
                screen.blit(time_text, (self.x + self.length // 2 - time_text.get_width() // 2, self.y + self.length + 5)) #blit it
            screen.blit(checkmark_img, (self.x + self.length - 24, self.y)) # Draw the checkmark in the top right corner of the square
        
        # Draw the level number centered in the square
        level_text = gameplay.retro_font_32.render(str(self.level_num), True, tools.WHITE)
        screen.blit(level_text, (self.x + self.length // 2 - level_text.get_width() // 2, self.y + self.length // 2 - level_text.get_height() // 2))
                    
    def selection(self):
        """Handles the selection of the level square.
        """
        if pygame.Rect(self.x, self.y, self.length, self.length).collidepoint((main_menu.input_info.xMouse, main_menu.input_info.yMouse)) and main_menu.input_info.left_mouse_down: # If the mouse is over the level square and clicked
            gameplay.load_level(f"level {self.level_num}.adiv") # Load the level file
            tools.game_state = "gameplay" # Change the game state to gameplay
        



# your FUNCTIONS go here
def level_grid(c_levels):
    """Creates a grid of level squares for the play menu.

    Args:
        c_levels (dict): A dictionary containing the completed levels and their best times.

    Returns:
        list: A list of Level instances representing the level squares.
    """
    global level_outline_img
    # Create a 5x4 grid of Level instances on the left of the screen
    levels = []
    level_width = 60
    level_height = 60
    xpadding = 25
    ypadding = 25
    start_x = 70
    start_y = 175

    for row in range(4):
        for col in range(5):
            x = start_x + col * (level_width + xpadding) # Calculate x position based on column
            y = start_y + row * (level_height + ypadding) # Calculate y position based on row
            level_number = row * 5 + col + 1 # Calculate level number (1 to 20)
            completed = False # Default to not completed
            if f"level {level_number}.adiv" in c_levels: # Check if the level file exists in the completed levels
                completed = True # If it exists, set completed to True
            best_time = float("inf") # Default best time to infinity
            if completed: # If the level is completed
                best_time = c_levels[f"level {level_number}.adiv"] # get the best time from the dictionary
            levels.append(Deafault_Levels(x, y, level_outline_img, level_number, level_width, completed, best_time)) # Append the level instance to the list
    return levels

def get_level_class():
    """Updates the global levels variable with the current level instances.
    """
    global levels
    _, tools.complete_levels, _, _ = tools.read_stats() # Read the completed levels from stats
    levels = level_grid(tools.complete_levels) # Create the level grid based on completed levels
    
def total_time():
    """Calculates the total time taken to complete all levels.

    Returns:
        pygame.Surface: A text surface displaying the total time.
    """
    global levels 
    time = 0
    for level in levels: # Iterate through each level in the levels list
        if level.best_time != float("inf"): # If the level has a valid best time
            time += level.best_time # Add the best time to the total time
    return gameplay.retro_font_32.render(f"your total time is: {round(time, 1)} s", True, tools.BLACK) # Render the total time as a text surface

def update_play_menu():
    """Updates the play menu with the current level instances and total time.
    """
    global levels, net_time_label
    tools.coins, tools.complete_levels, _, _ = tools.read_stats() # Read the coins and completed levels from stats
    levels = level_grid(tools.complete_levels) # Update the levels variable with the current level instances
    net_time_label = total_time() # Update the total time label with the new total time
    tools.game_state = "play_menu" # Change the game state to play_menu


# your GLOBAL variables go here
menu_background = pygame.image.load("play menu.png").convert_alpha() # Load the play menu background image
menu_background = pygame.transform.scale(menu_background, (tools.SCREEN_X, tools.SCREEN_Y)) # Scale the background to fit the screen

level_e_img = pygame.image.load("menu icons/level editor white.png").convert_alpha() # Load the level editor button image
level_e_length = 125 # Set the length of the level editor button
level_e_img = pygame.transform.scale(level_e_img, (level_e_length,level_e_length)) # Scale the level editor button image to the specified length

pm_buttons = [ # List of Menu_Buttons instances for the play menu
    Menu_Buttons(584, 279,level_e_img, 4, level_e_length), #level editor button, type 4
]

level_outline_img = pygame.image.load("menu icons/level outline.png").convert_alpha() # Load the level outline image
checkmark_img = pygame.image.load("check-mark.png").convert_alpha() # Load the checkmark image
checkmark_img = pygame.transform.scale(checkmark_img, (24, 24)) # Scale the checkmark image to the specified size

levels = []
get_level_class() # Initialize the levels variable with the current level instances

net_time_label = total_time() # Update the total time label with the new total time



# MAIN LOOP
def run_play_menu(): #while loop function for the play menu
    global screen, menu_background, level_e_img, level_e_length, pm_buttons, done, clock, done
    screen.blit(menu_background, (0, 0)) # Draw the play menu background
    
    main_menu.input_info, done = tools.check_input() # Check for user input and update the done variable

    screen.blit(main_menu.back_button, main_menu.back_button_pos) # Draw the back button on the screen
    main_menu.back_button_collide(main_menu.back_button_pos, 50, "main_menu", main_menu.input_info.left_mouse_down, main_menu.input_info.xMouse, main_menu.input_info.yMouse) # Check for collision with the back button and change the game state to main_menu if clicked
        
    tools.cloud_x = tools.draw_clouds(tools.cloud_img, tools.cloud_x) # Draw the clouds on the play menu background

    for button in pm_buttons: 
        button.go() # Call the go method for each button in the pm_buttons list to handle their actions
        
    for level in levels:
        level.go() # Call the go method for each level in the levels list to draw and handle their functionality
        
    screen.blit(net_time_label, (270 - net_time_label.get_width()*0.5, 510)) # Draw the total time label centered at the bottom of the screen
    
    # this line draws everything into the window all at once
    pygame.display.flip()
    # this line limits the frames per second to 60
    clock.tick(60)
    
    return done

if __name__ == "__main__":  # Run the play menu if this module is run directly
    while not done:
        run_play_menu()
    pygame.quit()