import pygame
from pygame.constants import *
from time import sleep

from lib.explosion import *
from lib.transformflash import *
from lib import resources, bullet, uitext, uiverticalbar, hands

vec = pygame.math.Vector2

class Player(pygame.sprite.Sprite):

    def __init__(self, ship_image, powered_mech_image, mech_image, acceleration, friction):
        super().__init__()
         #References
        self.res = resources.Resources.instance()
        self.game = self.res.game

        #Sprite Properties
        self.images = [
            self.res.assets['images']['ship_red2'],
            self.res.assets['images']['ship_yellow2'],
            self.res.assets['images']['ship_orange2'],
        ]
        self.image = random.choice(self.images)
        self.ship_image = ship_image
        self.powered_mech_image = powered_mech_image
        self.mech_image = mech_image
        self.rect = self.image.get_rect()

        self.ui_power_count = uitext.UIText()  
        self.ui_power_count.get_data_callback = self.get_power_count

        self.ui_bar = uiverticalbar.UIVerticalBar()
        self.ui_bar.get_data_callback = self.get_power_count

        self.ui_lives_count = uitext.UIText()
        self.ui_lives_count.rect = pygame.Rect(64,600,1,1)
        self.ui_lives_count.get_data_callback = self.get_num_lives

        self.ui_gameover_label = uitext.UIText()
        self.ui_gameover_label.rect = pygame.Rect((self.game.width/2)-128,self.game.height/2,1,1)
        self.ui_gameover_label.get_data_callback = self.get_gameover_string


        #Motion Properties
        self.friction = friction
        self.acceleration = acceleration
        
        self.spawn_pos = vec((self.game.width/2, self.game.height))
        self.pos = self.spawn_pos
        self.rect.center = self.pos
        self.vel = vec(0,0)
        self.acc = vec(0,0)

        #State Properties
        self.game_over = False
        self.num_lives = 3
        self.ready_to_fire = True
        self.power_count = 3
        self.mode_state = 0
        self.next_mode_state = 0
        self.transform_ready= True

        #Kludgey timer. Pls implement a better timer soon!
        self.drain_tick_count = 30
        self.drain_tick_rate = 30 

         # Sound power up properties

        #self.sound1 = pygame.mixer.Sound("/home/jammer/git/upsidedown-postman/assets/sounds/explosions4.wav")
        self.sound1 = self.res.assets['sounds']['explosions4']
        self.sound2 = self.res.assets['sounds']['powerup']

        # setting sound volume to max (range 0.0 - 1.0) becasue other sounds drowned out the transformation
        # TODO (matthew.moroge) may have to adjust other sound volumes if this is doesn't work, need feedback from the team first
        self.sound1.set_volume(1)
        self.sound2.set_volume(1)

        self.hands = False

        self.update_hand_positions()

        self.res.music_hype = False
        self.res.song_change()
        
        
        
    def update(self):

        #Handle kludgey timer. Pls implement a better timer soon!
        do_drain = False
        self.drain_tick_count = self.drain_tick_count - 1
        if self.drain_tick_count <= 0:
            self.drain_tick_count = 30
            do_drain = True
            print(f"Rect: {self.rect.x} {self.rect.y}")
            print(f"Pos: {self.pos.x} {self.pos.y}")

        if self.power_count <= 0:
            self.explode()

        # Player mode state machine
        self.next_mode_state = self.mode_state

        if self.mode_state == 0:
            self.take_damage(False)
            if self.power_count > 20:
                self.next_mode_state = 1
                TransformFlash(self.pos)
                self.res.music_hype = True
                self.res.song_change()
                self.image = self.powered_mech_image
                # super duct tape for playing two sounds together in pygame
                self.sound1.play()
                #sleep(0.5)
                self.sound2.play()
                self.rect = self.image.get_rect()
                if not self.hands:
                    for left_side in [True, False]:
                        if left_side:
                            self.left_hand = hands.Hands( .95, self.position_for_left, left_side, self.res.assets["images"]["power_L_hand"], self.acceleration*.5, self.friction*.25)
                        else:
                            self.right_hand = hands.Hands( .95, self.position_for_right, left_side, self.res.assets["images"]["power_R_hand"], self.acceleration, self.friction*.25)
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
                TransformFlash(self.pos)
                self.image = self.ship_image
                self.rect = self.image.get_rect()
                self.left_hand.kill()
                self.right_hand.kill()
                self.res.music_hype = False
                self.res.song_change()
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
        if pressed_keys[K_g]:
            self.power_count = 2
            
    
    def move(self):
        self.acc = vec(0,0)

        self.update_hand_positions()
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

        if self.pos.y > self.game.height-(self.rect.height/2):
            self.pos.y, self.acc.y = self.game.height-(self.rect.height/2), 0
        if self.pos.y < (self.rect.height/2):
            self.pos.y, self.acc.y = (self.rect.height/2), 0

        self.rect.center= self.pos

        if self.hands:
            self.left_hand.player_pos = self.position_for_left
            self.right_hand.player_pos = self.position_for_right

    def player_fire(self):
        if self.hands:
            self.left_hand.sweeping_attack()
            self.right_hand.sweeping_attack()
        if self.mode_state == 0 or self.mode_state == 2:
            new_bullet = bullet.Bullet(6, self.rect.midtop, False, self.res.player_bullet)
            new_bullet.parent = self
            self.res.update_groups["player_bullet"].add(new_bullet)
            self.res.draw_groups["render"].add(new_bullet)
            self.res.assets['sounds']['laser1'].play()
        if self.mode_state == 1:
            new_bullet = bullet.Bullet(6, self.rect.midtop, False, self.res.player_bullet)
            new_bullet.image = self.res.assets['images']['_0020_nuke']
            new_bullet.parent = self
            self.res.update_groups["player_bullet"].add(new_bullet)
            self.res.draw_groups["render"].add(new_bullet)
            self.res.assets['sounds']['shots3'].play()
    
    def increment_power_count(self):
        self.power_count = self.power_count + 1

    def get_power_count(self):
        return self.power_count

    def explode(self):
        Explosion((self.rect.x, self.rect.y))
        self.do_respawn()

    def destroy(self):
        if self.hands:
            self.left_hand.kill()
            self.right_hand.kill()
        self.ui_power_count.destroy()
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
            
        enemy_hits = pygame.sprite.spritecollide(self, enemies, False)
        if enemy_hits:
            if not invulnerable:
                self.power_count = self.power_count - 1
            for enemy in enemy_hits:
                enemy.explode()
            
        return (bullet_hits, enemy_hits)

    def update_hand_positions(self):
        if self.hands:
            self.position_for_left = (vec(self.rect.midleft).x -50, vec(self.rect.midleft).y) 
            self.position_for_right =  (vec(self.rect.midright).x + 140, vec(self.rect.midright).y)
        else:
            self.position_for_left = self.rect.midright
            self.position_for_right =  self.rect.midright

    def get_num_lives(self):
        return self.num_lives

    def get_gameover_string(self):
        if self.game_over:
            return "Game Over"
        else:
            return ""

    def do_respawn(self):
        self.num_lives -= 1
        if self.num_lives == 0:
            self.power_count = 1
            self.kill()
            self.game_over = True
            self.ui_bar.destroy()
            self.ui_lives_count.destroy()
            self.ui_power_count.destroy()
        else:
            self.num_lives -= 1
            self.image = random.choice(self.images)
            self.rect = self.image.get_rect()
            self.mode_state = 0
            self.next_mode_state = 0
            self.power_count = 0
            self.ready_to_fire = True
            self.pos = self.spawn_pos