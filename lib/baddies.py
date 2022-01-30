from lib import resources, loader, game, bullet
from lib.explosion import *
import pygame.math as math
import random as randy
import pygame




vec = pygame.math.Vector2

class Baddies(pygame.sprite.Sprite):
    """
    Currently repersents a single enemy
    """

    
    def __init__(self, image, height, width, aggression):
        super().__init__()
        """
        Initialize the alien and set its starting position
        """

        # basics needed for enemy
        self.width = width
        self.height = height
        self.aggression = aggression
        self.image = image
        self.image.convert_alpha()
        self.rect = self.image.get_rect( center = (75,75))
        self.res = resources.Resources.instance()


        # explosion animation?
        self.anime_count = 0
        self.anime_frames = 3
        self.anime = False

        # for bullet type
        self.bullet_number = randy.randint(0, 4)

        
        """
        adding movement options for random movements
        """

        # storing a copy of the image to try out rotation 
        self.rotate_img = self.image.copy()
        # random vector for enemy 
        self.direction = pygame.Vector2(randy.uniform(0, 50), randy.uniform(0, 50))
        while self.direction.length() == 0:
            self.direction = pygame.Vector2(randy.uniform(1, 4), randy.uniform(1, 4))

        # constant random speed for enemy
        self.direction.normalize_ip()
        self.speed = randy.uniform(0.3, 3)

        # storing the position in a vector, because math is hard
        self.pos = pygame.Vector2((randy.randint(self.rect.x,width-self.rect.x),randy.randint(self.rect.y,100)))

        # let's play around with some rotation to make it look cool 
        #self.rotation = randy.uniform(0.3, 1)
        #self.angle = 0

        

    def update(self):
        """
        Refreshing enemy on screen and catching events in real time
        """
        self.move()
        self.take_damage()        
        self.shoot()


    def enemy_fire(self, pos, bullet_number):
        new_bullet = bullet.Bullet(6, pos, True, self.res.enemy_bullet_pool[bullet_number])
        self.res.update_groups["enemy_bullet"].add(new_bullet)
        self.res.draw_groups["render"].add(new_bullet)
        self.res.assets['sounds']['laser1'].play()


    def move(self):
        """
        moving the enemy
        """

        self.pos += self.direction * self.speed 

        # used for rotating enemy, may use later
        # self.angle += self.rotation 
        # self.image = pygame.transform.rotate(self.rotate_img, self.angle)

        self.rect = self.image.get_rect(center=self.pos)

        if self.rect.x > self.width or self.rect.x < 0:
            self.kill()
        if self.rect.y > self.height or self.rect.y < 0:
            self.kill()

        
    def take_damage(self):
        """
        Collision detection
        """
        
        player_bullet = self.res.update_groups['player_bullet']
        player = self.res.update_groups['player']
        

        """
        1st arg: name of sprite I want to check
        2nd arg: name of group I want to compare against
        3rd arg: True/False reference to dokill which either deletes the object in 1st arg or not
        """
        bullet_hit = pygame.sprite.spritecollide(self, player_bullet, True)
        if bullet_hit:
            bullet_hit[0].parent.increment_power_count()
            self.explode()

        return bullet_hit


    def shoot(self):
        if randy.randrange(0, 400) == 69:
            self.enemy_fire(self.rect.midbottom, self.bullet_number)

    def explode(self):
        Explosion( (self.rect.x, self.rect.y) )
        self.destroy()

    def destroy(self):
        self.kill()
        del(self)
