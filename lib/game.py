import sys
import pygame, pygame.freetype
from pygame.locals import *

from lib import bullet, resources

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
        # Per docs, we should be checking that these modules exist before attempting to init them
        pygame.mixer.init()
        
        self.fps = 60
        self.fps_clock = pygame.time.Clock()
        
        self.width, self.height = 1360, 720
        self.screen = pygame.display.set_mode((self.width, self.height))

        resources.Resources.instance().load_assets()
        resources.Resources.instance().load_objects(self)

    # High-level game loop
    def loop(self):
        self.process_events()
        self.update_sprites()
        self.draw()        
        self.fps_clock.tick(self.fps)
        
        
    # Update Sprite state
    def update_sprites(self):
        update_groups = resources.Resources.instance().update_groups
        for group in update_groups:
            update_groups[group].update()
        resources.Resources.instance().load_badies()


    def process_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.mixer.quit()
                pygame.quit()
                sys.exit()

    def draw(self):
        self.screen.fill((0, 0, 0))
        # Rod: I thought I read something about dicts not gauranteeing a consistent access order.
        #      this could cause issues if e.g. the render group is drawn before the background.
        #      Perhaps that's for older Python tho and maybe we're fine?
        draw_groups = resources.Resources.instance().draw_groups
        for group in draw_groups:
            draw_groups[group].draw(self.screen)
        pygame.display.flip()
