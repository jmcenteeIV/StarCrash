import random
import pygame

from lib import resources

class Explosion(pygame.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()
        self.res = resources.Resources.instance()
        self.images = [
            self.res.assets['images']['explosion1'],
            self.res.assets['images']['explosion2'],
            self.res.assets['images']['explosion3'],
        ]
        self.sounds = [
            self.res.assets['sounds']['explosions1'],
            self.res.assets['sounds']['explosions2'],
            self.res.assets['sounds']['explosions3'],
        ]
        self.current_frame = 0
        self.image = self.images[self.current_frame]
        self.rect = pygame.Rect(pos[0], pos[1], 1, 1)

        self.res.update_groups["game"].add(self)
        self.res.draw_groups["render"].add(self)

        self.time_count = 0         # Keeps track of game ticks since spawn
        self.animation_rate = 10    # Update the animation frame every x ticks
        self.life_end = 60         # Destroy this sprite when the time is up

        self.sounds[random.randint(0,len(self.sounds)-1)].play()

    def update(self):
        self.time_count = self.time_count + 1

        if self.time_count % self.animation_rate == self.animation_rate -1:
            self.current_frame = self.current_frame + 1
            if self.current_frame >= len(self.sounds):
                self.current_frame = 0

        self.image = self.images[self.current_frame]

        if self.time_count >= self.life_end:
            self.destroy()

    def destroy(self):
        self.kill()
        del(self)