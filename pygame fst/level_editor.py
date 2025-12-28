""" 
level_editor.py
Author: Adiv Goldberg
Date last edited: 2025-06-09
Program: PLatformer level editor
Description:
-------------
This module provides a 2D platformer level editor built with Pygame, enabling users to design and manage game levels. It offers a comprehensive set of features for creating and modifying game environments, including:
- Interactive Placement: Easily place and arrange various block types (e.g., solid ground, platforms, walls) and power-ups within the level grid.
- Customization: Import and apply custom background images and music to personalize the level's aesthetic and atmosphere.
- File Management: Save and load level designs, including block layouts, power-up placements, and custom media, for easy access and iteration.
- Intuitive Interface: A user-friendly interface with dedicated panels for tile selection, file operations, and a clear visual representation of the level being edited.
"""
# import the pygame module
import pygame
from gameplay import Blocks, Power_Ups, load_images, grid_to_class 
import tools
import gameplay
import main_menu
import json

# will make it easier to use pygame functions
from pygame.draw import line, rect
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
class Level_Editor_Tiles(Blocks, Power_Ups):
    def __init__(self, type_num, location, is_block, grid_size,b_imgs, p_imgs):
        """intializes tiles to slect which tile you are adding to the level you are making

        Args:
            type_num (int): tile type
            location (tuple): x, y location of tile
            is_block (bool): weather its a block (or a powerup)
            grid_size (float): size of grid to scale the tiles to
            b_imgs (list): list of block imgs
            p_imgs (list): list of powerup images
        """
        self.type = type_num
        self.x, self.y = location
        self.is_block = is_block
        self.animate_time = 0 #time animation has been going on for
        self.MAX_animate_time = 25 #reset after animation after
        self.collected = False #for error handling with other class funcs
        self.rect = (0,0,0,0) #collision rect
        self.rect2 = (0,0,0,0) #collision rect
        self.g_size = grid_size #grid size
        self.select_rect = self.redifine_rect() #redifine collision to make it bigger for clicking compared to game
        self.selected = False #if the user has clicked on this tile
        self.b_imgs = b_imgs #block imgs
        self.p_imgs = p_imgs #powerup imgs
        
    def go(self):
        """
        run actions for this class
        """
        self.draw() #draw
        self.get_selected() #check collisions and actions
        
    def redifine_rect(self):
        """
        redifines the collision rect for mbetter clicking
        
        Returns:
           rect: (x,y,w,h) for collision
        """
        if self.is_block: # if its a block
            rect = (self.x - 3, self.y - 3, self.g_size + 6, self.g_size + 6) #this is its rect
        else: # else (powerup)
            rect = (self.x + 0.25*self.g_size - 5, self.y + 0.25*self.g_size - 5, 0.5*self.g_size + 10, 0.5*self.g_size + 10) #its rect
        return rect
    
    def draw(self):
        """
        draw the tile to the screen
        """
        global select_block, select_powerup
        if self.is_block and select_block == self.type: #if its the selected block
            self.selected = True #its selected
        elif not self.is_block and select_powerup == self.type: #if its the selected powerup
            self.selected = True #its selected
        else:
            self.selected = False #its not selected
        
        if self.selected: #if its selected
            pygame.draw.rect(screen, tools.BLUE, self.select_rect, 3) #draw a blue rect around it

        if self.is_block: #if its a block
            Blocks.draw(self) #draw it from blocks class
        else: #its a powerup
            Power_Ups.draw(self) #draw from powerups class
            
    def get_selected(self):
        """
        checks if its pressed and performs actions if it is
        """
        global select_block, select_powerup
        if pygame.Rect(self.select_rect).collidepoint((input_info.xMouse, input_info.yMouse)) and input_info.left_mouse_down: #if its colliding and the left mouse is clicked
            if self.is_block: #if its a block
                select_block = self.type # the selected block is that type
            else: #its a powerup
                select_powerup = self.type #set slected powerup to that type
 
