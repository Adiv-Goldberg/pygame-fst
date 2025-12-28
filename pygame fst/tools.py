""" 
tools.py
Author: Adiv Goldberg
Date last edited: 2025-06-09
Program: platformer tools module
Description:
-------------
This module provides utility functions and classes for the platformer game, including:
- Functions for loading and managing game assets (images, sounds, etc.).
- Classes for representing game objects (players, enemies, items, etc.).
- Functions for handling user input and game events.
- middle man file to avoid circular dependencies between modules
"""
# import the pygame module
import pygame
import json

# colour variables, (R, G, B) from 0-255
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

# initializes the pygame module
pygame.init()
SCREEN_X, SCREEN_Y = (800, 600)
screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))

class Status_Info:
    def __init__(self, keys, mouse_pos, just_jumped, left_mouse_down, right_mouse_down, h_Lmouse, h_Rmouse):
        """Initializes the status information for the player.

        Args:
            keys (list): The current state of all keyboard keys.
            mouse_pos (tuple): The current position of the mouse cursor.
            just_jumped (bool): Whether the player just jumped.
            left_mouse_down (bool): Whether the left mouse button is currently pressed.
            right_mouse_down (bool): Whether the right mouse button is currently pressed.
            h_Lmouse (bool): Whether the left mouse button was held down.
            h_Rmouse (bool): Whether the right mouse button was held down.
        """
        if keys[pygame.K_RIGHT]: # Check if the right arrow key is pressed
            self.R_pressed = True # Set the right arrow key state to pressed
        else: # If the right arrow key is not pressed
            self.R_pressed = False # Set the right arrow key state to not pressed
            
        if keys[pygame.K_LEFT]: # Check if the left arrow key is pressed
            self.L_pressed = True # Set the left arrow key state to pressed
        else: # If the left arrow key is not pressed
            self.L_pressed = False  # Set the left arrow key state to not pressed
            
        self.left_mouse_down = left_mouse_down # Store the state of the left mouse button
        
        self.right_mouse_down = right_mouse_down # Store the state of the right mouse button
        
        self.xMouse, self.yMouse = mouse_pos # Store the current position of the mouse cursor
                
        self.just_jumped = just_jumped # Store whether the player just jumped
        
        self.holding_Lmouse = h_Lmouse # Store whether the left mouse button was held down
        self.holding_Rmouse = h_Rmouse # Store whether the right mouse button was held down


def check_input():
    """Checks for user input and returns the status information.

    Returns:
        Status_Info: The current status information for the player.
    """
    keys =  pygame.key.get_pressed() # Get the current state of all keyboard keys
    mouse_pos = pygame.mouse.get_pos()   # Get the current position of the mouse cursor
    clicks = pygame.mouse.get_pressed() # Get the current state of mouse buttons (left, middle, right)
    
    h_Lmouse = clicks[0] # Check if the left mouse button is held down
    h_Rmouse = clicks[2] # Check if the right mouse button is held down

    done = False # assume the loop is not done
    just_jumped = False # assume the player has not just jumped
    left_mouse_down = False # assume the left mouse button is not pressed
    right_mouse_down = False # assume the right mouse button is not pressed
    for event in pygame.event.get(): # Loop through all events in the event queue
        if event.type == pygame.QUIT: # If the quit event is triggered (e.g., window close button clicked)
            done = True # Set done to True to exit the loop
        if event.type == pygame.KEYDOWN: # If a key is pressed down
            if event.key == pygame.K_SPACE: # If the space key is pressed
                just_jumped = True # Set just_jumped to True to indicate the player has jumped
            if event.key == pygame.K_UP: # If the up arrow key is pressed
                just_jumped = True # Set just_jumped to True to indicate the player has jumped
        if event.type == pygame.MOUSEBUTTONDOWN: # If a mouse button is pressed down
            if event.button == 1: # If the left mouse button is pressed
                left_mouse_down = True # Set left_mouse_down to True to indicate the left mouse button is pressed
            elif event.button == 3: # If the right mouse button is pressed
                right_mouse_down = True # Set right_mouse_down to True to indicate the right mouse button is pressed
    return (Status_Info(keys, mouse_pos, just_jumped, left_mouse_down, right_mouse_down, h_Lmouse, h_Rmouse), done)

