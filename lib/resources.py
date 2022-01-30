import os
import pygame
import random
from lib import loader

from lib import player, bullet, baddies

class Resources():
    
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

    # Load and store assets in a centralized location. 
    # For now this is also where we spawn our initial game objects.
    def load_assets(self):
        self.assets = {
            'images': {},
            'sounds': {},
        }

        for root, dirs, files in os.walk('assets'):
            for file in files:                          # e.g. assets/images/paperboy.jpg                            
                assetType = os.path.split(root)[1]      #      assets/images    ->  images
                assetName = os.path.splitext(file)[0]   #      paperboy.jpg     ->  paperboy
                assetPath = os.path.join(root, file)    #      assets/image, paperboy.jpg -> assets/images/paperboy.jpg
                print(f"Loading {assetType} {file} as {assetName}")
                asset = loader.load_asset(assetPath, assetType)
                self.assets[assetType][assetName] = asset

    def load_objects(self, game):
        self.game = game

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
        self.background_sprite.image = self.assets['images']['notspaceart']
        self.background_sprite.rect = pygame.Rect(0,0,1,1)

        # self.enemies = []
        # for x in range(random.randint(4,5)):
        baddies_choices = []
           
        for choice in ['eyeball', 'maw', 'thorny']:
            baddies_choices.append(self.assets['images'][choice])
        self.enemy = baddies.Baddies(random.choices(baddies_choices)[0], self.game.height, self.game.width, (self.game.width/2, 60), 2, 5)
        self.update_groups["enemy"].add(self.enemy)
        self.draw_groups["render"].add(self.enemy)

        ship_choices = []
        for choice in ['ship_orange2', 'ship_red2', 'ship_yellow2']:
            ship_choices.append(self.assets['images'][choice])
        self.player = player.Player(random.choices(ship_choices)[0], self.game.height, self.game.width, .25, -.12 )
        self.update_groups["player"].add(self.player)
        self.draw_groups["render"].add(self.player)

        self.player_bullet_pool = []
        