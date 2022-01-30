from lib import resources
import pygame 

vec = pygame.math.Vector2


class Boom(pygame.sprite.Sprite):
    """
    adding explosions with some sound 
    """
    
    def __init__(self):
        super().__init__()
        """
        start them booms! 
        """
        # reference to game assests
        self.res = resources.Resources.instance()
        
        self.explodey_imgs = [pygame.image.load(f'/home/jammer/git/upsidedown-postman/assets/sounds/explosions{x}.wav') for x in range(1,4)]

    def update(self):
        """
        keeping up with real time 
        """
        now = pygame.time.get_ticks()
        # keeping up with the game in real time to match explosion animation 
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            # checking if all 3 images play than kill Baddie
            if self.frame == 3:
                self.kill()
