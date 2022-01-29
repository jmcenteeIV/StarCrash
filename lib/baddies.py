<<<<<<< HEAD
from pygame.sprite import Sprite
from pygame.constants import K_LEFT, K_RIGHT, K_DOWN, K_UP
import loader
import pygame

# applies a 2-Dimensional Vector
=======
import pygame


>>>>>>> 5b7e7d72c4b3e072add23ffff525661d41bf3c7f
vec = pygame.math.Vector2

class Baddies(pygame.sprite.Sprite):
    """
    Currently repersents a single enemy, but can be used to spawn multiple enemies when used as an object
    """

<<<<<<< HEAD
    def __init__(self, height, width, acceleration, friction):
=======
    # TODO (matthew.moroge) will probably need to the class for the screen as a param and use super()
    def __init__(self, width, height, start_position, speed, aggression):
>>>>>>> 5b7e7d72c4b3e072add23ffff525661d41bf3c7f
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

<<<<<<< HEAD

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
=======
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
        
>>>>>>> 5b7e7d72c4b3e072add23ffff525661d41bf3c7f

    def update(self):
        self.move()

    def move(self):
        """
        moving the enemy
<<<<<<< HEAD
        """   
        

        self.pos.x += self.speed

        if self.pos.x > (self.width - (self.rect.width/2)):
            self.pos.x, self.speed = (self.width - (self.rect.width/2)), self.speed * -1
        if self.pos.x < (self.rect.width/2):
            self.pos.x, self.speed = (self.rect.width/2) , self.speed * -1

        self.rect.midbottom = self.pos

        # starting position for enemy spawn before movement 
        # starting at top left of screen
        self.rect.topleft = self.pos

    def update(self):
        """
        updating enemy movement to the screen 
        """
        self.move()

    def switch_mode(self):
        """
        switching to mech mode
        """
        pass 

    
=======
        """

        self.pos.x += self.speed

        if self.pos.x > (self.width - (self.rect.width/2)):
            self.pos.x, self.speed = (self.width - (self.rect.width/2)), self.speed * -1
        if self.pos.x < (self.rect.width/2):
            self.pos.x, self.speed = (self.rect.width/2) , self.speed * -1

        self.rect.midbottom = self.pos
>>>>>>> 5b7e7d72c4b3e072add23ffff525661d41bf3c7f
