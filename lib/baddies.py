from re import X
from pygame.sprite import Sprite
from pygame.constants import K_LEFT, K_RIGHT, K_DOWN, K_UP
import Game
import loader
import pygame

# applies a 2-Dimensional Vector
vec = pygame.math.Vector2

class bad_guy(Sprite):
    """
    Currently repersents a single enemy, but can be used to spawn multiple enemies when used as an object
    """

    # TODO (matthew.moroge) will probably need to the class for the screen as a param and use super()
    def __init__(self, height, width, acceleration, friction):
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
        self.acc = vec(0,0)
    
        pressed_keys = pygame.key.get_pressed()

        #  Horizontal movement for key presses 
        # x: hortizontal axis movement         
        if pressed_keys[K_LEFT]:
            self.acc.x = -self.acceleration
        if pressed_keys[K_RIGHT]:
            self.acc.x = self.acceleration

        self.acc.x += self.vel.x * self.friction
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > (self.width - (self.rect.width/2)):
            self.pos.x, self.acc.x = (self.width - (self.rect.width/2)), 0
        if self.pos.x < (self.rect.width/2):
            self.pos.x, self.acc.x = (self.rect.width/2) , 0

        #  Vertical movement for key presses
        # y: vertical axis movement 
        if pressed_keys[K_DOWN]:
            self.acc.y = self.acceleration
        if pressed_keys[K_UP]:
            self.acc.y = -self.acceleration

        # applying fricition to enemey movement 
        self.acc.y += self.vel.y * self.friction
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.y > self.height:
            self.pos.y, self.acc.y = self.height, 0
        if self.pos.y < self.rect.height:
            self.pos.y, self.acc.y = (0 + self.rect.height), 0

        # starting position for enemy spawn before movement 
        # starting at top left of screen
        self.rect.topleft = self.pos

    def update(self):
        """
        updating enemy movement to the screen 
        """
        self.move()

    def close_to_edge(self):
        """
        checking if enemy is at edge of screen
        """
        screen_rect = self.surf.get_rect()

        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
