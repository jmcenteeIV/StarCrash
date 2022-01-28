import os
import sys
import pygame

import lib.utility as util

def load_image(image_path):
    image = util.create_resource_path(image_path)
    return pygame.image.load(image).convert()

