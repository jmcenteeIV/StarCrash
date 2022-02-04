import pygame

from lib import resources

class UIVerticalBar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.background_color = pygame.Color(0,0,0)
        self.foreground_color = pygame.Color(0,255,0)
        self.height = 256
        self.width = 32
        self.border_size = 4
        self.x = 32
        self.y = 32
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        self.image = pygame.Surface( (self.width, self.height) )
        self.image.set_alpha(128)

        self.min_color = pygame.Color('red4')
        self.max_color = pygame.Color('green')
        
        self.max_value = 30
        self.min_value = 0
        self.value = 0
        self.get_data_callback = None
        
        self.test_count = 0

        resources.Resources.instance().update_groups["game"].add(self)
        resources.Resources.instance().draw_groups["ui"].add(self)

    def update(self):
        self.value = self.get_data_callback()
        self.render(self.calc_fill())
        
    def calc_fill(self):
        if(self.value > self.max_value):
            foreground_ratio = 1
        elif(self.value < self.min_value):
            foreground_ratio = 0
        else:
            foreground_ratio = self.value / (self.max_value - self.min_value)
        self.foreground_color = self.min_color.lerp(self.max_color, foreground_ratio)
        foreground_height = int(foreground_ratio * self.height) 
        foreground_top = self.height - foreground_height
        return pygame.Rect(0, foreground_top, self.rect.width, foreground_height)

    def render(self, foreground_rect):
        self.image.fill(self.background_color)
        pygame.draw.rect(self.image, self.foreground_color, foreground_rect)

    def destroy(self):
        self.kill()
        del(self)        