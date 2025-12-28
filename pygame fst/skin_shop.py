""" 
skin_shop.py
Author: Adiv Goldberg
Date last edited: 2025-06-09
Program: platformer skin shop
Description:
-------------
This module implements the skin shop for the platformer game. It provides a user-friendly interface for accessing different character skins, including:
- A grid of available skins to choose from.
- Information about each skin, including its name, cost, and whether it is owned.
- A button to purchase or equip a selected skin.
- Back button to return to the main menu.
"""
# import the pygame module
import pygame
import tools
import main_menu
from pygame.draw import rect
import gameplay

# initializes the pygame module
pygame.init()
SCREEN_X = 800
SCREEN_Y = 600

# creates a screen variable of size 800 x 600
screen = pygame.display.set_mode([SCREEN_X,SCREEN_Y])

# controls the main game while loop
done = False

# sets the frame rate of the program
clock = pygame.time.Clock()

#CLASSES
class Skins:
    def __init__(self, x, y, img, cost, type, name, length, owned):
        """ Initializes a skin with the specified attributes.

        Args:
            x (int): The x-coordinate of the skin.
            y (int): The y-coordinate of the skin.
            img (Surface): The image representing the skin.
            cost (int): The cost of the skin.
            type (int): The type of the skin (1 for cube, 2 for runner).
            name (str): The name of the skin.
            length (int): The length of the skin.
            owned (bool): Whether the skin is owned by the player.
        """
        self.x = x
        self.y = y
        self.length = length
        if type == 1: # If the skin is a cube, it has a single image
            self.img = pygame.transform.scale(img, (self.length, self.length)) # Scale the image to fit the skin
        else: # If the skin is a runner, it has multiple images (for animation)
            self.img = []
            for i in range(len(img)): 
                self.img.append(pygame.transform.scale(img[i], (self.length, self.length))) # Scale each image to fit the skin
        self.cost = cost # The cost of the skin
        self.name = name # The name of the skin
        self.type = type #1 for cube 2 for runner
        self.owned = owned # Whether the skin is owned by the player
    
    def go(self):
        """Runs the main actions for the skin.
        """
        self.draw()
        self.selection()
    
    def draw(self):
        """Draws the skin on the screen.
        """
        global retro_font_15, coin_img_small, checkmark_img
        if self.type == 1: # If the skin is a cube, draw the single image
            screen.blit(self.img, (self.x, self.y)) 
        else:
            screen.blit(self.img[0], (self.x, self.y)) # If the skin is a runner, draw the first image (for now, no animation)
            
        name_text = retro_font_15.render(self.name, True, tools.BLACK) # Render the name of the skin
        screen.blit(name_text, (self.x + self.length // 2 - name_text.get_width() // 2, self.y - 18)) #blit it above the skin
         
        if not self.owned: # If the skin is not owned
            cost_text = retro_font_15.render(str(self.cost), True, tools.BLACK) # Render the cost of the skin
            screen.blit(cost_text, (self.x + self.length // 2 - cost_text.get_width() // 2 + 5, self.y + self.length + 12 - cost_text.get_height() // 2)) #blit it below the skin
            screen.blit(coin_img_small, (self.x + self.length // 2 - cost_text.get_width() // 2 - coin_img_small.get_width() + 5, self.y + self.length + 12 - coin_img_small.get_height() // 2)) #blit the coin image next to the cost
        else: # If the skin is owned
            screen.blit(checkmark_img, (self.x + self.length // 2 - checkmark_img.get_width() // 2, self.y + self.length + 12 - checkmark_img.get_height() // 2)) #blit the checkmark image below the skin
        
        if self.name == tools.selected_skin[0]: # If the skin is the selected skin
            rect(screen, tools.GREEN, (self.x - 5, self.y - 5, self.length + 10, self.length + 10), 5) # Draw a green border around the skin to indicate it is selected
            
    def selection(self):
        """Handles the selection of the skin.
        """
        if pygame.Rect(self.x, self.y, self.length, self.length).collidepoint(main_menu.input_info.xMouse, main_menu.input_info.yMouse) and main_menu.input_info.left_mouse_down: # If the mouse is over the skin and clicked
            if self.owned: # If the skin is owned
                tools.selected_skin = [self.name, self.type] # Set the selected skin to this skin
                tools.write_stats(None, None, tools.selected_skin, tools.selected_skin) # Write the selected skin to the stats file
                gameplay.player = gameplay.Player(self.img, self.type) # Update the player with the new skin
            elif tools.coins >= self.cost: # If the skin is not owned and the player has enough coins
                tools.selected_skin = [self.name, self.type] # Set the selected skin to this skin
                tools.coins -= self.cost # Deduct the cost of the skin from the player's coins
                self.owned = True # Mark the skin as owned
                gameplay.player = gameplay.Player(self.img, self.type) # Update the player with the new skin
                tools.write_stats(tools.coins, None, tools.selected_skin, tools.selected_skin) # Write the updated coins and selected skin to the stats file

# your FUNCTIONS go here
def draw_coins(coin_img):
    """Draws the player's coins on the screen.

    Args:
        coin_img (Surface): The image representing a coin.
    """
    x = 335
    y = 75
    screen.blit(coin_img, (x,y)) # Draw the coin image at the specified position
    coin_text = gameplay.retro_font_32.render(str(tools.coins), True, tools.BLACK) # Render the player's coins as text
    screen.blit(coin_text, (x + coin_img.get_width(), y + coin_img.get_height() // 2 - coin_text.get_height() // 2)) #blit the text next to the coin image
    
def draw_coming_soon(img, num):
    """Draws the "Coming Soon" message and the associated image. in a row

    Args:
        img (Surface): The image to display.
        num (int): The number of times to display the image.
    """
    global retro_font_15
    x_start = 75 + img.get_width()
    margin = img.get_width() + 20
    y_start = 450
    text = retro_font_15.render("Coming Soon", True, tools.BLACK) # Render the "Coming Soon" text
    for i in range(num):
        screen.blit(img, (x_start + margin*i, y_start)) # Draw the image at the specified position
        screen.blit(text, (x_start + margin*i + 0.5*img.get_width() - 0.5*text.get_width(), y_start - text.get_height()- 5)) #blit the text above the image
    

# your GLOBAL variables go here
menu_background = pygame.image.load("skin shop menu.png").convert_alpha() # Load the skin shop background image
menu_background = pygame.transform.scale(menu_background, (SCREEN_X, SCREEN_Y)) # Scale the background image to fit the screen

retro_font_15 = pygame.font.Font("upheavtt.ttf", 15) # Load the retro font for rendering text

checkmark_img = pygame.image.load("check-mark.png") # Load the checkmark image
checkmark_img = pygame.transform.scale(checkmark_img, (25,25)) # Scale the checkmark image

coin_img = pygame.image.load("powerups for game/coin(1).png") # Load the coin image
coin_img_small = pygame.transform.scale(coin_img, (20,20)) # Scale the coin image to a smaller size for displaying coins

coming_soon_img = pygame.image.load("characters/coming soon.png").convert_alpha() # Load the "Coming Soon" image
coming_soon_img = pygame.transform.scale(coming_soon_img, (100, 100)) # Scale the "Coming Soon" image

tools.coins, _, tools.owned_skins, tools.selected_skin = tools.read_stats() # Read the player's coins, owned skins, and selected skin from the stats file

skins = []

person_owned = False # assume user doesnt own skin
if "Runner" in tools.owned_skins: # If the player owns the Runner skin
    person_owned = True # Mark the skin as owned
skins.append(Skins(50,450, tools.person_imgs, 500, 2, "Runner", 100, person_owned)) # Add the Runner skin to the list of skins

cols = 10
x_margin = 50 # Margin from the left edge of the screen
y_margin = 150 # Margin from the top edge of the screen
spacing_x = 75 # Horizontal spacing between skins
spacing_y = 100 # Vertical spacing between skins

for i, (name, img) in enumerate(tools.type1_skins_imgs.items()): # Iterate through the type 1 skins
    row = i // cols # Calculate the row index based on the current index and number of columns
    col = i % cols # Calculate the column index based on the current index and number of columns
    x = x_margin + col * spacing_x # Calculate the x position based on the column index and spacing
    y = y_margin + row * spacing_y # Calculate the y position based on the row index and spacing
    cost = 50 # Default cost for the skin
    owned = False # Assume the skin is not owned by the player
    if name in tools.owned_skins: # If the player owns the skin
        owned = True # Mark the skin as owned
    skins.append(Skins(x, y, img, cost, 1, name, 35, owned)) # Add the skin to the list of skins



# MAIN LOOP
def run_skin_shop(): #while loop function for the skin shop
    global screen, menu_background, coin_img, skins, done, coming_soon_img

    screen.blit(menu_background, (0, 0)) # Draw the skin shop background image onto the screen
        
    tools.cloud_x = tools.draw_clouds(tools.cloud_img, tools.cloud_x) # Draw the clouds on the skin shop background

    main_menu.input_info, done = tools.check_input() # Check for user input and update the input_info and done variables
    
    screen.blit(main_menu.back_button, main_menu.back_button_pos) # Draw the back button onto the screen
    main_menu.back_button_collide(main_menu.back_button_pos, 50, "main_menu", main_menu.input_info.left_mouse_down, main_menu.input_info.xMouse, main_menu.input_info.yMouse) # Check if the back button is clicked and change the game state to main_menu if it is

    draw_coins(coin_img) # Draw the player's coins on the screen

    for skin in skins:
        skin.go() # Call the go method of each skin to draw it and handle its selection  
    
    draw_coming_soon(coming_soon_img, 5) # Draw the "Coming Soon" message and the associated image in a row

    # this line draws everything into the window all at once
    pygame.display.flip()
    # this line limits the frames per second to 60
    clock.tick(60)
    
    return done
    
if __name__ == "__main__": # Run the skin shop if this module is run directly
    while not done:
        run_skin_shop()  
    pygame.quit()