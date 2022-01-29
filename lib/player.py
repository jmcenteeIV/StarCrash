import pygame
from pygame.constants import K_LEFT, K_RIGHT, K_DOWN, K_UP
from lib import loader

vec = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self, height: float, width: float, friction, acceleration):
        super().__init__()
        self.accuracy = acceleration
        self.friction = friction
        self.width = width
        self.height = height
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((128,255,40))
        self.image = loader.load_image('assets/images/ejike.png')
        self.rect = self.image.get_rect(center = (100, 420))

        self.pos = vec((width/2, height))
        self.vel = vec(0,0)
        self.acc = vec(0,0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
    
    def move(self):
        self.acc = vec(0,0)
    
        pressed_keys = pygame.key.get_pressed()
        #  Horizontal movement        
        if pressed_keys[K_LEFT]:
            self.acc.x = -self.accuracy
        if pressed_keys[K_RIGHT]:
            self.acc.x = self.accuracy

        self.acc.x += self.vel.x * self.friction
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > self.width:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = self.width

        #  Vertical movement
        if pressed_keys[K_DOWN]:
            self.acc.y = self.accuracy
        if pressed_keys[K_UP]:
            self.acc.y = -self.accuracy

        self.acc.y += self.vel.y * self.friction
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.y > self.height:
            self.pos.y, self.acc.y = self.height, 0
        if self.pos.y < self.rect.height:
            self.pos.y, self.acc.y = (0 + self.rect.height), 0

        self.rect.midbottom = self.pos