class File_Handler():
    def __init__(self, x, y, img, g_size, type):
        """
        initialize class for loading and saving files buttons

        Args:
            x (float): x position of button
            y (float): y position of button
            img (img): img of button
            g_size (float): grid size
            type (int): type number indetifier
        """
        self.x = x
        self.y = y
        self.img = img
        self.g_size = g_size
        self.type = type
        self.selected = False #if its selected
        self.panel_open = False #if the panel (for loading imgs and sound) is open
        self.panel_rect = (625,self.y - 55, 100 ,50) #rect for clicking
        self.img_impimg = pygame.image.load("menu icons/image upload.png") #img upload for panel
        self.img_impimg = pygame.transform.scale(self.img_impimg, (self.g_size, self.g_size)) #rescale img
        self.img_impsound = pygame.image.load("menu icons/sound upload.png") #same for import sound image
        self.img_impsound = pygame.transform.scale(self.img_impsound, (self.g_size, self.g_size))
    
    def go(self):
        """
        run actions for class
        """
        self.draw()
        self.selection()
    
    def draw(self):
        """
        draw button to screen
        """
        global select_block, select_powerup
        screen.blit(self.img, (self.x, self.y)) #draw it
        if self.type == 3 and select_block == 0 and select_powerup == 0: # if its a delete tile
            pygame.draw.rect(screen, tools.RED,  (self.x - 3, self.y - 3, self.g_size + 6, self.g_size + 6), 3) #draw a red rect around it
            
    def selection(self):
        """
        hadnles clicking and actions if its cliked
        """
        global select_block, select_powerup, power_up_output, block_output, b_img, b_img_file_path, b_sound, b_sound_file_path
        if pygame.Rect(self.x, self.y, self.g_size, self.g_size).collidepoint((input_info.xMouse, input_info.yMouse)) and input_info.left_mouse_down: # if collinding and clicked
            self.selected = True #its selected
        else:
            self.selected = False #its not slected
        
        if (input_info.left_mouse_down or input_info.right_mouse_down) and not pygame.Rect(self.panel_rect).collidepoint((input_info.xMouse, input_info.yMouse)): #either mouse is clicked and its not colliding with the panel
            self.panel_open = False #close it
        
        if self.selected: # if the tile is selected
            if self.type == 1:
                #save button
                save_level(block_output, power_up_output, b_img_file_path, b_sound_file_path) # save the level
            elif self.type == 2:
                #load button
                self.panel_open = True # open panel
            elif self.type == 3:
                #trash button
                select_block = 0 # set selected powerup and img to empty
                select_powerup = 0
            
        if self.panel_open: # if the panel is open
            rect(screen, tools.WHITE, self.panel_rect) #draw the panel
            rect(screen, tools.BLUE, self.panel_rect, 5) #and a blue outline for visibilty
            screen.blit(self.img_impimg, (640,self.y - 45)) #blit import img img
            screen.blit(self.img_impsound, (640 + self.g_size + 10, self.y - 45))# blit import sound img 
            if input_info.left_mouse_down: #if left mouse is clicked
                # Check if clicking on the image import icon
                impimg_rect = pygame.Rect(640, self.y - 45, self.g_size, self.g_size)
                if impimg_rect.collidepoint((input_info.xMouse, input_info.yMouse)): # if colliding img with button
                    root = tk.Tk() #open file selecter for imgs
                    root.withdraw()
                    b_img_file_path = filedialog.askopenfilename(
                        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"), ("All Files", "*.*")]
                    )
                    
                    root.destroy()
                    
                    if b_img_file_path:
                        #try loading and scaling the image
                        try:
                            b_img = pygame.image.load(b_img_file_path)
                            b_img = pygame.transform.scale(b_img, (725, 543))
                        except:
                            b_img = None
                # Check if clicking on the sound import icon
                impsound_rect = pygame.Rect(640 + self.g_size + 10, self.y - 45, self.g_size, self.g_size)
                if impsound_rect.collidepoint((input_info.xMouse, input_info.yMouse)): # if clicking on sound button
                    root = tk.Tk()
                    root.withdraw()
                    b_sound_file_path = filedialog.askopenfilename( #open file selecter for sound
                        filetypes=[("Sound Files", "*.wav;*.ogg;*.mp3"), ("All Files", "*.*")]
                    )
                    
                    root.destroy()
                    
                    if b_sound_file_path: # if there is a sound uploaded
                        # You can now use file_path to load the sound with pygame.mixer.Sound(file_path)
                        try: 
                            b_sound = pygame.mixer.Sound(b_sound_file_path) #try loading the sound
                            pygame.mixer.stop()
                        except:
                            b_sound = None #if you cant set no path

