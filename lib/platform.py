from typing import Tuple
import pygame
import random


class Platform(pygame.sprite.Sprite):
    def __init__(self, height: float, width: float, position: Tuple[float, float]):
        super().__init__()
        self.surf = pygame.Surface((width, height))
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect(center=(position))

    def draw(self, surface):
        pass
    
    def move(self):
        pass