import pygame
from pygame.constants import K_LEFT, K_RIGHT, K_DOWN, K_UP

vec = pygame.math.Vector2

class Player(pygame.sprite.Sprite):

    def __init__(self, image, height, width, acceleration, friction):
        super().__init__()
        self.friction = friction
        self.acceleration = acceleration
        self.width = width
        self.height = height
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((128,255,40))
        self.image = image
        self.rect = self.image.get_rect(center = (100, 420))

        self.pos = vec((width/2, height))
        self.vel = vec(0,0)
        self.acc = vec(0,0)

    # def draw(self, surface):
    #     surface.blit(self.image, self.rect)

    def update(self):
        self.move()
    
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

        if self.pos.x > (self.width - (self.rect.width/2)):
            self.pos.x, self.acc.x = (self.width - (self.rect.width/2)), 0
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

        if self.pos.y > self.height:
            self.pos.y, self.acc.y = self.height, 0
        if self.pos.y < self.rect.height:
            self.pos.y, self.acc.y = (0 + self.rect.height), 0

        self.rect.midbottom = self.pos