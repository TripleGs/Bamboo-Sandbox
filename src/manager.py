import pygame
import random
import time

from src.bamboo import Bamboo
 
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

        #Game variables
        self.running = False

    #Draws the background
    def draw_background(self):
        self.screen.fill((20,80,140))

    #Draws the ground
    def draw_ground(self):
        pygame.draw.rect(self.screen, (0,0,0), pygame.Rect(0, 440, 500, 60))

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
            self.check_events()
            self.draw()
        pygame.quit()
