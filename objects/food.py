import pygame
import random
from objects.settings import DISPLAY_WIDTH
from objects.settings import DISPLAY_HEIGHT
from objects.settings import SIZE_FOOD

class Food:
    
    def __init__(self):
        self.set_new_coords()

    def set_new_coords(self):
        self.x = random.randrange(0, DISPLAY_WIDTH, 10)
        self.y = random.randrange(0, DISPLAY_HEIGHT, 10)

    def get_all_coords(self):
        return {(x, y) for x in range(self.x, self.x+SIZE_FOOD) for y in range(self.y, self.y+SIZE_FOOD)}