import pygame
import random
from time import time

class Ground:
    def __init__(self, screen):
        self.screen = screen
        self.dirt_img = pygame.image.load('assets/dirt.png')
        self.dirt_size = 10  # Size of each dirt block
        self.ground_height = 60  # Height of ground in pixels
        self.ground_y = 440  # Y position of ground
        
    def draw(self):
        # Calculate how many dirt blocks we need
        num_blocks_x = self.screen.get_width() // self.dirt_size + 1
        num_blocks_y = self.ground_height // self.dirt_size + 1
        
        # Draw dirt blocks
        for y in range(num_blocks_y):
            for x in range(num_blocks_x):
                pos_x = x * self.dirt_size
                pos_y = self.ground_y + (y * self.dirt_size)
                self.screen.blit(self.dirt_img, (pos_x, pos_y))
