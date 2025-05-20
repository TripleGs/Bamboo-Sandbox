import pygame
import random
import time

from src.bamboo import Bamboo
from src.ground import Ground
from src.day_night import DayNightCycle
 
class Game:

    #Creates Window
    def __init__(self, game_name, width, height):
        pygame.init()
        pygame.display.set_caption(game_name)

        #Defines window details
        self.width, self.height = width, height
        self.screen = pygame.display.set_mode((width, height))
        self.game_name = game_name

        self.bamboos = [Bamboo(self.screen,100),
                        Bamboo(self.screen,50),
                        Bamboo(self.screen,70),
                        Bamboo(self.screen,300),
                        Bamboo(self.screen,420)]
        
        # Initialize ground, day/night cycle
        self.ground = Ground(self.screen)
        self.day_night = DayNightCycle(self.screen)
        
        # Game variables
        self.running = False
        self.clock = pygame.time.Clock()
        self.last_time = time.time()

    #Draws the background
    def draw_background(self):
        self.day_night.draw()

    #Draws the ground
    def draw_ground(self):
        self.ground.draw()

    #Draws the trees
    def draw_bamboos(self):
        for bamboo in self.bamboos:
            bamboo.draw()
        
    #Draws the elements on the screen
    def draw(self):
        self.draw_background()
        self.draw_ground()
        self.draw_bamboos()
        pygame.display.flip()
        
    #Checks the events
    def check_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

    #Starts the game   
    def start(self):
        self.running = True

        while self.running:
            # Calculate delta time
            current_time = time.time()
            dt = current_time - self.last_time
            self.last_time = current_time
            
            # Update day/night cycle
            self.day_night.update(dt)
            
            self.check_events()
            self.draw()
            self.clock.tick(60)  # Cap at 60 FPS
            
        pygame.quit()
