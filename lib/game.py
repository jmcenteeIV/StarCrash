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

    # Init pygame and modules, setup screen, load assets
    def start_game(self):
        
        pygame.init()
        pygame.mixer.init()
        
        self.fps = 60
        self.fps_clock = pygame.time.Clock()
        
        self.width, self.height = 1360, 720
        self.screen = pygame.display.set_mode((self.width, self.height))
        
        self.load_assets()


    # Load and store assets in a centralized location. For now this is where we spawn our initial game objects too.
    def load_assets(self):
        self.background_image = loader.load_asset("assets/images/notspaceart.png")
        self.laser_sound = loader.load_asset("assets/sounds/laser1.wav", 'sound')

        # These groups are meant to be used only for drawing sprites
        self.draw_groups = {
            "background": pygame.sprite.Group(),
            "render": pygame.sprite.Group(),
            "ui": pygame.sprite.Group(),
        }

        # These groups are meant to be used only for updating state (logic, state, etc)
        self.update_groups = {
            "enemy": pygame.sprite.Group(),
            "enemy_bullet": pygame.sprite.Group(),
            "player_bullet":pygame.sprite.Group(),
            "player": pygame.sprite.Group()
        }

        # The background is now another sprite. This code is a bit cumbersome, but this allows the bg to be altered
        self.background_sprite = pygame.sprite.Sprite(self.draw_groups['background'])
        self.background_sprite.image = self.background_image
        self.background_sprite.rect = pygame.Rect(0,0,1,1)

        self.player = player.Player(self.height, self.width, .25, -.12 )
        self.update_groups["player"].add(self.player)
        self.draw_groups["render"].add(self.player)
        

    # High-level game loop
    def loop(self):
        self.process_events()
        self.update_sprites()
        self.draw()        
        self.fps_clock.tick(self.fps)
        
        
    # Update Sprite state
    def update_sprites(self):
        for group in self.update_groups:
            self.update_groups[group].update()

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
        # Rod: I thought I read something about dicts not gauranteeing a consistent access order.
        #      this could cause issues if e.g. the render group is drawn before the background.
        #      Perhaps that's for older Python tho and maybe we're fine?
        for group in self.draw_groups:
            self.draw_groups[group].draw(self.screen)
        pygame.display.flip()


    def player_fire(self):
        self.bullet = bullet.Bullet(self.height, 6, self.player.rect.midtop)
        self.update_groups["player_bullet"].add(self.bullet)
        self.draw_groups["render"].add(self.bullet)
        self.laser_sound.play()