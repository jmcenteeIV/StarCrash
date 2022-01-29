from pygame.sprite import Sprite
from pygame.constants import K_LEFT, K_RIGHT, K_DOWN, K_UP

import pygame


vec = pygame.math.Vector2

class Baddies(pygame.sprite.Sprite):
    """
    Currently repersents a single enemy
    """

    # TODO (matthew.moroge) will probably need to the class for the screen as a param and use super()
    def __init__(self, width, height, start_position, speed, aggression):
        super().__init__()
        """
        Initialize the alien and set its starting position
        """
        
        # load enemy image when we have it
        # self.image = loader.load_image('/path/to/file')
        # self.image.convert_alpha()
        # self.rect = self.enemy.image.get_rect()

        # creating basic rect for beginning, change to image later
        # gonna need to import the screen variable for the rect

        self.width = width
        self.height = height
        self.aggression = aggression
        self.image = pygame.Surface((50, 50))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect( center = (50,50))

        # self.rect = pygame.draw.rect((screen, 0, 0, 255), (20, 20, 160,160))

        self.speed = speed
        self.counter = 0
        self.pos = vec(start_position)
        

    def update(self):
        self.move()

    def move(self):
        """
        moving the enemy
        """

        self.pos.x += self.speed

        if self.pos.x > (self.width - (self.rect.width/2)):
            self.pos.x, self.speed = (self.width - (self.rect.width/2)), self.speed * -1
        if self.pos.x < (self.rect.width/2):
            self.pos.x, self.speed = (self.rect.width/2) , self.speed * -1

        self.rect.midbottom = self.pos

    