# your FUNCTIONS go here
def place_on_grid(g_size):
    """
    when you click on the grid it places the block there

    Args:
        g_size (float): grid size
    """
    global select_block, select_powerup
    if not file_handler_tiles[1].panel_open: #if the panel is closed
        for i in range(len(blocks)): # iterate through blocks
            if pygame.Rect((blocks[i].x, blocks[i].y, g_size, g_size)).collidepoint((input_info.xMouse, input_info.yMouse)) and input_info.holding_Lmouse: # if its clicked on
                blocks[i].type = select_block #change that block to the selected block
                
        for i in range(len(power_ups)): #same for powerups
            if pygame.Rect((power_ups[i].x, power_ups[i].y, g_size, g_size)).collidepoint((input_info.xMouse, input_info.yMouse)) and input_info.holding_Rmouse:
                power_ups[i].type = select_powerup

def draw_grid(g_size, grid_screenx, grid_screeny):
    """
    Draws a grid on the screen with specified cell size and dimensions.

    Args:
        g_size (int): The size (in pixels) of each grid cell.
        grid_screenx (int): The width of the grid area in pixels.
        grid_SCREEN_Y (int): The height of the grid area in pixels.

    Notes:
        - Draws vertical and horizontal lines to form the grid.
    """
    # Draw grid
    # Draw vertical grid lines
    for x in range(int(grids[0]) + 1):
        line(screen, tools.BLACK, (x * g_size, 0), (x * g_size, grid_screeny), 1)
    # Draw horizontal grid lines
    for y in range(int(grids[1]) + 1):
        line(screen, tools.BLACK, (0, y * g_size), (grid_screenx, y * g_size), 1)
        
def draw_panels(panel_size,small_panel_size, grid_screenx, grid_screeny):
    """
    Draws the side and bottom panels on the screen.
    Args:
        panel_size (int): The width of the side panel.
        small_panel_size (int): The height of the bottom panel.
        grid_screenx (int): The x-coordinate where the grid ends and the side panel begins.
        grid_screeny (int): The y-coordinate where the grid ends and the bottom panel begins.
    Globals:
        tools.SCREEN_X (int): The width of the entire screen.
        tools.SCREEN_Y (int): The height of the entire screen.
        screen (pygame.Surface): The surface to draw on.
        tools.WHITE (tuple): The color used for the panels.
    Side Effects:
        Draws rectangles representing the side and bottom panels on the screen.
    """
    # Draw side panel
    rect(screen, tools.WHITE, (grid_screenx + 1, 0, panel_size, tools.SCREEN_Y))

    # Draw bottom panel
    rect(screen, tools.WHITE, (0, grid_screeny + 1, tools.SCREEN_X, small_panel_size))

