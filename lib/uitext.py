import pygame

from lib import resources

class UIText(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(64,400,1,1)
        self.text = 0

        resources.Resources.instance().update_groups["game"].add(self)
        resources.Resources.instance().draw_groups["ui"].add(self)

    def update(self):
        (image, rect) = resources.Resources.instance().assets['fonts']['default'].render(str(self.text))
        self.image = image
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_q]:
            self.text = self.text + 1
