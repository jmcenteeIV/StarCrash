import resources
import pygame
import lib


vec = pygame.math.Vector2

class Baddies(pygame.sprite.Sprite):
    """
    Currently repersents a single enemy
    """

    # TODO (matthew.moroge) will probably need to the class for the screen as a param and use super()
    def __init__(self, width, height, start_position, speed, aggression):
        super().__init__()
        """
        Initialize the alien and set its starting position
        """
        
        # load enemy image when we have it
        # self.image = loader.load_image('/path/to/file')
        # self.image.convert_alpha()
        # self.rect = self.enemy.image.get_rect()

        # creating basic rect for beginning, change to image later
        # gonna need to import the screen variable for the rect

        self.width = width
        self.height = height
        self.aggression = aggression
        self.image = pygame.Surface((50, 50))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect( center = (50,50))
        self.pos = vec(start_position)

        self.resources = resources.Resources.instance()
        
        
        

    def update(self):
        """
        Refreshing enemy on screen and catching events in real time
        """
        self.move()
        self.take_damage()



    def move(self):
        """
        moving the enemy
        """

        self.pos.x += self.speed

        if self.pos.x > (self.width - (self.rect.width/2)):
            self.pos.x, self.speed = (self.width - (self.rect.width/2)), self.speed * -1
        if self.pos.x < (self.rect.width/2):
            self.pos.x, self.speed = (self.rect.width/2) , self.speed * -1

        self.rect.midbottom = self.pos

    def take_damage(self, player_bullet, player):
        """
        
        """
        
        player_bullet = self.resources.update_groups['player_bullet']
        player = self.resources.update_groups['player']

        """
        1st arg: name of sprite I want to check
        2nd arg: name of group I want to compare against
        3rd arg: True/False reference to dokill which either deletes the object in 1st arg or not
        """
        hits = pygame.sprite.spritecollide(self, player_bullet, True)
    