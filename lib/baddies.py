from re import X
from pygame.sprite import Sprite
import Game
import loader
import pygame



class bad_guy(Sprite):
    """
    Currently repersents a single enemy, but can be used to spawn multiple enemies when used as an object
    """

    # TODO (matthew.moroge) will probably need to the class for the screen as a param and use super()
    def __init__(self, x, y):
        """
        Initialize the alien and set its starting position
        """
        
        # load enemy image when we have it
        # self.image = loader.load_image('/path/to/file')
        # self.image.convert_alpha()
        # self.rect = self.enemy.image.get_rect()

        # creating basic rect for beginning, change to image later
        # gonna need to import the screen variable for the rect
        self.screen = pygame.Surface((50, 50))
        self.rect = pygame.draw.rect((self.screen, 0, 0, 255), (20, 20, 160,160))

        # base enemy speed, trying out 10, can be changed 
        self.enemy_speed = 10

        # enemy base health, can be changed
        self.health = 10
        
        # x: horizantial movement 
        # y: vertical movement 
        # counter: keeping track of movement axis
        self.rect.x = x 
        self.rect.y = y 
        self.counter = 0


    def move(self):
        """
        moving the enemy
        """
        # adjust to screen size for better movement strides 
        distance = 80

        if self.counter >= 0 and self.counter <= distance:
            self.rect.x += self.enemy_speed
        elif self.counter >= distance and self.counter <= distance * 2:
            self.rect.x -= self.enemy_speed
        else:
            self.counter = 0

        self.counter += 1

    def close_to_edge(self):
        """
        checking if enemy is at edge of screen
        """
        screen_rect = self.screen.get_rect()

        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
