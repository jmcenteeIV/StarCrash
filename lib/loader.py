import os
import sys
import pygame

# deprecate?
def load_image(image_path: str):
    image = util.create_resource_path(image_path)
    return pygame.image.load(image).convert()

def load_asset(asset_path: str, asset_type: str = 'image', volume=None):

    if asset_type == 'image' or asset_type == 'images':
        return pygame.image.load(asset_path).convert_alpha()
    elif asset_type == 'sound' or asset_type == 'sounds':
        return pygame.mixer.Sound(asset_path)
    else:
        raise TypeError("Asset Type not supported!")