from xml.sax.handler import DTDHandler
from lib import resources
import pygame.math as math
import random as randy
import pygame
import lib


vec = pygame.math.Vector2

class Baddies(pygame.sprite.Sprite):
    """
    Currently repersents a single enemy
    """

<<<<<<< HEAD
    
    def __init__(self, width, height, start_position, speed, aggression):
=======
    # TODO (matthew.moroge) will probably need to the class for the screen as a param and use super()
    def __init__(self, image, height, width, start_position, speed, aggression):
>>>>>>> bc84cf03d1972d23f033c8dc5745039323d6aa58
        super().__init__()
        """
        Initialize the alien and set its starting position
        """
        
        # load enemy image when we have it
        # self.image = loader.load_image('/path/to/file')
        # self.image.convert_alpha()
        # self.rect = self.enemy.image.get_rect()

        self.health = 10

        self.width = width
        self.height = height
        self.aggression = aggression
        self.image = image
        self.rect = self.image.get_rect( center = (50,50))
        # self.pos = vec(start_position)
        # self.speed = speed

        self.resources = resources.Resources.instance()

        """
        adding movement options for random movements
        """

        # storing a copy of the image to try out rotation 
        self.rotate_img = self.image.copy()
        # random vector for enemy 
        self.direction = pygame.Vector2(0, 0)
        while self.direction.length() == 0:
            self.direction = pygame.Vector2(randy.uniform(1, 4), randy.uniform(1, 4))

        # constant random speed for enemy
        self.direction.normalize_ip()
        self.speed = randy.uniform(1, 5)

        # storing the position in a vector, because math is hard
        self.pos = pygame.Vector2(self.rect.center)

        # let's play around with some rotation to make it look cool 
        self.rotation = randy.uniform(0.3, 1)
        self.angle = 0
        
        
        

    def update(self):
        """
        Refreshing enemy on screen and catching events in real time
        """
        self.move()
        self.take_damage()        



    def move(self):
        """
        moving the enemy
        """

        self.pos += self.direction * self.speed 
        self.angle += self.rotation 
        self.image = pygame.transform.rotate(self.rotate_img, self.angle)

        self.rect = self.image.get_rect(center=self.pos)
        
        

        

    def take_damage(self):
        """
        
        """
        
        player_bullet = self.resources.update_groups['player_bullet']
        player = self.resources.update_groups['player']
        

        """
        1st arg: name of sprite I want to check
        2nd arg: name of group I want to compare against
        3rd arg: True/False reference to dokill which either deletes the object in 1st arg or not
        """
        hits = pygame.sprite.spritecollide(self, player_bullet, True)

        
        
