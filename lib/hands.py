from random import random
import pygame
from pygame.constants import K_LEFT, K_RIGHT, K_DOWN, K_UP

from lib import resources

vec = pygame.math.Vector2

class Hands(pygame.sprite.Sprite):

    def __init__(self, velocity, pos, left, image, acceleration, friction):
        super().__init__()
        #Sprite Properties
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.attacking = False
        self.attacked = False

        #References
        self.res = resources.Resources.instance()
        self.game = self.res.game
        self.left = left
        self.player_pos = pos
        #Motion Properties
        self.pos = (pos)
        self.acceleration = acceleration
        self.friction = friction

        self.vel = vec(0,0)
        self.acc = vec(0,0)
        
        

    def update(self):
        self.move()
        self.process_collisions()

    def move(self):
        if not self.attacking:
            if vec(self.pos).x > vec(self.player_pos).x:
                self.acc.x = -self.acceleration*random()
            if vec(self.pos).x < vec(self.player_pos).x:
                self.acc.x = self.acceleration*random()
            if vec(self.pos).x == vec(self.player_pos).x:
                self.acc.x = 0
            self.acc.x += self.vel.x * self.friction
            self.vel += self.acc
            self.pos += self.vel + 0.5 * self.acc

            if vec(self.pos).y > vec(self.player_pos).y:
                self.acc.y = -self.acceleration*random()
            
            if vec(self.pos).y < vec(self.player_pos).y:
                if vec(self.pos).y < vec(self.player_pos).y - 400:
                    self.acc.y = 3
                else: 
                    self.acc.y = self.acceleration*random()
            if vec(self.pos).y == vec(self.player_pos).y:
                self.acc.y = 0
            self.acc.y += self.vel.y * self.friction
            self.vel += self.acc
            self.pos += self.vel + 0.5 * self.acc
            

        else:
            self.acc.y = -10
            self.acc.y += self.vel.y * self.friction
            self.vel += self.acc
            self.pos += self.vel + 0.5 * self.acc

            if self.left:
                self.acc.x = 3
            else:
                self.acc.x = -3
            self.acc.x += self.vel.x * self.friction
            self.vel += self.acc
            self.pos += self.vel + 0.5 * self.acc
            # for position in pos_list:
            #     for _ in range(20):
            #         self.pos = (vec(self.player_pos).x+vec(position).x/20,vec(self.player_pos).y+vec(position).y/20)
                    
            self.attacking = False
        
        self.rect.bottomright = self.pos

    def sweeping_attack(self):
        self.attacking = True
        

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
