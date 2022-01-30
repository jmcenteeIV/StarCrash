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

    def update(self):
        self.process_collisions()

    def process_collisions(self):
        """
        Collision detection
        """
        enemy_bullets = self.res.update_groups['enemy_bullet']
        enemies = self.res.update_groups['enemy']
        
        """
        1st arg: name of sprite I want to check
        2nd arg: name of group I want to compare against
        3rd arg: True/False reference to dokill which either deletes the object in 1st arg or not
        """
        bullet_hits = pygame.sprite.spritecollide(self, enemy_bullets, True)
            
        enemy_hits = pygame.sprite.spritecollide(self, enemies, False)
        if enemy_hits:
            for enemy in enemy_hits:
                enemy.explode()
            
        return (bullet_hits, enemy_hits)