def load_type1_skins():
    """Loads all animal skin images from the 'characters/simple animals' folder and returns them as a dictionary.

    Returns:
        dict: A dictionary containing the loaded animal skin images.
    """
    bear = pygame.image.load('characters/simple animals/bear.png')
    buffalo = pygame.image.load('characters/simple animals/buffalo.png')
    chick = pygame.image.load('characters/simple animals/chick.png')
    chicken = pygame.image.load('characters/simple animals/chicken.png')
    cow = pygame.image.load('characters/simple animals/cow.png')
    crocodile = pygame.image.load('characters/simple animals/crocodile.png')
    dog = pygame.image.load('characters/simple animals/dog.png')
    duck = pygame.image.load('characters/simple animals/duck.png')
    elephant = pygame.image.load('characters/simple animals/elephant.png')
    frog = pygame.image.load('characters/simple animals/frog.png')
    giraffe = pygame.image.load('characters/simple animals/giraffe.png')
    goat = pygame.image.load('characters/simple animals/goat.png')
    gorilla = pygame.image.load('characters/simple animals/gorilla.png')
    hippo = pygame.image.load('characters/simple animals/hippo.png')
    horse = pygame.image.load('characters/simple animals/horse.png')
    monkey = pygame.image.load('characters/simple animals/monkey.png')
    moose = pygame.image.load('characters/simple animals/moose.png')
    narwhal = pygame.image.load('characters/simple animals/narwhal.png')
    owl = pygame.image.load('characters/simple animals/owl.png')
    panda = pygame.image.load('characters/simple animals/panda.png')
    parrot = pygame.image.load('characters/simple animals/parrot.png')
    penguin = pygame.image.load('characters/simple animals/penguin.png')
    pig = pygame.image.load('characters/simple animals/pig.png')
    rabbit = pygame.image.load('characters/simple animals/rabbit.png')
    rhino = pygame.image.load('characters/simple animals/rhino.png')
    sloth = pygame.image.load('characters/simple animals/sloth.png')
    snake = pygame.image.load('characters/simple animals/snake.png')
    walrus = pygame.image.load('characters/simple animals/walrus.png')
    whale = pygame.image.load('characters/simple animals/whale.png')
    zebra = pygame.image.load('characters/simple animals/zebra.png')
    return {
        "bear": bear,
        "buffalo": buffalo,
        "chick": chick,
        "chicken": chicken,
        "cow": cow,
        "crocodile": crocodile,
        "dog": dog,
        "duck": duck,
        "elephant": elephant,
        "frog": frog,
        "giraffe": giraffe,
        "goat": goat,
        "gorilla": gorilla,
        "hippo": hippo,
        "horse": horse,
        "monkey": monkey,
        "moose": moose,
        "narwhal": narwhal,
        "owl": owl,
        "panda": panda,
        "parrot": parrot,
        "penguin": penguin,
        "pig": pig,
        "rabbit": rabbit,
        "rhino": rhino,
        "sloth": sloth,
        "snake": snake,
        "walrus": walrus,
        "whale": whale,
        "zebra": zebra
    }

def load_type2_skin():
    """Loads the runner character skins.

    Returns:
        tuple: A tuple containing the loaded runner character skins.
    """
    standing = pygame.image.load("characters/runner/standing.png").convert_alpha()
    falling = pygame.image.load("characters/runner/falling.png").convert_alpha()
    jumping = pygame.image.load("characters/runner/jumping.png").convert_alpha()
    run1 = pygame.image.load("characters/runner/run1.png").convert_alpha()
    run2 = pygame.image.load("characters/runner/run2.png").convert_alpha()
    run3 = pygame.image.load("characters/runner/run3.png").convert_alpha()
    return  standing, falling, jumping, run1, run2, run3

