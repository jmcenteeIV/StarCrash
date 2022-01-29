from pygame.sprite import Sprite
import loader
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
        # self.image = loader.load_image('/path/to/file')
        # self.image.convert_alpha()
        # self.rect = self.enemy.image.get_rect()

        # creating basic rect for beginning, change to image later
        # gonna need to import the screen variable for the rect

        self.rect = pygame.draw.rect((screen, 0, 0, 255), (20, 20, 160,160))

        # Starting each enemy near the top left of screen, can change later
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # enemy speed
        self.enemy_speed = 1.0

        # tracking enemy horizontal speed for fine tuning later on
        self.x = float(self.rect.x)

        # tracking enemy vertical speed for fine tuning later on
        self.y = float(self.rect.y)


    def move(self):
        """
        moving the enemy
        """
        self.x += self.enemy_speed
        self.rect.x = self.x 

    def close_to_edge(self):
        """
        checking if enemy is at edge of screen
        """
        screen_rect = self.screen.get_rect()

        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """
        moving enemy left or right
        """
        self.x += self.enemy_speed
        self.rect.x = self.x 
