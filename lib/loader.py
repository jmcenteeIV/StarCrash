import os
import sys
import pygame

import lib.utility as util

# deprecate?
def load_image(image_path: str):
    image = util.create_resource_path(image_path)
    return pygame.image.load(image).convert()

def load_asset(asset_path: str, asset_type: str = 'image'):
    resource_path = util.create_resource_path(asset_path)

    if asset_type == 'image':
        return pygame.image.load(resource_path).convert()
    elif asset_type == 'sound':
        return pygame.mixer.Sound(resource_path)
    else:
        raise TypeError("Asset Type not supported!")