def read_stats_dict():
    """Reads the game statistics from the stats.json file.

    Returns:
        dict: A dictionary containing the game statistics.
    """
    try:
        with open("stats.json") as filehandle: # Open the stats.json file
            return json.load(filehandle) # Load the JSON data from the file
    except:
        return {} # If the file does not exist or cannot be read, return an empty dictionary

def read_stats():
    """Reads the game statistics from the stats.json file.

    Returns:
        tuple: A tuple containing the game statistics.
    """
    data = read_stats_dict() # Read the statistics dictionary from the stats.json file
    coins = data.get("coins", 0) # Get the number of coins, defaulting to 0 if not found
    complete_levels = data.get("completed_levels", {}) # Get the completed levels, defaulting to an empty dictionary if not found
    owned_skins = data.get("owned_skins", {}) # Get the owned skins, defaulting to an empty dictionary if not found
    selected_skin = data.get("selected_skin", []) # Get the selected skin, defaulting to an empty list if not found
    return coins, complete_levels, owned_skins, selected_skin

def write_stats(coins=None, level_time=None, new_skin=None, selected_skin=None):
    """Writes the game statistics to the stats.json file.

    Args:
        coins (int, optional): The number of coins to update. Defaults to None.
        level_time (tuple, optional): A tuple containing the level path and new time to update. Defaults to None.
        new_skin (tuple, optional): A tuple containing the skin name and skin type to add. Defaults to None.
        selected_skin (list, optional): A list of selected skins to update. Defaults to None.
    """
    data = read_stats_dict() # Read the statistics dictionary from the stats.json file
        
    if coins is not None: # If coins is provided
        data["coins"] = coins # Update the coins in the statistics dictionary

    if level_time is not None: # If level_time is provided
        level_path, new_time = level_time # Unpack the level path and new time
        saved_score = data["completed_levels"].get(level_path, float('inf')) # Get the saved time for the level, defaulting to infinity if not found
        data["completed_levels"][level_path] = min(new_time, saved_score) # Update the level time, keeping the minimum of the new time and saved score

    if new_skin is not None: # If new_skin is provided
        skin_name, skin_type = new_skin # Unpack the skin name and skin type
        data["owned_skins"][skin_name] = skin_type # Add the new skin to the owned skins dictionary
        
    if selected_skin is not None: # If selected_skin is provided
        data["selected_skin"] = selected_skin # Update the selected skin in the statistics dictionary

    with open("stats.json", "w") as filehandle: # Open the stats.json file in write mode
        json.dump(data, filehandle) # Write the updated statistics dictionary to the file
        
def draw_clouds(cloud_img, cloud_x):
    """Draws the clouds on the screen.

    Args:
        cloud_img (Surface): The image of the cloud to draw.
        cloud_x (int): The x-coordinate of the cloud.

    Returns:
        int: The updated x-coordinate of the cloud.
    """
    global SCREEN_X
    if cloud_img is not None: # Check if the cloud image is loaded
        screen.blit(cloud_img, (cloud_x,0)) # Draw the cloud image at the specified x-coordinate and at the top of the screen
        cloud_x -= 1 # Move the cloud to the left by 1 pixel
        cloud_x %= SCREEN_X - cloud_img.get_width() # Wrap the cloud position around the screen width to create a continuous scrolling effect
        return cloud_x 
    return 0 # If the cloud image is not loaded, return 0


game_state = "main_menu" # Global variable to keep track of the current game state
type1_skins_imgs = load_type1_skins() # Load the type 1 skins images from the 'characters/simple animals' folder
person_imgs = load_type2_skin() # Load the runner character skins
coins, complete_levels, owned_skins, selected_skin = read_stats() # Read the game statistics from the stats.json file
cloud_img = pygame.image.load("clouds.png").convert_alpha() # Load the cloud image for drawing clouds
cloud_x = 0 # Initial x-coordinate for the cloud image