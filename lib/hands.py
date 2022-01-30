import pygame
from pygame.constants import K_LEFT, K_RIGHT, K_DOWN, K_UP

from lib import resources

vec = pygame.math.Vector2

class Hands(pygame.sprite.Sprite):

    def __init__(self, velocity, pos, left, image):
        super().__init__()
        #Sprite Properties
        self.image = image
        self.rect = self.image.get_rect(center=pos)

        #References
        self.res = resources.Resources.instance()
        self.game = self.res.game
        self.left = left
        #Motion Properties
        self.pos = (pos)

    def move(self, pos):
        if self.left:
            self.rect.bottomright = pos
        else:
            self.rect.bottomleft = pos
