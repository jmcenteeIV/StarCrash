import random
import pygame

from lib.animatedeffect import *
from lib import resources

class Explosion(AnimatedEffect):

    def __init__(self, pos):
        self.res = resources.Resources.instance()
        explosion1 = self.res.assets['explosion1'].load_resource()
        explosion2 = self.res.assets['explosion2'].load_resource()
        explosion3 = self.res.assets['explosion3'].load_resource()
        super().__init__(pos, [explosion1, explosion2, explosion3], 10, 80)
        
        self.sounds = [
            'explosions1',
            'explosions2',
            'explosions3',
            'explosions4'
        ]
        for sound in self.sounds:
            vol = sound.get_volume()
            sound.set_volume(vol*1.1)

        sound = self.sounds[random.randint(0,len(self.sounds)-1)].load_resource()
        sound.play()
