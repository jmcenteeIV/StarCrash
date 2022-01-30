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
        self.bullet_number = random.randint(0,3)
        self.position_variance = 100
        self.assets = {
            'images': {},
            'sounds': {},
            'fonts': {},
        }

        for root, dirs, files in os.walk('assets'):
            for file in files:                          # e.g. assets/images/paperboy.jpg                            
                assetType = os.path.split(root)[1]      #      assets/images    ->  images
                assetName = os.path.splitext(file)[0]   #      paperboy.jpg     ->  paperboy
                assetPath = os.path.join(root, file)    #      assets/image, paperboy.jpg -> assets/images/paperboy.jpg
                print(f"Loading {assetType} {file} as {assetName}")
                asset = loader.load_asset(assetPath, assetType)
                self.assets[assetType][assetName] = asset

        # Manually load font

        self.assets['fonts']['default'] = pygame.freetype.Font(None)
        self.assets['fonts']['default'].size = 64
        self.assets['fonts']['default'].antialiased = False

    def load_objects(self, game):
        self.badies_range = [5, 8]
        self.game = game
        self.position_variance = 100

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
            "player": pygame.sprite.Group(),
            "game": pygame.sprite.Group()
        }

        # The background is now another sprite. This code is a bit cumbersome, but this allows the bg to be altered
        self.background_sprite = pygame.sprite.Sprite(self.draw_groups['background'])
        self.background_sprite.image = self.assets['images']['notspaceart']
        self.background_sprite.rect = pygame.Rect(0,0,1,1)

        # Sprite for UI
        self.ui_sprite = pygame.sprite.Sprite(self.draw_groups['ui'])
        self.ui_sprite.image = pygame.Surface((256,64))
        self.ui_sprite.rect = pygame.Rect(64,64,1,1)
        self.ui_sprite.image.set_colorkey(pygame.Color(0,255,0))
        self.ui_sprite.image.fill(pygame.Color(0,255,0))
    
        self.load_badies()

        # Player
        ship_choices = []
        for choice in ['ship_orange2', 'ship_red2', 'ship_yellow2']:
            ship_choices.append(self.assets['images'][choice])
        self.player = player.Player(random.choices(ship_choices)[0], self.assets['images']['power_mech'], self.assets['images']['_0000_mech'], .4, -.12 )
        self.update_groups["player"].add(self.player)
        self.draw_groups["render"].add(self.player)

        self.player_bullet_pool = []
        for bullet in ['_0011_bullet_green', '_0012_bullet_yellow', '_0013_bullet_pink', '_0017_bullet' ]:
            self.player_bullet_pool.append(self.assets['images'][bullet])
        self.player_bullet = self.player_bullet_pool[self.bullet_number]

        self.enemy_bullet_pool = []
        for bullet in ['_0008_droplet', 'spikeball', '_0007_missile', '_0005_thorn1', '_0006_thorn2' ]:
            self.enemy_bullet_pool.append(self.assets['images'][bullet])
        
        

    def load_badies(self):
        enemies = len(self.update_groups["enemy"])
        if  enemies < self.badies_range[0]:
            for x in range(random.randint((self.badies_range[0] - enemies), (self.badies_range[1] - enemies))):
                baddies_choices = []
                for choice in ['eyeball', 'maw', 'thorny']:
                    baddies_choices.append(self.assets['images'][choice])
                enemy = baddies.Baddies(random.choices(baddies_choices)[0], self.game.height, self.game.width, 5)
                self.update_groups["enemy"].add(enemy)
                self.draw_groups["render"].add(enemy)
                self.position_variance += 75

    def sound_picker(self):
        """
        dict of sounds to load 
        """
        pass