def tiles_to_panel(tile_size, b_imgs, p_imgs, g_size):
    """takes tiles and put them in level editor class to be placed in the level

    Args:
        tile_size (float): size of tile
        b_imgs (list): list of block imgs
        p_imgs (list): list of powerup imgs
        g_size (float): size of grid

    Returns:
        level_editor_tiles (list): list of Level_Editor_Tiles objects for blocks and powerups
        last_powerup_x (float): x position of the last powerup tile
        last_block_x (float): x position of the last block tile
        file_handler_tiles (list): list of File_Handler objects for save, load, and delete buttons
    """
    level_editor_tiles = []
    tile_margin = 10 #margin

    # Add block tiles
    block_types = [i + 1 for i in range(len(block_imgs)-1)] # dont include type 0 or 17 as they cant be placed
    # First 10 block types on the side panel, bc only 10 fit
    for i, type_num in enumerate(block_types[:10]):
        x = GRID_SCREEN_X + PANEL_SIZE // 2 - tile_size // 2
        y = tile_margin + i * (tile_size + tile_margin)
        level_editor_tiles.append(Level_Editor_Tiles(type_num, (x, y), True, GRID_SIZE_LE, b_imgs, p_imgs))

    # Power-ups on the bottom panel
    powerup_start_x = tile_margin
    powerup_y = GRID_SCREEN_Y + SMALL_PANEL_SIZE // 2 - tile_size // 2
    for idx, type_num in enumerate(range(1, len(power_up_imgs) + 1)):
        x = powerup_start_x + idx * (tile_size + tile_margin)
        y = powerup_y
        level_editor_tiles.append(Level_Editor_Tiles(type_num, (x, y), False, GRID_SIZE_LE, b_imgs, p_imgs))

    # Remaining block types on the bottom panel, after power-ups
    bottom_block_start_x = powerup_start_x + len(power_up_imgs) * (tile_size + tile_margin) + tile_margin
    for idx, type_num in enumerate(block_types[10:]):
        x = bottom_block_start_x + idx * (tile_size + tile_margin)
        y = powerup_y
        level_editor_tiles.append(Level_Editor_Tiles(type_num, (x, y), True, GRID_SIZE_LE, b_imgs, p_imgs))

    # x values for lines to seperate sections
    last_powerup_x = powerup_start_x + (len(power_up_imgs)) * (tile_size + tile_margin) - tile_margin // 2
    last_block_x = bottom_block_start_x + (len(block_types[10:])) * (tile_size + tile_margin) - tile_margin // 2
    
    file_handler_tiles = []
    # Create two file handler tiles next to the vertical line after the last powerup
    file_tile_margin = 5  # Lowered spacing
    file_tile_size = int(g_size * 0.75)
    file_tile_y = powerup_y + 10

    # imgs for file handler
    save_img = pygame.image.load("menu icons/save.png").convert_alpha()
    load_img = pygame.image.load("menu icons/load.png").convert_alpha()
    delete_img = pygame.image.load("menu icons/delete.png").convert_alpha()
    #scale imgs
    save_img = pygame.transform.smoothscale(save_img, (int(file_tile_size), int(file_tile_size)))
    load_img = pygame.transform.smoothscale(load_img, (int(file_tile_size), int(file_tile_size)))
    delete_img = pygame.transform.smoothscale(delete_img, (int(file_tile_size), int(file_tile_size)))

    # Center vertically in the bottom panel
    file_tile1_x = last_block_x + file_tile_margin
    #save button
    file_handler_tiles.append(File_Handler(file_tile1_x, file_tile_y, save_img, file_tile_size, 1))

    # load button
    file_tile2_x = file_tile1_x + file_tile_size + file_tile_margin
    file_handler_tiles.append(File_Handler(file_tile2_x, file_tile_y, load_img, file_tile_size, 2))

    #delete button
    delete_tile_x = file_tile2_x + file_tile_size + file_tile_margin
    file_handler_tiles.append(File_Handler(delete_tile_x, file_tile_y, delete_img, file_tile_size, 3))
    
    return level_editor_tiles, last_powerup_x, last_block_x, file_handler_tiles

def save_level(b_output,p_output, img = None, music = None):
    """Saves the current level data to a file.

    Args:
        b_output (list): 2D list representing block types in the level.
        p_output (list): 2D list representing power-up types in the level.
        img (pygame.Surface, optional): Background image for the level. Defaults to None.
        music (str, optional): File path to the level's music. Defaults to None.

    Returns:
        block output (list): 2D list of block types.
        power_up output (list): 2D list of power-up types.
        background image (pygame.Surface, optional): Background image for the level. Defaults to None.
        music (str, optional): File path to the level's music. Defaults to None.
    """
    global blocks, power_ups
    for block in blocks: #iterate through block
        x, y = block.grid_location
        b_output[y][x] = block.type #places it in grid based on location
    for power_up in power_ups: #same for powerups
        x, y = power_up.grid_location
        p_output[y][x] = power_up.type
        
    data = {'blocks': b_output, 'powerups' : p_output} #write that list as data to save file
    
    # Hide the root window (prevents the Tkinter window from showing)
    root = tk.Tk()
    root.withdraw()

    # Ask the user for a file name and location to save
    file_path = filedialog.asksaveasfilename(
        defaultextension=".adiv",  # Default file extension for saved files
        filetypes=[("Adiv Level Files", "*.adiv"), ("All Files", "*.*")],  # File type filters
        title="Save Level As"  # Dialog window title
    )
    root.destroy()

    # If the user selected a file path
    if file_path:
        # Open the file for writing
        with open(file_path, 'w') as filehandle:
            # Save the level data as JSON to the file
            # Save image and music file paths
            if img is not None and img != "background.png":
                try:
                    data['image'] = img
                except:
                    pass #image doesnt load
            if music is not None:
                try:
                    data['music'] = music
                except:
                    pass #music doesnt load
            json.dump(data, filehandle) #place data in file

    return b_output, p_output

def load_level_e(level_path):
    """loads a file to edit in level editor

    Args:
        level_path (string): file path of level
    """
    global block_output, power_up_output, b_img, b_sound, blocks, power_ups
    block_output, power_up_output, b_img, b_sound, _ = gameplay.adiv_parser(level_path, b_img, b_sound) #load file to edit or None for new file
    blocks, power_ups = grid_to_class(block_output, "Block", GRID_SIZE_LE, block_imgs), grid_to_class(power_up_output, "Powerups", GRID_SIZE_LE, power_up_imgs)

