import os
import sys
import pygame

import lib.utility as util

# deprecate?
def load_image(image_path: str):
    image = util.create_resource_path(image_path)
    return pygame.image.load(image).convert()

def load_asset(asset_path: str, asset_type: str = 'image', volume=.5):
    resource_path = util.create_resource_path(asset_path)

    if asset_type == 'image' or asset_type == 'images':
        return pygame.image.load(resource_path).convert_alpha()
    elif asset_type == 'sound' or asset_type == 'sounds':
        sound = pygame.mixer.Sound(resource_path)
        if volume:
            vol=sound.get_volume()
            sound.set_volume(vol*volume)
        return sound
    else:
        raise TypeError("Asset Type not supported!")