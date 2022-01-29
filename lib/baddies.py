from pygame.sprite import Sprite
import pygame



class bad_guy(Sprite):
    """
    Currently repersents a single enemy
    """

    # TODO (matthew.moroge) will probably need to the class for the screen as a param and use super()
    def __init__(self, **kwargs):
        """
        Initialize the alien and set its starting position
        """

        # load enemy image when we have it
        # self.image = pygame.image.load('path/to/image')
        # self.rect = self.enemy.image.get_rect()

        # creating basic rect for beginning, change to image later
        # gonna need to import the screen variable for the rect

        self.rect = pygame.draw.rect((0, 0, 255), (20, 20, 160,160))
        # Starting each enemy near the top left of screen, can change later
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # tracking enemy horizontal speed for fine tuning later on
        self.x = float(self.rect.x)

        # tracking enemy vertical speed for fine tuning later on
        self.y = float(self.rect.y)

