import pygame
import random
import math
from time import time

class Leaf:
    def __init__(self, screen, x, y, left, size):
        self. screen = screen

        #Location of leaf
        self.x = x
        self.y = y
        self.original_y = y
        self.original_x = x

        #Size of the leaf
        self.leaf_length = 2
        self.leaf_width = 1

        #Max size of leaf
        self.width_max = size
        self.length_max = size*2

        #Growth time of leaf
        self.last_growth = time()
        self.growth_time = 8

        #Left side of bamboo tree?
        self.left = left

        #Image
        self.img = None
        self.img_name = random.choice(['assets/bamboo/bamboo_leaf_1.png',
                                       'assets/bamboo/bamboo_leaf_2.png'])
        
        #Falling properties
        self.falling = False
        self.fall_speed = random.uniform(0.3, 0.7)  # Randomize fall speed
        self.sway_amount = random.uniform(1.0, 3.0)  # Randomize sway amount
        self.sway_speed = random.uniform(0.05, 0.15)  # Randomize sway speed
        self.fall_time = 0
        self.rotation = 0
        self.rotation_speed = random.uniform(-2, 2)  # Randomize rotation speed
        self.grounded = False

    #Grows leaf
    def grow(self):
        #Increase size of leaf
        self.leaf_width += 1
        self.leaf_length += 2

        #Modify if located on the left
        if self.left: self.x -= 2

    #Draws leaf
    def draw(self):
        #If falling, move down with sway
        if self.falling:
            if not self.grounded:
                # Update fall time
                self.fall_time += 0.016  # Approximate time between frames
                
                # Move down
                self.y += self.fall_speed
                
                # Add swaying motion using sine wave
                self.x = self.original_x + math.sin(self.fall_time * self.sway_speed * 10) * self.sway_amount
                
                # Rotate as it falls
                self.rotation += self.rotation_speed
                
                # Check if reached ground
                if self.y >= 435:  # Just above ground level
                    self.y = 435  # Place on top of ground
                    self.grounded = True
                    # Random final rotation to make it look natural on ground
                    self.rotation = random.uniform(-45, 45)
            
        #If time for the leaf to grow, grow it
        elif self.leaf_width < self.width_max and time() - self.last_growth > self.growth_time:
            self.grow()
            self.last_growth = time()

        #Reload, update, and draw image and update leaf image
        self.img = pygame.image.load(self.img_name)
        if not self.left: self.img = pygame.transform.flip(self.img, True, False)
        self.img = pygame.transform.scale(self.img, (self.leaf_length, self.leaf_width))
        
        # Rotate image if falling or grounded
        if self.falling or self.grounded:
            self.img = pygame.transform.rotate(self.img, self.rotation)
            
        # Calculate position accounting for any size change from rotation
        rect = self.img.get_rect()
        rect.center = (self.x + self.leaf_length//2, self.y + self.leaf_width//2)
        
        self.screen.blit(self.img, rect)
        
    def start_falling(self):
        self.falling = True
        self.fall_time = 0

class Segment:
    def __init__(self, screen, x, y, width, height):
        self.screen = screen

        #Tracks dimensions of segment
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.original_img = pygame.image.load('assets/bamboo/bamboo_segment.png')
        self.img = self.original_img.copy()
        self.dying_img = None
        self.dying = False
        self.position_y = y  # Store the original position Y for comparison

        #Edits image
        self.img = pygame.transform.scale(self.img, (self.width, self.height))

    #Draws the segment
    def draw(self):
        if self.dying and not self.dying_img:
            # Create a darkened version of the segment
            self.dying_img = self.original_img.copy()
            darkened_surface = pygame.Surface(self.dying_img.get_size(), pygame.SRCALPHA)
            darkened_surface.fill((50, 50, 50, 0))  # Transparent dark overlay
            self.dying_img.blit(darkened_surface, (0, 0), special_flags=pygame.BLEND_RGB_SUB)
            self.dying_img = pygame.transform.scale(self.dying_img, (self.width, self.height))
            
        image_to_use = self.dying_img if self.dying else self.img
        self.screen.blit(image_to_use, (self.x, self.y))
    
    def start_dying(self):
        self.dying = True
        
class Bamboo:
    def __init__(self, screen, x):
        self.screen = screen

        #Tracks the hieght, width, color, and location of the bamboo
        self.height = 2
        self.x = x
        self.width = random.randint(5,20)
        self.color = (0,160,0)
        self.max_height = random.randint(30*self.width, 35*self.width)
        self.original_img = pygame.image.load('assets/bamboo/bamboo_stem.png')
        self.img = self.original_img.copy()
        self.dying_img = None

        #Tracks growth info
        self.growth_speed = 1
        self.growth_chance = 1  # Restored growth chance
        self.growth_amount = 2
        self.last_grown = time()

        #Tracks death info
        self.die_amount = self.growth_amount
        self.dying = False
        self.die_speed = self.growth_speed / 3  # 3x faster than growth
        self.die_chance = 1  # Restored die chance
        self.last_die = time()

        #Tracks spread info
        self.spread_speed = 5
        self.spread_chance = 10
        self.last_spread = time()

        #Tracks the leaves
        self.leaf_cords = []
        self.leaf_chance = 8
        self.leaf_size = self.width*.7

        #Tracks the segments
        self.segments = []
        self.segment_distance = 2*self.width
        self.segment_thickness = int(self.width/3)

        #Tracks wind
        self.wind = False

    #Grows the plant
    def grow(self):
        self.height +=self.growth_amount
        if random.randint(0,self.leaf_chance) == self.leaf_chance and self.height > 10: self.add_leaf()
        if self.height % self.segment_distance == 0: self.add_segment()

    #Calculates the max height
    def calculate_max_height(self):
        # Allow bamboo to grow up to 80% of screen height
        screen_height = self.screen.get_height()
        self.max_height = int(screen_height * 0.8)
        
    #Adds a segment
    def add_segment(self):
        segment_y = 440-self.height
        self.segments.append(Segment(self.screen, self.x, segment_y, self.width, self.segment_thickness))
        
    #Checks if the plant grows
    def check_if_grow(self):
        if self.dying: return False
        if self.height >= self.max_height: 
            self.dying = True  # Start dying when max height is reached
            return False
            
        #If it would be time for the plant to grow, reset timer
        if time() - self.last_grown >= self.growth_speed:
            self.last_grown = time()
        else: return False  # Restored early return

        #Determine if growing actually grows - restored randomness
        if random.randint(0, self.growth_chance) == self.growth_chance: 
            self.grow()
            
        return True

    #Adds a leaf to draw
    def add_leaf(self):
        x_mod, left = 0, False
        if random.randint(0,1) == 1: x_mod+=self.width
        else:
            x_mod -= 2
            left =True
        self.leaf_cords.append(Leaf(self.screen, self.x+x_mod, 440-self.height, left, self.leaf_size))

    #Draws the stem of the plant
    def draw_stem(self):
        if self.dying and not self.dying_img:
            # Create a darkened version of the stem
            self.dying_img = self.original_img.copy()
            darkened_surface = pygame.Surface(self.dying_img.get_size(), pygame.SRCALPHA)
            darkened_surface.fill((50, 50, 50, 0))  # Transparent dark overlay
            self.dying_img.blit(darkened_surface, (0, 0), special_flags=pygame.BLEND_RGB_SUB)
        
        image_to_use = self.dying_img if self.dying else self.img
        scaled_img = pygame.transform.scale(image_to_use, (self.width, self.height))
        self.screen.blit(scaled_img, (self.x, 440-self.height))

    #Draws the plant.
    def draw(self):
        self.check_if_grow()
        self.check_if_die()
        if self.check_if_dead():
            self.draw_stem()
            self.draw_leaves()
            self.draw_segments()
            return True
        else:
            return False

    #Draws the segments
    def draw_segments(self):
        # Only draw segments that are at or below the current top of the bamboo
        current_top = 440 - self.height
        segments_to_draw = [segment for segment in self.segments if segment.y >= current_top]
        
        for segment in segments_to_draw:
            segment.draw()

    #Draws the leaves of the plant
    def draw_leaves(self):
        for leaf in self.leaf_cords:
            leaf.draw()

    #Responds to the weather
    def respond_to_weather(self, weather):
        pass

    def check_if_spread(self):
        if self.height >= self.max_height or self.height < 10: return False

        if time() - self.last_spread >= self.spread_speed:
            self.last_spread = time()
        else: return False

        if random.randint(0,self.spread_chance) == self.spread_chance: return True
        return False
    
    def check_if_die(self):
        if not self.dying: 
            return False
        
        # Check if it's time to decrease height
        if time() - self.last_die >= self.die_speed:
            self.last_die = time()
        else: return False  # Restored early return

        # Restore random chance of dying
        if random.randint(0, self.die_chance) == self.die_chance:
            self.die()
            
        return True
    
    def die(self):
        # Calculate the height before reduction
        old_height = self.height
        
        # Reduce the height
        self.height -= self.die_amount
        
        # Make leaves fall when they reach the current height point
        current_top = 440 - self.height
        for leaf in self.leaf_cords:
            if not leaf.falling and leaf.original_y <= current_top:
                leaf.start_falling()
                
        # Make all segments darken when the bamboo is dying
        for segment in self.segments:
            if not segment.dying:
                segment.start_dying()

    def check_if_dead(self):
        if self.height <= 0:
            return False  # Bamboo is dead, will be removed
        else:
            return True  # Bamboo is still alive

