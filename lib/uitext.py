import pygame

from lib import resources

class UIText(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(64,400,1,1)
        self.text = 0
        self.get_data_callback = None

        resources.Resources.instance().update_groups["game"].add(self)
        resources.Resources.instance().draw_groups["ui"].add(self)

    def update(self):
        self.text = str(self.get_data_callback())
        (image, rect) = resources.Resources.instance().assets['fonts']['default'].render(str(self.text))
        self.image = image

    def destroy(self):
        self.kill()
        del(self)