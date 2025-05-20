import pygame
import random
from time import time

#Rotating bamboo
#https://stackoverflow.com/questions/36510795/rotating-a-rectangle-not-image-in-pygame
#https://www.youtube.com/watch?v=BzsCqL9l8SM

class Leaf:
    def __init__(self, screen, x, y, left, size):
        self. screen = screen

        #Location of leaf
        self.x = x
        self.y = y

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

    #Grows leaf
    def grow(self):

        #Increase size of leaf
        self.leaf_width += 1
        self.leaf_length += 2

        #Modify if located on the left
        if self.left: self.x -= 2

    #Draws leaf
    def draw(self):

        #If time for the leaf to grow, grow it
        if self.leaf_width <self.width_max and time() - self.last_growth > self.growth_time:
            self.grow()
            self.last_growth = time()

        #Reload, update, and draw image and update leaf image
        self.img = pygame.image.load(self.img_name)
        if not self.left: self.img = pygame.transform.flip(self.img, True, False)
        self.img = pygame.transform.scale(self.img, (self.leaf_length, self.leaf_width))
        self.screen.blit(self.img, (self.x,self.y))

class Segment:
    def __init__(self, screen, x, y, width, height):
        self.screen = screen

        #Tracks dimensions of segment
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.img = pygame.image.load('assets/bamboo/bamboo_segment.png')

        #Edits image
        self.img = pygame.transform.scale(self.img, (self.width, self.height))

    #Draws the segment
    def draw(self):
        self.screen.blit(self.img, (self.x,self.y))
        
class Bamboo:
    def __init__(self, screen, x):
        self.screen = screen

        #Tracks the hieght, width, color, and location of the bamboo
        self.height = 2
        self.x = x
        self.width = random.randint(5,20)
        self.color = (0,160,0)
        self.max_height = random.randint(10*self.width, 20*self.width)
        self.img = pygame.image.load('assets/bamboo/bamboo_stem.png')

        #Tracks growth info
        self.growth_speed = 1
        self.growth_chance = 1
        self.last_grown = time()
        self.growth_amount = 2

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
        self.segments.append(Segment(self.screen, self.x, 440-self.height, self.width, self.segment_thickness))
        
    #Checks if the plant grows
    def check_if_grow(self):
        if self.height >= self.max_height: return False
        #If it would be time for the plant to grow, reset timer
        if time() - self.last_grown >= self.growth_speed:
            self.last_grown = time()
        else: return False

        #Determine if growing actually grows
        if random.randint(0,self.growth_chance)== self.growth_chance: self.grow()
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
        self.img = pygame.transform.scale(self.img, (self.width, self.height))
        self.screen.blit(self.img, (self.x, 440-self.height))

    #Draws the plant.
    def draw(self):
        self.check_if_grow()
        self.draw_stem()
        self.draw_leaves()
        self.draw_segments()

    #Draws the segments
    def draw_segments(self):
        for segment in self.segments:
            segment.draw()

    #Draws the leaves of the plant
    def draw_leaves(self):
        for leaf in self.leaf_cords:
            leaf.draw()

    #Responds to the weather
    def respond_to_weather(self, weather):
        pass
