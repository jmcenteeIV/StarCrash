import random
import pygame

from lib.animatedeffect import *
from lib import resources

class Explosion(AnimatedEffect):

    def __init__(self, pos):
        self.res = resources.Resources.instance()
        self.images = [
            self.res.assets['images']['explosion1'],
            self.res.assets['images']['explosion2'],
            self.res.assets['images']['explosion3'],
        ]
        super().__init__(pos, self.images, 10, 80)
        
        self.sounds = [
            self.res.assets['sounds']['explosions1'],
            self.res.assets['sounds']['explosions2'],
            self.res.assets['sounds']['explosions3'],
            self.res.assets['sounds']['explosions4'],
        ]
        for sound in self.sounds:
            vol = sound.get_volume()
            sound.set_volume(vol*1.2)

        self.sounds[random.randint(0,len(self.sounds)-1)].play()
