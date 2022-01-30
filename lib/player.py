import pygame
from pygame.constants import K_LEFT, K_RIGHT, K_DOWN, K_UP, K_SPACE

from lib import resources, bullet, uitext

vec = pygame.math.Vector2

class Player(pygame.sprite.Sprite):

    def __init__(self, ship_image, mech_image, acceleration, friction):
        super().__init__()

        #Sprite Properties
        self.image = ship_image
        self.ship_image = ship_image
        self.mech_image = mech_image
        self.rect = self.image.get_rect( center = (100, 420))

        #References
        self.res = resources.Resources.instance()
        self.game = self.res.game
        self.ui_text = uitext.UIText()  

        #Motion Properties
        self.friction = friction
        self.acceleration = acceleration
        
        self.pos = vec((self.game.width/2, self.game.height))
        self.vel = vec(0,0)
        self.acc = vec(0,0)

        #State Properties
        self.ready_to_fire = True
        self.kills = 0
        self.mode_state = 0
        self.next_mode_state = 0

    def update(self):

        self.next_mode_state = self.mode_state

        if self.mode_state == 0:
            if self.kills > 2:
                print("Leaving state 0")
                self.next_mode_state = 1
                self.image = self.mech_image
        if self.mode_state == 1:
            if self.kills < 1:
                print("Leaving state 1")
                self.image = self.ship_image
                self.next_mode_state = 0

        self.mode_state = self.next_mode_state

        self.move()

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_SPACE]:
            if self.ready_to_fire:
                self.ready_to_fire = False
                self.player_fire()
        if not pressed_keys[K_SPACE]:
            self.ready_to_fire = True
    
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
        new_bullet = bullet.Bullet(6, self.res.player.rect.midtop)
        new_bullet.parent = self
        resources.Resources.instance().update_groups["player_bullet"].add(new_bullet)
        resources.Resources.instance().draw_groups["render"].add(new_bullet)
        resources.Resources.instance().assets['sounds']['laser1'].play()
    
    def increment_kills(self):
        self.kills = self.kills + 1