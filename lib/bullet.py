import pygame
from pygame.constants import K_LEFT, K_RIGHT, K_DOWN, K_UP

from lib import resources

vec = pygame.math.Vector2

class Bullet(pygame.sprite.Sprite):

    def __init__(self, velocity, pos, image):
        super().__init__()
        #Sprite Properties
        self.image = image
        self.rect = self.image.get_rect(center=pos)

        #References
        self.res = resources.Resources.instance()
        self.game = self.res.game

        #Motion Properties
        self.pos = (pos)
        self.vel = vec(0, velocity)

    def update(self):
        self.move()
    
    def move(self):
        self.pos -= self.vel
        if self.pos.y < 0 - self.rect.height:
            self.kill()
        self.rect.midbottom = self.pos