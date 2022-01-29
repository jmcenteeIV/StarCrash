import sys
import pygame
from pygame.locals import *

from lib import loader

class Game():

    # Singleton instantiation and getting, code from: 
    # https://python-patterns.guide/gang-of-four/singleton/
    _instance = None

    def __init__(self):
        raise RuntimeError('Game has already been instantiated')

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
        return cls._instance
    # End Singleton code


    def start_game(self):
        # Pygame, Pygame Module, and Screen setup
        pygame.init()
        
        self.fps = 60
        self.fpsClock = pygame.time.Clock()
        
        self.width, self.height = 640, 480
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background_image = loader.load_image("assets/images/paperboy.jpg")

        # Game state setup

        self.sprite_groups = {
            "render": pygame.sprite.Group(),
            "background": pygame.sprite.Group(),
            "ui": pygame.sprite.Group(),
            "enemy": pygame.sprite.Group(),
            "enemy_bullet": pygame.sprite.Group(),
            "player_bullet":pygame.sprite.Group(),
            "player": pygame.sprite.Group(),
        }


    def loop(self):
        self.process_events()
        self.update_sprites()
        self.draw()        
        self.fpsClock.tick(self.fps)
        
        
    def update_sprites(self):
        pass

    def process_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background_image, [0, 0])
        self.sprite_groups['render'].draw(self.screen)
        pygame.display.flip()