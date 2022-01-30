import pygame
from pygame.constants import *

from lib import resources, bullet, uitext

vec = pygame.math.Vector2

class Player(pygame.sprite.Sprite):

    def __init__(self, ship_image, powered_mech_image, mech_image, acceleration, friction):
        super().__init__()

        #Sprite Properties
        self.image = ship_image
        self.ship_image = ship_image
        self.powered_mech_image = powered_mech_image
        self.mech_image = mech_image
        self.rect = self.image.get_rect( center = (100, 420))

        #References
        self.res = resources.Resources.instance()
        self.game = self.res.game
        self.ui_text = uitext.UIText()  
        self.ui_text.get_data_callback = self.get_power_count

        #Motion Properties
        self.friction = friction
        self.acceleration = acceleration
        
        self.pos = vec((self.game.width/2, self.game.height))
        self.vel = vec(0,0)
        self.acc = vec(0,0)

        #State Properties
        self.ready_to_fire = True
        self.power_count = 0
        self.mode_state = 0
        self.next_mode_state = 0

        #Kludgey timer. Pls implement a better timer soon!
        self.drain_tick_count = 30
        self.drain_tick_rate = 30

        
    def update(self):

        #Handle kludgey timer. Pls implement a better timer soon!
        do_drain = False
        self.drain_tick_count = self.drain_tick_count - 1
        if(self.drain_tick_count <= 0):
            self.drain_tick_count = 30
            do_drain = True

        self.next_mode_state = self.mode_state

        if self.mode_state == 0:
            if self.power_count > 20:
                self.next_mode_state = 1
                self.image = self.powered_mech_image

        if self.mode_state == 1:
            if do_drain:
                self.power_count = self.power_count -1
            if self.power_count < 11:
                self.next_mode_state = 2
                self.image = self.mech_image
                
        if self.mode_state == 2:
            if self.power_count < 0:
                self.next_mode_state = 0
                self.image = self.ship_image

            if self.power_count > 20:
                self.next_mode_state = 1
                self.image = self.powered_mech_image

        if not self.mode_state == self.next_mode_state:
            print(f"Mode: {self.mode_state} -> {self.next_mode_state}")

        self.mode_state = self.next_mode_state

        self.move()

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_SPACE]:
            if self.ready_to_fire:
                self.ready_to_fire = False
                self.player_fire()
        if not pressed_keys[K_SPACE]:
            self.ready_to_fire = True
        # To test player mode state change. Remove after testing
        if pressed_keys[K_t]:
            self.power_count = -1
    
    def move(self):
        self.acc = vec(0,0)

        pressed_keys = pygame.key.get_pressed()
        #  Horizontal movement        
        if pressed_keys[K_LEFT]:
            self.acc.x = -self.acceleration
        if pressed_keys[K_RIGHT]:
            self.acc.x = self.acceleration

        self.acc.x += self.vel.x * self.friction
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > (self.game.width - (self.rect.width/2)):
            self.pos.x, self.acc.x = (self.game.width - (self.rect.width/2)), 0
        if self.pos.x < (self.rect.width/2):
            self.pos.x, self.acc.x = (self.rect.width/2) , 0

        #  Vertical movement
        if pressed_keys[K_DOWN]:
            self.acc.y = self.acceleration
        if pressed_keys[K_UP]:
            self.acc.y = -self.acceleration

        self.acc.y += self.vel.y * self.friction
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.y > self.game.height:
            self.pos.y, self.acc.y = self.game.height, 0
        if self.pos.y < self.rect.height:
            self.pos.y, self.acc.y = (0 + self.rect.height), 0

        self.rect.midbottom = self.pos

    def player_fire(self):
        new_bullet = bullet.Bullet(6, self.rect.midtop, self.res.bullet)
        new_bullet.parent = self
        self.res.update_groups["player_bullet"].add(new_bullet)
        self.res.draw_groups["render"].add(new_bullet)
        self.res.assets['sounds']['laser1'].play()
        self.increment_power_count()
    
    def increment_power_count(self):
        self.power_count = self.power_count + 1

    def get_power_count(self):
        return self.power_count
