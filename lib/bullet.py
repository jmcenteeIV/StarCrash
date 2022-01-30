import pygame
from pygame.constants import K_LEFT, K_RIGHT, K_DOWN, K_UP


vec = pygame.math.Vector2

class Bullet(pygame.sprite.Sprite):

    def __init__(self, height, velocity, pos, enemy_bullet, image):
        super().__init__()
        self.height = height
        self.image = pygame.Surface((30, 30))
        self.image.fill((128,255,40))
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        # self.image = loader.load_image('assets/images/ejike.png')
        # self.rect = self.image.get_rect(center = (100, 420))

        self.pos = (pos)
        self.vel = vec(0, velocity)
        self.enemy_bullet = enemy_bullet

    def update(self):
        self.move()
    
    def move(self):
        if not self.enemy_bullet:
            self.pos -= self.vel
        else:
            self.pos += self.vel
        if self.pos.y < 0 - self.rect.height:
            self.kill()
        self.rect.midbottom = self.pos