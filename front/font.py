import os
import pygame


class Font:
    def __init__(self):
        self.root = os.path.join('.', 'src', 'fonts')

    def get(self, file):
        return os.path.join(self.root, file)