# your GLOBAL variables go here
GRID_SIZE_LE = gameplay.GRID_SIZE

b_img = pygame.image.load("background.png").convert_alpha() 
b_img_file_path = "background.png" #start bg file_path
b_sound = None #default sound (none)
b_sound_file_path = None 

block_output, power_up_output, b_img, b_sound, _ = gameplay.adiv_parser(None, b_img, b_sound) #load file to edit or None for new file

select_block = 0 #start at eraser
select_powerup = 0

grids = (tools.SCREEN_X/GRID_SIZE_LE, tools.SCREEN_Y/GRID_SIZE_LE) #grid dimensions
PANEL_SIZE = 75 # size of bigger panel
SMALL_PANEL_SIZE = PANEL_SIZE * min(tools.SCREEN_X,tools.SCREEN_Y) / max(tools.SCREEN_X,tools.SCREEN_Y) #size of smaller panel
GRID_SIZE_LE = (GRID_SIZE_LE/tools.SCREEN_X)*(tools.SCREEN_X - PANEL_SIZE) #grid size with panel 
GRID_SCREEN_X, GRID_SCREEN_Y = (tools.SCREEN_X - PANEL_SIZE, tools.SCREEN_Y - SMALL_PANEL_SIZE) #screen size ignoring panels
if tools.SCREEN_Y > tools.SCREEN_X: #flip them if the y screen is bigger than x
    GRID_SCREEN_X, GRID_SCREEN_Y = (tools.SCREEN_X - SMALL_PANEL_SIZE, tools.SCREEN_Y - PANEL_SIZE)
    
block_imgs, power_up_imgs, background_img = load_images(GRID_SIZE_LE) #load images

blocks, power_ups = grid_to_class(block_output, "Block", GRID_SIZE_LE, block_imgs), grid_to_class(power_up_output, "Powerups", GRID_SIZE_LE, power_up_imgs) #place blocks and powerups in class

level_editor_tiles, last_powerup_x, last_block_x, file_handler_tiles = tiles_to_panel(GRID_SIZE_LE, block_imgs, power_up_imgs, GRID_SIZE_LE) #create panel and some buttons

input_info = None #button info







# MAIN LOOP
def run_level_editor(): #while loop
    global screen, b_img, b_sound, PANEL_SIZE, SMALL_PANEL_SIZE, GRID_SIZE_LE, b_img_file_path, b_sound_file_path
    global block_imgs, power_up_imgs, background_img, block_output, power_up_output, blocks, power_ups
    global level_editor_tiles, last_powerup_x, last_block_x, file_handler_tiles, input_info, done #split globals into a few lines for organization
    screen.fill(tools.WHITE)
    if b_img is not None: #if there is an image
        screen.blit(b_img, (0,0)) #blit it
        
    if b_sound is not None: #play bg sound if it exists
        if not pygame.mixer.get_busy(): #prevent echo
            b_sound.play(-1)

    input_info, done = tools.check_input() # get user inputs
    
    #draw grid and panels
    draw_grid(GRID_SIZE_LE, GRID_SCREEN_X, GRID_SCREEN_Y)
    draw_panels(PANEL_SIZE, SMALL_PANEL_SIZE, GRID_SCREEN_X, GRID_SCREEN_Y)
        
    place_on_grid(GRID_SIZE_LE) #place on grid
    
    for tile in level_editor_tiles:
        tile.go() #run leevel editor tiles
    
    for block in blocks: # run blocks
        block.go()
        
    for power_up in power_ups: # run powerups
        power_up.go()
        
    for tile in file_handler_tiles:
        tile.go() #run file handler tiles
        
    screen.blit(main_menu.back_button, (745,545)) #blit back button
    back = main_menu.back_button_collide((745,545), 50, "level_editor_menu", input_info.left_mouse_down, input_info.xMouse, input_info.yMouse) #check for collision
    if back: # if you go back reset img and sound
        b_img = pygame.image.load("background.png").convert_alpha() 
        b_img_file_path = "background.png" #start bg file_path
        if b_sound is not None: #if there is a sound
            b_sound.stop()
        b_sound = None
        b_sound_file_path = None
    

    # this line draws everything into the window all at once
    pygame.display.flip()
    # this line limits the frames per second to 60
    clock.tick(60)
    
    return done
    
if __name__ == "__main__": #if in file run (for testing)
    while not done:
        run_level_editor()
    pygame.quit()