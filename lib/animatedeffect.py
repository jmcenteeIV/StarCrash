import random
import pygame

from lib import resources

vec = pygame.math.Vector2

class AnimatedEffect(pygame.sprite.Sprite):

    def __init__(self, pos: vec, images, animation_rate: int=10, lifetime: int=0, playback_mode: int=0, parent=None):
        super().__init__()
        self.pos = pos
        self.res = resources.Resources.instance()
        self.images = images
        self.current_frame = 0
        self.image = self.images[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.parent = parent

        self.res.update_groups["game"].add(self)
        self.res.draw_groups["render"].add(self)

        self.time_count = 0                     # Keeps track of game ticks since spawn
        self.animation_rate = animation_rate    # Update the animation frame every x ticks
        self.lifetime = lifetime                # Destroy this sprite when the time is up (when animation ends when set to 0)
        self.playback_mode = playback_mode      # 0: Looping, 1: PingPong
        self.animation_direction = 1            # Used by playback_mode
        self.animation_ended = False            # True when animation ends

    def update(self):
        self.rect.center = self.pos
        if self.parent:
            self.pos = self.parent.pos

        self.time_count = self.time_count + 1

        if self.time_count % self.animation_rate == self.animation_rate -1:
            self.current_frame = self.current_frame + self.animation_direction
            if self.current_frame >= len(self.images):
                if self.playback_mode == 0:
                    self.current_frame = 0
                    self.animation_ended = True
                if self.playback_mode == 1:
                    self.animation_direction = -1
                    self.current_frame = len(self.images) - 1
            if self.current_frame < 0:
                self.animation_direction = 1
                self.current_frame = 0
                self.animation_ended = True

        self.image = self.images[self.current_frame]

        if self.lifetime == 0:
            if self.animation_ended:
                self.destroy()
        elif self.time_count >= self.lifetime:
            self.destroy()

    def destroy(self):
        self.kill()
        del(self)