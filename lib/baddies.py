from pygame.sprite import Sprite
from pygame.constants import K_LEFT, K_RIGHT, K_DOWN, K_UP

import pygame
import random

# applies a 2-Dimensional Vector
vec = pygame.math.Vector2

class bad_guy(Sprite):
    """
    Currently repersents a single enemy, but can be used to spawn multiple enemies when used as an object
    """

    def __init__(self, height, width, acceleration, friction):
        super().__init__()
        """
        Initialize the alien and set its starting position
        """
        
        # load enemy image when we have it
        # self.image = loader.load_image('/path/to/file')
        # self.image.convert_alpha()
        # self.rect = self.enemy.image.get_rect()

        # basic handling for enemy movement 
        self.friction = friction
        self.acceleration = acceleration

        # screen variables
        self.width = width
        self.height = height

        # creating basic rect for beginning, change to image later
        # gonna need to import the screen variable for the rect
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((128,255,40))
        self.rect = pygame.draw.rect((self.screen, 0, 0, 255), (20, 20, 160,160))


        # enemy base health, can be changed
        self.health = 10
        
        # pos: starting position for enemy 
        # vel: elocity with which it should move across the window
        # acc: enemy acceleration
        self.pos = vec((width/2, height))
        self.vel = vec(0,0)
        self.acc = vec(0,0)

    def blitme(self):
        """Draw the enemy at its current location."""
        self.surf.blit(self.image, self.rect)


    def move(self):
        """
        moving the enemy
        """   
        free_real_estate = ['top', 'topleft', 'topright', 'midtop', 'midleft', 'midright', ]
        randy_appear = random.choice(free_real_estate)

        self.pos.x += self.speed

        if self.pos.x > (self.width - (self.rect.width/2)):
            self.pos.x, self.speed = (self.width - (self.rect.width/2)), self.speed * -1
        if self.pos.x < (self.rect.width/2):
            self.pos.x, self.speed = (self.rect.width/2) , self.speed * -1

        # starting position for enemy spawn before movement 
        # starting at top left of screen
        self.rect.topleft = self.pos

    def update(self):
        """
        updating enemy movement to the screen 
        """
        self.move()

        # handling co

    def switch_mode(self):
        """
        switching to mech mode
        """
        pass 

    