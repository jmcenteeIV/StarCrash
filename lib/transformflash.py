import random
import pygame

from lib.animatedeffect import *
from lib import resources

class TransformFlash(AnimatedEffect):

    def __init__(self, pos):
        self.res = resources.Resources.instance()
        animation_name = 'flash'
        self.animation_frame_count = 8
        self.images = []
        animation_rate = 1
        lifetime = 0        # Effect destroyed on animation end
        mode = 1            # PingPong playback: goes to end and reverses

        for i in range(0,self.animation_frame_count):
            self.images.append(self.res.assets['images'][f"{animation_name}{i}"])
        super().__init__(pos, self.images, animation_rate, lifetime, mode)
        
        self.sound = self.res.assets['sounds']['powerup']
        #self.sound.play()

        #self.finished_callback = lambda *_, **__: None # Callback function to let Player know transformation is finished

    def update(self):
        #if self.current_frame == self.animation_frame_count -1:
        #    self.finished_callback()
        super().update()