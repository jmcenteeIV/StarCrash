import pygame
from pygame.constants import *
from time import sleep

from lib import resources, bullet, uitext, uiverticalbar, hands

vec = pygame.math.Vector2

class Player(pygame.sprite.Sprite):

    def __init__(self, ship_image, powered_mech_image, mech_image, acceleration, friction):
        super().__init__()

        #Sprite Properties
        self.image = ship_image
        self.ship_image = ship_image
        self.powered_mech_image = powered_mech_image
        self.mech_image = mech_image
        self.rect = self.image.get_rect( center = (106, 100))

        #References
        self.res = resources.Resources.instance()
        self.game = self.res.game
        self.ui_text = uitext.UIText()  
        self.ui_text.get_data_callback = self.get_power_count
        self.ui_bar = uiverticalbar.UIVerticalBar()
        self.ui_bar.get_data_callback = self.get_power_count


        #Motion Properties
        self.friction = friction
        self.acceleration = acceleration
        
        self.pos = vec((self.game.width/2, self.game.height))
        self.vel = vec(0,0)
        self.acc = vec(0,0)

        #State Properties
        self.ready_to_fire = True
        self.power_count = 1
        self.mode_state = 0
        self.next_mode_state = 0

        #Kludgey timer. Pls implement a better timer soon!
        self.drain_tick_count = 30
        self.drain_tick_rate = 30

        # Sound power up properties
        self.sound1 = pygame.mixer.Sound("/home/jammer/git/upsidedown-postman/assets/sounds/explosions4.wav")
        self.sound2 = pygame.mixer.Sound("/home/jammer/git/upsidedown-postman/assets/sounds/powerup.wav")

        # setting sound volume to max (range 0.0 - 1.0) becasue other sounds drowned out the transformation
        # TODO (matthew.moroge) may have to adjust other sound volumes if this is doesn't work, need feedback from the team first
        self.sound1.set_volume(1.0)
        self.sound2.set_volume(1.0)

        self.hands = False
        
    def update(self):

        #Handle kludgey timer. Pls implement a better timer soon!
        do_drain = False
        self.drain_tick_count = self.drain_tick_count - 1
        if self.drain_tick_count <= 0:
            self.drain_tick_count = 30
            do_drain = True

        if self.power_count <= 0:
            self.destroy()

        # Player mode state machine
        self.next_mode_state = self.mode_state

        if self.mode_state == 0:
            self.take_damage(False)
            if self.power_count > 20:
                self.next_mode_state = 1
                self.image = self.powered_mech_image
                # super duct tape for playing two sounds together in pygame
                self.sound1.play()
                sleep(0.5)
                self.sound2.play()
                if not self.hands:
                    for left_side in [True, False]:
                        if left_side:
                            self.left_hand = hands.Hands( .95, self.rect.topleft, left_side, self.res.assets["images"]["power_L_hand"])
                        else:
                            self.right_hand = hands.Hands( .95, self.rect.topright, left_side, self.res.assets["images"]["power_R_hand"])
                    for hand in [self.left_hand, self.right_hand]:
                        self.res.update_groups["player"].add(hand)
                        self.res.draw_groups["render"].add(hand)
                    self.hands = True

        if self.mode_state == 1:
            self.take_damage(True)
            if do_drain:
                self.power_count = self.power_count -1
            if self.power_count < 11:
                self.next_mode_state = 2
                self.image = self.mech_image
                self.right_hand.image = self.res.assets["images"]["R_hand"]
                self.left_hand.image = self.res.assets["images"]["L_hand"]
                
        if self.mode_state == 2:
            self.take_damage(False)
            if self.power_count < 5:
                self.next_mode_state = 0
                self.image = self.ship_image
                self.left_hand.kill()
                self.right_hand.kill()
                self.hands = False

            if self.power_count > 20:
                self.next_mode_state = 1
                self.image = self.powered_mech_image
                self.right_hand.image = self.res.assets["images"]["power_R_hand"]
                self.left_hand.image = self.res.assets["images"]["power_L_hand"]

        if not self.mode_state == self.next_mode_state:
            print(f"Mode: {self.mode_state} -> {self.next_mode_state}")

        self.mode_state = self.next_mode_state

        #End state machine

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
            self.power_count = 25
    
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

        if self.hands:
            self.left_hand.move(self.rect.topleft)
            self.right_hand.move(self.rect.topright)

    def player_fire(self):
        if self.image == self.ship_image:
            new_bullet = bullet.Bullet(6, self.rect.midtop, False, self.res.player_bullet)
            new_bullet.parent = self
            self.res.update_groups["player_bullet"].add(new_bullet)
            self.res.draw_groups["render"].add(new_bullet)
            self.res.assets['sounds']['laser1'].play()
        if self.image == self.powered_mech_image:
            new_bullet = bullet.Bullet(6, self.rect.midtop, False, self.res.player_bullet)
            new_bullet.parent = self
            self.res.update_groups["player_bullet"].add(new_bullet)
            self.res.draw_groups["render"].add(new_bullet)
            self.res.assets['sounds']['shots3'].play()
    
    def increment_power_count(self):
        self.power_count = self.power_count + 1

    def get_power_count(self):
        return self.power_count

    def destroy(self):
        if self.hands:
            self.left_hand.kill()
            self.right_hand.kill()
        self.ui_text.destroy()
        self.ui_bar.destroy()
        self.kill()
        del(self)
        
    def take_damage(self, invulnerable):
        """
        Collision detection
        """
        
        enemy_bullets = self.res.update_groups['enemy_bullet']
        enemies = self.res.update_groups['enemy']
        

        """
        1st arg: name of sprite I want to check
        2nd arg: name of group I want to compare against
        3rd arg: True/False reference to dokill which either deletes the object in 1st arg or not
        """
        bullet_hits = pygame.sprite.spritecollide(self, enemy_bullets, True)
        if bullet_hits and not invulnerable:
            self.power_count = self.power_count - 1
            
        enemy_hits = pygame.sprite.spritecollide(self, enemies, True)
        if enemy_hits and not invulnerable:
            self.power_count = self.power_count - 1

        return (bullet_hits, enemy_hits)
