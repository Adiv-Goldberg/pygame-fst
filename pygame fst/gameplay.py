""" 
gameplay.py
Author: Adiv Goldberg
Date last edited: 2025-06-09
Program: Platformer Physics Engine with Pygame
Description:
-------------
This module implements a basic 2D platformer physics engine using Pygame. It provides classes and functions for player movement, collision detection, and level/block management. The main features include:
- Player class with gravity, jumping, friction, air resistance, and collision handling.
- Blocks class for representing different types of level tiles (full blocks, platforms, walls, etc.).
- Utility functions for level-to-block conversion, sign determination, and more.
- A sample level layout and a main game loop for demonstration.
"""
# import the pygame module
import pygame, random, math
import tools

# will make it easier to use pygame functions
from pygame.draw import line, circle, rect
from random import randint
import json

# initializes the pygame module
pygame.init()

# creates a screen variable of size 800 x 600
screen = pygame.display.set_mode([tools.SCREEN_X,tools.SCREEN_Y])

# controls the main game while loop
done = False

# sets the frame rate of the program
clock = pygame.time.Clock()

#CLASSES

class Player:
    def __init__(self, img, p_type):
        """initializes the Player object with default attributes and images.

        Args:
            img (pygame.Surface): The image representing the player.
            p_type (int): The type of player (1 for cube, 2 for runner).
        """
        self.x = 0
        self.y = 0
        self.length = 0
        self.vx = 0
        self.vy = 0
        self.colliding = False
        self.time = 0
        self.GRAVITY = 1.5
        self.just_jumped = False
        self.jump_force = 17.5
        self.air_time = 0
        self.friction = 0.8
        self.air_accel_resist = 0.8
        self.u_accel = 2.6
        self.max_vx = 7.5
        self.max_vy = 25
        self.R_pressed = False
        self.L_pressed = False
        self.direction = 0 # 0 not moving, 1 right, -1 left
        self.total_coins = tools.coins
        self.user_power_ups = [self.total_coins,0,0,0,0]
        self.touching_wall_side = False
        # Make deep copies of images so base_img is never modified
        if p_type == 1:
            self.base_img = img.copy()  # single surface
            self.img = self.base_img.copy()
        else:
            self.base_img = [im.copy() for im in img]  # list of surfaces
            self.img = [im.copy() for im in self.base_img]
        self.angle = 0  # For continuous rotation
        self.p_type = p_type #1 for cube 2 for runner
        self.animate_time = 0 #time animation has been going on for
        self.MAX_animate_time = 25 #reset after animation after
                
    def make_new(self):
        """
        adjusts the variables to reset a level back to its original state for the player.
        """
        global pause_panel_open
        spawn_block = None
        check_next = True
        for b in blocks:
            if b.type == 12 and b.collected:
                spawn_block = b
                check_next = False
                break
            elif b.type == 13 and check_next:
                spawn_block = b
                self.time = 0
                break
        if spawn_block:
            self.x = spawn_block.x
            self.y = spawn_block.y
        self.length = 35
        self.vx = 0
        self.vy = 0
        if self.p_type == 1:
            # Scale base_img and img to new size
            self.base_img = pygame.transform.scale(self.base_img, (self.length, self.length))
            self.img = self.base_img.copy()
        else:
            # Scale all frames in base_img, then copy to img
            self.base_img = [pygame.transform.scale(self.base_img[i], (self.length, self.length)) for i in range(len(self.base_img))]
            self.img = [im.copy() for im in self.base_img]
        self.angle = 0
        self.user_power_ups = [tools.coins,0,0,0,0]
        pause_panel_open = False
        
    def go(self):
        """
        Updates the player's state and handles movement and collisions.
        """
        self.draw()
        self.air_time += 1
        self.colliding = self.collision_with_blocks(blocks)
        self.collison_with_power_ups()
        self.rotate()
        self.move()
        self.time += 1

    def draw(self):
        """
        Draws the player on the screen.
        """
        # Center the rotated image on the player
        if self.p_type == 1:
            img = self.img
            rect_img = img.get_rect(center=(self.x + self.length // 2, self.y + self.length // 2))
            screen.blit(img, rect_img.topleft)
        else:
            if int(self.direction) == 1:
                self.img[0] = pygame.transform.flip(self.base_img[0], True, False)
            elif int(self.direction) == -1:
                self.img[0] = self.base_img[0]
            
            if self.air_time < 3:
                if self.direction == 0:
                    screen.blit(self.img[0], (self.x, self.y))
                else:
                    self.animate_time += 1
                    self.animate_time %= self.MAX_animate_time
                    img_index = int(self.animate_time / (self.MAX_animate_time / 3)) % 3
                    if self.direction == 1:
                        self.img[img_index + 3] = pygame.transform.flip(self.base_img[img_index + 3], True, False)
                    elif self.direction == -1:
                        self.img[img_index + 3] = self.base_img[img_index + 3]
                    screen.blit(self.img[img_index + 3], (self.x, self.y))
            else:
                if self.vy < 0:
                    # index 2 is the jumping image
                    if self.direction == 1:
                        self.img[2] = pygame.transform.flip(self.base_img[2], True, False)
                    elif self.direction == -1:
                        self.img[2] =self.base_img[2]
                    screen.blit(self.img[2], (self.x, self.y))
                else:
                    # index 1 is the falling image
                    if self.direction == 1:
                        self.img[1] = pygame.transform.flip(self.base_img[1], True, False)
                    elif self.direction == -1:
                        self.img[1] =self.base_img[1]
                    screen.blit(self.img[1], (self.x, self.y))
                            
    def rotate(self):
        """
        Rotates the player's image based on its current angle and direction. if it is a type 1 player (cube)
        """
        if self.p_type == 1:
            if self.air_time > 2:
                self.angle += 5 * -self.direction
                self.img = pygame.transform.rotate(self.base_img, self.angle)
            elif self.angle % 90 != 0:
                self.angle = round(self.angle / 90) * 90
                self.img = pygame.transform.rotate(self.base_img, self.angle)

    def get_velo(self):
        """
        Updates the object's velocity based on gravity, user input, and environmental factors.
        - Applies gravity to the vertical velocity (`vy`).
        - If the object has just jumped and has been airborne for less than 3 frames, sets the vertical velocity to the negative jump force.
        - Adjusts horizontal velocity (`vx`) based on right (`R_pressed`) and left (`L_pressed`) input.
        - Applies friction to horizontal velocity if airborne for less than 3 frames, otherwise applies air resistance.
        - Clamps the vertical and horizontal velocities to their respective maximum values (`max_vy`, `max_vx`).
        """
        global use_powerup_se, jump_se
        #y velocity
        self.vy += self.GRAVITY
        if self.just_jumped:
            if self.air_time < 3:
                self.vy = -self.jump_force
                jump_se.play()
            elif self.user_power_ups[2] > 0 and self.touching_wall_side:
                self.vy = -self.jump_force
                self.user_power_ups[2] -= 1
                use_powerup_se.play()
            elif self.user_power_ups[1] > 0:
                self.vy = -self.jump_force
                self.user_power_ups[1] -= 1
                use_powerup_se.play()
            if self.user_power_ups[3] > 0:
                self.vy = -self.jump_force*1.5
                self.user_power_ups[3] -= 1
                use_powerup_se.play()
        
        if self.R_pressed:
            self.vx += self.u_accel
        if self.L_pressed:
            self.vx -= self.u_accel
            
        if self.air_time > 2:
            self.vx *= self.air_accel_resist
            
        self.vx *= self.friction
            
        if abs(self.vy) > self.max_vy:
            self.vy = sign(self.vy) * self.max_vy
            
        if abs(self.vx) > self.max_vx:
            self.vx = sign(self.vx) * self.max_vx
            
        self.direction = sign(round(self.vx,1))
        
    def move(self):
        """
        Moves the object based on its current velocity, handling pixel-perfect movement and collision detection.
        The method first updates the object's velocity using `get_velo()`. It then performs movement in small steps
        (equal to the maximum of the absolute values of the velocity components) to ensure precise collision detection.
        For each step:
            - Moves the object along the x-axis and checks for collisions with level blocks.
                - If a collision is detected, reverts the x movement and sets horizontal velocity to zero.
            - Moves the object along the y-axis and checks for collisions with level blocks.
                - If a collision is detected:
                    - If moving downward, resets air time.
                    - Reverts the y movement and sets vertical velocity to zero.
            extra check at the end in case in gets stuck which may happen in a a phase block
        """
        self.get_velo()
        #pixel pixel movement for more precise collisons
        
        steps = int(max(abs(self.vx), abs(self.vy)))
        for _ in range(steps):
            self.x += self.vx / steps
            self.colliding = self.collision_with_blocks(blocks)
            if self.colliding or self.x < 0 or self.x + self.length > tools.SCREEN_X:
                self.x -= self.vx / steps
                self.vx = 0
            self.y += self.vy / steps
            self.colliding = self.collision_with_blocks(blocks)
            if self.colliding or self.y < 0 or self.y + self.length > tools.SCREEN_Y:
                if self.vy > 0:
                    self.air_time = 0
                self.y -= self.vy / steps
                self.vy = 0
                
        #extra check to prevent player from getting stuck
        self.colliding = self.collision_with_blocks(blocks)
        while self.colliding:
            self.y -= 0.1
            self.colliding = self.collision_with_blocks(blocks)
                
        
    def collision_with_blocks(self, level_blocks):
        """
        Checks for collision between the player and various types of level blocks.

        Args:
            level_blocks (list): A list of block objects in the level. Each block must have attributes:
                - x (int): The x-coordinate of the block.
                - y (int): The y-coordinate of the block.
                - type (int): The type of the block (1-6).

        Returns:
            bool: True if a collision is detected with any block, False otherwise.

        Notes:
            - Uses pygame.Rect for collision detection.
            - also handles special cases for different block types such as finishing the level if colliding with a finish block
        """
        global  level_complete_se, game_over_se, jump_se, checkpoint_se, unlock_se, pause_panel_open, current_level, pause_panel_text
        colliding = False #assumes its not colliding
        self.touching_wall_side = False #assumes it is not touching wall
        for block in level_blocks: #iterate through each block in the level
            # Determine player rect based on block type
            if (block.type == 2 or block.type == 17) and self.vy >= 0:
            # Platform: only check feet to avoid getting stuck
                player_rect = pygame.Rect(self.x, self.y + self.length - 2, self.length, 2)
                block_rects = [pygame.Rect(block.rect)]
            else:
            # All other blocks: full player rect
                if self.p_type == 1:
                    player_rect = pygame.Rect(self.x, self.y, self.length, self.length)
                else:
                    player_rect = pygame.Rect(self.x + 3, self.y, self.length - 5, self.length)
                block_rects = []
                if block.rect != (0,0,0,0):
                    block_rects.append(pygame.Rect(block.rect))
                if block.rect2 != (0,0,0,0):
                    block_rects.append(pygame.Rect(block.rect2))
                                    
            for brect in block_rects: #iterate through the collision rectangles of each block (some may have have 2 checks such as corner blocks)
                if pygame.Rect(self.x - 5, self.y - 5, self.length + 10, self.length + 10).colliderect(brect): # bigger hitbox for checking if its touching wall 
                    self.touching_wall_side = True
                elif not self.touching_wall_side:
                    self.touching_wall_side = False

                if player_rect.colliderect(brect): #check normal collision for phyisics
                    if block.type in (1,3,4,5,6,7,8,9,10,16): #all blocks that are not listed below, normal phisics behaviour
                        if block.type == 16: #key wall
                            if self.user_power_ups[4] > 0: #if the user has a key
                                block.type = 17 #set the block to an empty key block
                                self.user_power_ups[4] -= 1 #take away the key
                                unlock_se.play() #play unlock sound
                        colliding = True
                    elif block.type == 2 or block.type == 17: #phase platform
                        if self.vy > 0: #only colliding if moving down
                            colliding = True
                    elif block.type == 11 or block.type == 15: #death block
                        self.make_new() #reset the player
                        game_over_se.play() # play game over sound
                        pause_panel_open = True # open the pause panel
                        Hud_buttons[2].enabled = True #enable pause button in that pannel
                        pause_panel_text = "You Died" #set text on pause panel
                        for power_up in power_ups: #reset each powerup
                            power_up.reset()
                        for block in blocks: #reset each block
                            block.reset()
                    elif block.type == 12: #checkpoint
                        for check_block in blocks: #check if there are any other checkpoints by iterating through blocks
                            if check_block.type == 12: # if its a checkpoint
                                block.collected = False #make it not active
                        if not checkpoint_se.get_num_channels(): #if checkpoint sound is not playing
                            checkpoint_se.play() #play it
                        block.collected = True #set current checkpoint to active checkpoint
                    elif block.type == 14: #finish block
                        tools.write_stats(self.user_power_ups[0], (current_level, round(self.time / 60, 1)), None) #wrtie to stats that you you finished the level and its time
                        if background_sound is not None: #if there is a background sound
                            background_sound.stop() #stop it
                        if not level_complete_se.get_num_channels(): #if the win sound is not playing
                            level_complete_se.play() #play it
                        tools.coins, tools.complete_levels, _, _ = tools.read_stats() #read stats to find complete levels and their times
                        best_time = tools.complete_levels.get(current_level, float("inf")) #find best time for current level, infinity if it isnt found
                        if best_time >= round(self.time/60, 1): #if best time is greater or equal than the attempts time
                            end_text = " Yay!!!" # add yay to the end of the pause panel text
                        else:
                            end_text = ""
                        pause_panel_text = f"Level Complete, time: {round(self.time/60, 1)}, best time: {best_time}{end_text}" # set pause panel text, displays current and best time
                        pause_panel_open = True #open the pause panel
                        Hud_buttons[2].enabled = False #disable the play button
        return colliding #return if the player is collinding
    
    def collison_with_power_ups (self):
        """
        Checks for collision between the player and power-ups, updating the player's power-up inventory if a collision occurs.
        """
        global coin_se
        player_rect = pygame.Rect(self.x, self.y, self.length, self.length) #rectangle for player, for collision
        for power_up in power_ups: # iterate through powerups
            if player_rect.colliderect(pygame.Rect(power_up.rect)): #if its colliding
                power_up.collected = True #set the powerup to collected
                self.user_power_ups[power_up.type - 1] += 1 #add that powerup to the users inventory
                coin_se.play() # play sound effect
                       
class Blocks:
    def __init__(self,type_num, grid_loc, g_size, b_imgs):
        """_summary_

        Args:
            type_num (int): block number, identifies block
            grid_loc (tuple): x, y for cell location in grid 
            g_size (float): size of of each cell in the grid
            b_imgs (lsit): list of images for each block type
        """
        self.type = type_num #indicates block type in tile map, 0 represents no block
        self.grid_location = grid_loc #location on grid
        self.x, self.y = get_loc_from_grid(self.grid_location, g_size) #get pixel coords for block
        self.animate_time = 0 # how far along in animation
        self.MAX_animate_time = 25 # after how many frames, restart the animation
        self.rect = (0,0,0,0) #collision rectangle
        self.rect2 = (0,0,0,0) #2nd collision rectangle, needed if block is not a rect (corner block)
        self.collected = False #for checkpoints
        self.g_size = g_size #grid size
        self.b_imgs = b_imgs #background images
        
    def go(self):
        """performs actions for blocks
            draws the block to the screen
        """
        self.draw()
        
    def reset(self):
        """resets the block for when restarting a level
        """
        if self.type == 17: # if its an opened key box
            self.type = 16 # close it
            
    def draw(self):
        """
        Draws a shape on the screen based on the object's type attribute.
        """
        if self.type not in (0, 14, 15): # if its not no block, or animated block (floor death and finish line)
            if self.b_imgs[self.type - 1] is not None: # if there is an image
                screen.blit(self.b_imgs[self.type - 1], (self.x, self.y)) # blit it to the screen
        elif self.type in (14, 15): #if it needs to be animated
            # Animate finish block by flipping through the image list at index self.type - 1
            self.animate_time += 1 # add 1 to length the frame has been shown for
            self.animate_time %= self.MAX_animate_time #modulus to the time it needs to restart the animation
            img_list = self.b_imgs[self.type - 1]
            #show image at index, split max animate into the number of photos there are, ex: if animate time/ max animate time = 0.33 and there are 2 images it will be the first frame
            img = img_list[int(self.animate_time / (self.MAX_animate_time / len(img_list)) % len(img_list))]
            screen.blit(img, (self.x, self.y)) #blit the image to the screen
        if self.type == 1: #if its a full block
            self.rect = (self.x, self.y, self.g_size, self.g_size) # set its collision rect
        elif self.type == 2  or self.type == 17: #phase block
            self.rect = (self.x, self.y + round(self.g_size*0.75), self.g_size, 2) # set its collision rect
        elif self.type == 3: #floor piece
            self.rect = (self.x, self.y + round(self.g_size*0.75), self.g_size, self.g_size*0.25) # set its collision rect
        elif self.type == 4: # if its a cieleing
            self.rect = (self.x, self.y, self.g_size, self.g_size*0.25) # set its rect
        elif self.type == 5: #left wall
            self.rect = (self.x, self.y, self.g_size*0.25, self.g_size) # set its collision rect
        elif self.type == 6: #right wall
            self.rect = (self.x + round(self.g_size*0.75), self.y, self.g_size*0.25, self.g_size) # set its collision rect
        elif self.type == 7:# corner piece
            self.rect = (self.x + round(self.g_size*0.75), self.y, self.g_size*0.25, self.g_size)# set its collision rect
            self.rect2 = (self.x, self.y + round(self.g_size*0.75), self.g_size, self.g_size*0.25)# set its 2nd collision rect
        elif self.type == 8:# corner piece
            self.rect = (self.x, self.y, self.g_size*0.25, self.g_size) # set its collision rect
            self.rect2 = (self.x, self.y + round(self.g_size*0.75), self.g_size, self.g_size*0.25)# set its 2nd collision rect
        elif self.type == 9: #corner piece
            self.rect = (self.x + round(self.g_size*0.75), self.y, self.g_size*0.25, self.g_size) # set its collision rect
            self.rect2 = (self.x, self.y, self.g_size, self.g_size*0.25) # set its 2nd collision rect
        elif self.type == 10: #corner piece 
            self.rect = (self.x, self.y, self.g_size, self.g_size*0.25) # set its collision rect
            self.rect2 = (self.x, self.y, self.g_size*0.25, self.g_size)# set its 2nd collision rect
        elif self.type == 11: #death block
            self.rect = (self.x, self.y, self.g_size, self.g_size) # set its collision rect
        elif self.type == 12: # checkpoint
            self.rect = (self.x, self.y, self.g_size, self.g_size)# set its collision rect
        elif self.type == 14: # finish line
            self.rect = (self.x, self.y, self.g_size*0.5, self.g_size) # set its collision rect
        elif self.type == 15: # floor death block
            self.rect = (self.x, self.y + round(self.g_size*0.75), self.g_size, self.g_size*0.25) # set its collision rect
        elif self.type == 16: # key block
            self.rect = (self.x, self.y, self.g_size, self.g_size) # set its collision rect
    
class Power_Ups:
    def __init__(self,type_num, grid_loc, g_size, p_imgs):
        """_summary_

        Args:
            type_num (int): powerup number, identifies powerup
            grid_loc (tuple): x, y for cell location in grid 
            g_size (float): size of of each cell in the grid
            p_imgs (lsit): list of images for each powerup type
        """
        self.type = type_num #indicates block type in tile map, 0 represents no block
        self.grid_location = grid_loc #location on grid
        self.x, self.y = get_loc_from_grid(self.grid_location, g_size) #gets pixel coords
        self.rect = (0,0,0,0) #collision rect
        self.collected = False #if the coin is collected
        self.g_size = g_size #grid size
        self.p_imgs = p_imgs #imgs
        
    def go(self):
        """
        performs powerup actions
        """
        self.draw() # draws to screen
        
    def reset(self):
        """
        resets for start if level
        """
        self.collected = False
    
    def draw(self):
        """
        Draws a shape on the screen based on the object's type attribute.
        """
        if self.collected: # its collected
            self.rect = (0,0,0,0) # no collision rect
        else:
            if self.type != 0: #if its not a no block
                self.rect = (self.x + 0.25*self.g_size, self.y + 0.25*self.g_size, 0.5*self.g_size, 0.5*self.g_size) # set its collide rect
                screen.blit(self.p_imgs[self.type - 1], (self.x, self.y)) # draw it

class Hud_Buttons:
    def __init__(self, x, y, img, g_size, type):
        """buttons that allow user to naviagte

        Args:
            x (int): x pos of buttons
            y (int): y pos of button
            img (pygame.surface): image of button
            g_size (float): size of grid
            type (int): type of button
        """
        self.x = x
        self.y = y
        self.img = img
        self.g_size = g_size
        self.type = type
        self.selected = False
        if self.type == 1: #pause button
            self.on_panel = False # on screen
        else: # other button
            self.on_panel = True #on pause panel
        self.enabled = True # if clicking button works
             
    def go(self):
        """runs all actions for buttons
        """
        global pause_panel_open
        if not self.on_panel or pause_panel_open:
            self.draw() # draw it
            self.selection() #check and do things if clicked
            
    
    def draw(self):
        """draw to screen
        """
        global pause_panel_open, pause_menu_img, pause_menu_long_img,pause_panel_text, retro_font_32
        if pause_panel_open and not self.on_panel: # if the pause panel is open and its the not on the pnale (so it only draws once)
            # Center the pause panel on the screen
            if len(pause_panel_text) > 15: # if the pause panel text is long
                img_coords = ((tools.SCREEN_X-pause_menu_long_img.get_width())*0.5, (tools.SCREEN_Y-pause_menu_img.get_height())*0.5)
                screen.blit(pause_menu_long_img, img_coords) #blit the long pause panel
            else: # if its not long
                img_coords = ((tools.SCREEN_X-pause_menu_img.get_width())*0.5, (tools.SCREEN_Y-pause_menu_img.get_height())*0.5)
                screen.blit(pause_menu_img, img_coords) # blit the regular one
            text_label = retro_font_32.render(pause_panel_text, True, tools.WHITE) # Center the heading text relative to the panel
            screen.blit(text_label, ((tools.SCREEN_X-text_label.get_width())*0.5,220)) # blit it

        screen.blit(self.img, (self.x, self.y)) #blit the image
        
    def selection(self):
        """
            checks if it clicked and performs action if it is
        """
        global pause_panel_open, pause_panel_text, background_img, background_sound
        img = self.img # set image to self.img for shorter length in next lines
        if input_info.left_mouse_down and pygame.Rect(self.x, self.y, img.get_width(), img.get_height()).collidepoint(input_info.xMouse, input_info.yMouse) and self.enabled: # if the left mouse is pressed, it is colliding with the mouse, and the buttons is active
            if self.type == 1:
                #pause button
                pause_panel_open = True #open pause panel
                Hud_buttons[2].enabled = True #enable play button
                pause_panel_text = "Pause" #panel text to pause
            elif self.type == 2:
                #home button
                tools.cloud_img = pygame.image.load("clouds.png").convert_alpha() #set cloud image back to original for menus
                background_sound = pygame.mixer.Sound("sound/music/Worldmap Theme.mp3") # set background sound to world map theme
                background_img = pygame.image.load("background.png").convert_alpha() #set background image to original for menus
                tools.game_state = "update_play_menu" #go update the play menu
            elif self.type == 3:
                #play button
                pause_panel_open = False #close the pause panel
            elif self.type == 4:
                #restart
                pause_panel_open = False # close pause panel
                for power_up in power_ups: #reset powerups
                    power_up.reset()
                for block in blocks: #reset blocks and checkpoints
                    block.collected = False
                    block.reset()
                player.make_new()# reset player
                
# your FUNCTIONS go here
def grid_to_class(level, level_class, g_size, imgs):
    """
    Converts a 2D level layout into a list of Blocks with their positions.

    Args:
        level (list of list): A 2D list representing the level, where each element corresponds to a block type.

    Returns:
        list: A list of Blocks objects, each initialized with the block type and its (x, y) position in the level grid.
    """
    output_block_list = [] 
    for i in range(len(level)): #iterate through level grid
        for j in range(len(level[i])):
            if level_class == "Block": # if its a block
                output_block_list.append(Blocks(level[i][j],(j,i), g_size, imgs)) #put each block in the class
            else: # if its not a block
                output_block_list.append(Power_Ups(level[i][j],(j,i), g_size, imgs)) # put each in the powerup class
    return output_block_list # return the list of block or powerup instances

def sign(num):
    """
    Returns the sign of a number.

    Args:
        num (float or int): The number to check.

    Returns:
        int: 1 if num is positive, -1 if num is negative, 0 if num is zero.
    """
    if num == 0: # if its zero
        return 0
    else:
        return int(abs(num)/num) # 1 for positive, -1 for negative, avoid if statements for code effincancy 
    
def get_loc_from_grid(g_loc, g_size):
        """
        Converts a grid location to pixel coordinates.

        Args:
            g_loc (tuple): A tuple (x, y) representing the grid location.

        Returns:
            tuple: A tuple (pixel_x, pixel_y) representing the pixel coordinates corresponding to the grid location.
        """
        x, y = g_loc #cell loction set to x and y
        return g_size*x, g_size*y #pixel coords of the cells top left
    
def load_images(grid_size):
    """loads many needed images for this file and sizes them properly

    Args:
        grid_size (float): size of the grid

    Returns:
        block_image_list (list): list of images for each block type
        power_up_image_list (list): list of images for each powerup type
        bg_img (pygame.Surface): background image
    """
    #blocks
    full_block = pygame.image.load("tiles for game/full block(1).png").convert_alpha()
    phase_block = pygame.image.load("tiles for game/phase block(2).png").convert_alpha()
    floor_block = pygame.image.load("tiles for game/floor piece(3).png").convert_alpha()
    roof_block = pygame.image.load("tiles for game/roof piece(4).png").convert_alpha()
    left_wall = pygame.image.load("tiles for game/left wall(5).png").convert_alpha()
    right_wall = pygame.image.load("tiles for game/right wall(6).png").convert_alpha()
    bottom_right_wall = pygame.image.load("tiles for game/bottom right wall(7).png").convert_alpha()
    bottom_left_wall = pygame.image.load("tiles for game/bottom left wall(8).png").convert_alpha()
    top_right_wall = pygame.image.load("tiles for game/top right wall(9).png").convert_alpha()
    top_left_wall = pygame.image.load("tiles for game/top left wall(10).png").convert_alpha()
    death_block = pygame.image.load("tiles for game/death block(11).png").convert_alpha()
    checkpoint = pygame.image.load("tiles for game/checkpoint(12).png").convert_alpha()
    spawn_block = pygame.image.load("tiles for game/spawn block(13).png").convert_alpha()
    finish_block1 = pygame.image.load("tiles for game/finish block 1(14).png").convert_alpha()
    finish_block2 = pygame.image.load("tiles for game/finish block 2(14).png").convert_alpha()
    floor_death_block1 = pygame.image.load("tiles for game/floor death piece1(15).png").convert_alpha()
    floor_death_block2 = pygame.image.load("tiles for game/floor death piece2(15).png").convert_alpha()
    key_block = pygame.image.load("tiles for game/key block(16).png").convert_alpha()
    key_empty_block = phase_block.copy()

    block_image_list = [
        full_block,
        phase_block,
        floor_block,
        roof_block,
        left_wall,
        right_wall,
        bottom_right_wall,
        bottom_left_wall,
        top_right_wall,  
        top_left_wall,
        death_block,
        checkpoint,
        spawn_block,
        [finish_block1,
        finish_block2],
        [floor_death_block1,
        floor_death_block2],
        key_block,
        key_empty_block
    ]
    
    for i in range(len(block_image_list)): # iterate through block imgs
        if isinstance(block_image_list[i], list): # if its list, menaing animation
            for j in range(len(block_image_list[i])): #iterate through again in case for animation
                block_image_list[i][j] = pygame.transform.scale(block_image_list[i][j], (grid_size, grid_size)) # scale image to grid size
        elif block_image_list[i] is not None: #if the image exists
            block_image_list[i] = pygame.transform.scale(block_image_list[i], (grid_size, grid_size)) # scale to grid_size
    
    #power ups
    coin = pygame.image.load("powerups for game/coin(1).png").convert_alpha()
    double_jump = pygame.image.load("powerups for game/double jump(2).png").convert_alpha()
    wall_jump = pygame.image.load("powerups for game/wall jump(3).png").convert_alpha()
    high_jump = pygame.image.load("powerups for game/high jump(4).png").convert_alpha()
    key = pygame.image.load("powerups for game/key(5).png").convert_alpha()

    power_up_image_list = [
        coin,
        double_jump,
        wall_jump,
        high_jump,
        key
    ]
    for i in range(len(power_up_image_list)): # iterate through powerup imgs
        if power_up_image_list[i] is not None: #if it exists
            power_up_image_list[i] = pygame.transform.scale(power_up_image_list[i], (grid_size, grid_size)) # scale to grid size
            
    #background
    bg_img = pygame.image.load("background.png").convert_alpha() #load deafult bg
    bg_img = pygame.transform.scale(bg_img, (tools.SCREEN_X, tools.SCREEN_Y)) #scale to screen size
            
    return block_image_list, power_up_image_list, bg_img

def draw_hud(power_up_list, imgs, font):
    """draws amount of powerups and coins, shows time passed

    Args:
        power_up_list (list): list of power up amounts
        imgs (list): list of powerup images
        font (font): font
    """
    x_offset = 10 #offset to start po
    y_offset = 10
    text_y = y_offset + (imgs[0].get_height() - 32) // 2 #y of text

    # Draw timer first, to the left of the powerups
    timer_text = font.render(f"time: {round(player.time / 60, 1)}", True, tools.BLACK) # fstring to set time
    screen.blit(timer_text, (x_offset, text_y)) #blit timer
    # Start powerups after the timer, with a little space
    powerup_x_start = x_offset + 200 # first x for powerup img
    img_x = powerup_x_start # set img x
    for i in range(len(power_up_list)): #iterate through powerups
        count = power_up_list[i] #amt of powerup
        if imgs[i] is not None: # if img exists
            img_width = imgs[i].get_width() # width of img
            text = font.render(str(count), True, tools.BLACK) #labelize the amt of powerup
            text_width = text.get_width() # get the width
            text_y = y_offset + (imgs[i].get_height() - text.get_height()) // 2 # get the y of the text
            screen.blit(imgs[i], (img_x, y_offset)) # blit the img
            screen.blit(text, (img_x + img_width + 1, text_y)) # blit the 
            img_x += img_width + text_width + 20 #add spacing for next text

def adiv_parser(file_path, background_img = None, background_sound = None, clouds_img= None):
    """parses .adiv level fiel

    Args:
        file_path (string): filepath of the .adiv file
        background_img (img, optional): default bg img. Defaults to None.
        background_sound (sound, optional): default bg sound. Defaults to None.
        clouds_img (img, optional): def clouds img. Defaults to None.

    Returns:
        blocks, powerups data as a grid for the level
        bg image and sound for the level
    """
    try:
        with open(file_path, "r") as f: #try opening the file
            data = json.load(f) #load the data
    except:
        # If file can't be read or parsed, return all defaults
        return [[0]*16 for _ in range(12)], [[0]*16 for _ in range(12)], background_img, background_sound, clouds_img

    def valid_grid(grid):
        """checks if grid is valid

        Args:
            grid (list): grid 

        Returns:
            if the grid is a valid length
        """
        return len(grid) == 12 and len(grid[0]) == 16

    blocks = data.get("blocks") #get the blocks data
    if not valid_grid(blocks): #if the blocks arent valid
        blocks = [[0]*16 for _ in range(12)] #make it all 0s

    powerups = data.get("powerups") #get powerup data
    if not valid_grid(powerups): # powerup data is invalid
        powerups = [[0]*16 for _ in range(12)] # grid of 0s

    image = data.get("image") # get image data
    try:
        image = pygame.image.load(image).convert_alpha() #try loading image
        image = pygame.transform.scale(image, (tools.SCREEN_X, tools.SCREEN_Y)) #rescalling to screen size
        clouds_img = None #and if theres and image then no clouds
    except: #if it doesnt wokr
        image = background_img #set img to default
        clouds_img = pygame.image.load("clouds.png") # and load clouds

    music = data.get("music") # music data
    try:
        music = pygame.mixer.Sound(music) # try loading the music
    except:
        music = background_sound # if it deosnnt work load bg music

    return blocks, powerups, image, music, clouds_img
        
def load_sounds():
    """loads all sound effects for game

    Returns:
        all of the sound effects
    """
    click = pygame.mixer.Sound("sound/click.mp3")
    level_complete = pygame.mixer.Sound("sound/level complete.mp3")
    game_over = pygame.mixer.Sound("sound/game over.mp3")
    jump = pygame.mixer.Sound("sound/jump.mp3")
    checkpoint = pygame.mixer.Sound("sound/checkpoint.mp3")
    coin = pygame.mixer.Sound("sound/coin.mp3")
    coin.set_volume(0.2) #adjust volume i would have done it more but the difference felt neglidgable
    unlock = pygame.mixer.Sound("sound/unlock.mp3")
    unlock.set_volume(10.0)
    use_powerup = pygame.mixer.Sound("sound/use powerup.mp3")
    
    return click, level_complete, game_over, jump, checkpoint, coin, unlock, use_powerup

def load_level(level_path):
    """given level path loads entire level 

    Args:
        level_path (string): filepath to .adiv
    """
    global background_img, background_sound, block_grid, powerup_grid, blocks, power_ups, current_level
    block_grid, powerup_grid, background_img, background_sound, tools.cloud_img = adiv_parser(level_path, background_img, background_sound, tools.cloud_img)   #play level x 
    blocks = grid_to_class(block_grid, "Block", GRID_SIZE, block_imgs) # replace blocks in class
    power_ups = grid_to_class(powerup_grid, "Power Ups", GRID_SIZE, power_up_imgs) #replace powerups in class
    player.make_new() # reset the player

    current_level = level_path # set current level to level path



# your GLOBAL variables go here
GRID_SIZE = 50
retro_font_32 = pygame.font.Font("upheavtt.ttf", 32)

tools.coins, tools.complete_levels, _, tools.selected_skin = tools.read_stats() #data from stats

block_imgs, power_up_imgs, background_img = load_images(GRID_SIZE) #set images
background_sound = pygame.mixer.Sound("sound/music/Worldmap Theme.mp3") #set default bg sound

click_se, level_complete_se, game_over_se, jump_se, checkpoint_se, coin_se, unlock_se, use_powerup_se = load_sounds() # load sounds

restart_img = pygame.image.load("menu icons/restart white.png").convert_alpha() #restart image from pause menu
restart_img = pygame.transform.scale(restart_img, (60, 60)) # resize

play_img = pygame.image.load("menu icons/play white.png").convert_alpha() #play image from pause menu
play_img = pygame.transform.scale(play_img, (60, 60)) #resize

pause_img = pygame.image.load("menu icons/pause.png").convert_alpha() #pause img
pause_img = pygame.transform.scale(pause_img, (32, 32)) #resize

home_img = pygame.image.load("menu icons/home white.png").convert_alpha() #home image from pause menu
home_img = pygame.transform.scale(home_img, (60, 60)) #resize

pause_menu_img = pygame.image.load("pause menu.png").convert_alpha()#image of pause menu
pause_menu_long_img = pygame.image.load("pause menu long.png").convert_alpha() #long pause menu

pause_menu_img = pygame. transform.scale(pause_menu_img, (350, 350*pause_menu_img.get_height()/pause_menu_img.get_width())) # resize to width 350 without hurting aspect ratio
pause_menu_long_img = pygame. transform.scale(pause_menu_long_img, (175*pause_menu_long_img.get_width()/pause_menu_long_img.get_height(), 175)) # resize to height 175

button_spacing = 70  # horizontal space between buttons
button_y_offset = 22 # y offset for buttons

Hud_buttons = [ # add buttons to hud class
    Hud_Buttons(760, 10, pause_img, GRID_SIZE, 1),  # Pause button (type 1)
    Hud_Buttons(tools.SCREEN_X // 2 - button_spacing - play_img.get_width(), tools.SCREEN_Y // 2 - play_img.get_height() // 2 + button_y_offset, home_img, GRID_SIZE, 2),  # home button (type 2)
    Hud_Buttons(tools.SCREEN_X // 2 - restart_img.get_width() // 2, tools.SCREEN_Y // 2 - restart_img.get_height() // 2 + button_y_offset, play_img, GRID_SIZE, 3), # play button (type 3)
    Hud_Buttons(tools.SCREEN_X // 2 + button_spacing, tools.SCREEN_Y // 2 - home_img.get_height() // 2 + button_y_offset, restart_img, GRID_SIZE, 4) # restart button (type 4)
]
pause_panel_open = False #pause panel starts as closed
pause_panel_text = "Pause" #default text "pause"

current_level = None #no current level to start

#not for code but dictionaries to identify each block num and the description
block_help = {0:"empty", 1:"full block", 2:"1/4 height, can phase from under", 3:"floor piece, cant penetrate", 4:"roof piece", 5:"left wall", 6:"right wall", 7:"bottom right wall", 8:"bottom left wall", 9:"top right wall", 10:"top left wall", 11:"death block, level reset if collided", 12:"checkpoint", 13:"spwan block (empty), top of player spawns on top of block", 14:"finish line block, if collided with block level is won", 15:"floor death piece", 16:"key locked wall", 17:"key block that is already collected, phase block"}
power_ups_help = {0:"no powerup", 1:"coin for skin shop", 2:"double jump", 3:"wall jump", 4:"high jump", 5:"key"}


if tools.selected_skin[1] == 2: #if type 2 skin
    player = Player(tools.person_imgs, tools.selected_skin[1]) #load the player person skin
else: #type 1
    player = Player(tools.type1_skins_imgs[tools.selected_skin[0]], tools.selected_skin[1]) #load image of selected skin from dict
    
load_level(None) # load level none to start
input_info = None # no user input info


def run_gameplay(): # while loop of this file 
    global screen, pause_panel_open, blocks, power_ups, player, Hud_buttons, power_up_imgs, retro_font_32, done, background_img, background_sound, input_info
    # MAIN LOOP    
    screen.blit(background_img, (0,0)) #blit bg
    tools.cloud_x = tools.draw_clouds(tools.cloud_img, tools.cloud_x) #animate cloud
    
    # Ensure background music is only played once and not overlapping
    if background_sound is not None: 
        if not pygame.mixer.get_busy() and not pause_panel_open:
            background_sound.play(-1)
        if pause_panel_open and pygame.mixer.get_busy():
            background_sound.stop()
    
    input_info, done = tools.check_input() #get user inputs
    
    player.R_pressed, player.L_pressed = input_info.R_pressed, input_info.L_pressed #set player class variables to user input variables
    
    if not pause_panel_open: #if the pause panel is closed
        player.go() # run player

        for block in blocks: # run blocks
            block.go()
            
        for power_up in power_ups: #run powerups
            power_up.go()
    else: # if its open
        player.draw() #only draw evrything dont perform other actions

        for block in blocks:
            block.draw()
            
        for power_up in power_ups:
            power_up.draw()
        
    draw_hud(player.user_power_ups, power_up_imgs, retro_font_32) # draw the hud
    
    for button in Hud_buttons: # run hud buttons
        button.go()

    # set player just jumped to user input class values
    player.just_jumped = input_info.just_jumped 
    

    # this line draws everything into the window all at once
    pygame.display.flip()
    # this line limits the frames per second to 60
    clock.tick(60)
    
    return done #return done so main can close properly
    

if __name__ == '__main__': # if in this file and not from import (for testing)
    while not done: #run it
        run_gameplay()
    pygame.quit()