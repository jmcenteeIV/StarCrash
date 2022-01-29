import sys
import pygame
from pygame.locals import *

from lib import loader, player, bullet

class Game(object):

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
        pygame.mixer.init()
        
        self.fps = 60
        self.fpsClock = pygame.time.Clock()
        
        self.width, self.height = 1360, 720
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background_image = loader.load_asset("assets/images/notspaceart.png")
        self.laser_sound = loader.load_asset("assets/sounds/laser1.wav", 'sound')

        # Game state setup

        self.sprite_groups = {
            "render": pygame.sprite.Group(),
            "update" : {
                "background": pygame.sprite.Group(),
                "ui": pygame.sprite.Group(),
                "enemy": pygame.sprite.Group(),
                "enemy_bullet": pygame.sprite.Group(),
                "player_bullet":pygame.sprite.Group(),
                "player": pygame.sprite.Group()
            }
        }
        self.player = player.Player(self.height, self.width, .25, -.12 )
        self.sprite_groups["update"]["player"].add(self.player)
        self.sprite_groups["render"].add(self.player)

        

    def loop(self):
        self.process_events()
        self.update_sprites()
        self.draw()        
        self.fpsClock.tick(self.fps)
        
        
    def update_sprites(self):
        for group in self.sprite_groups["update"]:
            self.sprite_groups["update"][group].update()

    def process_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.mixer.quit()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player_fire()

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background_image, [0, 0])
        self.sprite_groups['render'].draw(self.screen)
        pygame.display.flip()

    def player_fire(self):
        self.bullet = bullet.Bullet(self.height, 6, self.player.rect.midtop)
        self.sprite_groups["update"]["player_bullet"].add(self.bullet)
        self.sprite_groups["render"].add(self.bullet)
        self.laser_sound.play()