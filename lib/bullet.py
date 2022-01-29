import pygame
from pygame.constants import K_LEFT, K_RIGHT, K_DOWN, K_UP


vec = pygame.math.Vector2

class Bullet(pygame.sprite.Sprite):

    def __init__(self, height, velocity, pos):
        super().__init__()
        self.height = height
        self.image = pygame.Surface((30, 30))
        self.image.fill((128,255,40))
        self.rect = self.image.get_rect(center=pos)
        # self.image = loader.load_image('assets/images/ejike.png')
        # self.rect = self.image.get_rect(center = (100, 420))

        self.pos = (pos)
        self.vel = vec(0, velocity)

    def update(self):
        self.move()
    
    def move(self):
        self.pos -= self.vel
        if self.pos.y > self.height:
            self.kill()
        self.rect.midbottom = self.pos