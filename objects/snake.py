import pygame
import random
from objects.settings import *

class Snake:

    class Element:
        
        def __init__(self, x: int, y: int):
            self.x = x
            self.y = y

        def change_coord(self, x: int, y: int):
            self.x += x
            self.y += y

            if self.y < 0:
                self.y += DISPLAY_HEIGHT
            elif self.y > DISPLAY_HEIGHT:
                self.y -= DISPLAY_HEIGHT

            if self.x < 0:
                self.x += DISPLAY_WIDTH
            elif self.x > DISPLAY_WIDTH:
                self.x -= DISPLAY_WIDTH

        def get_all_coords(self):
            return {(x, y) for x in range(self.x, self.x+SIZE_SNAKE_ELEMENT) for y in range(self.y, self.y+SIZE_SNAKE_ELEMENT)}

    def __init__(self):
        self.elems = [self.Element(random.randrange(0, DISPLAY_WIDTH, STEP), random.randrange(0, DISPLAY_HEIGHT, STEP))]

    def move(self, x_change: int, y_change: int):
        old = [self.Element(self.elems[i].x, self.elems[i].y) for i in range(len(self.elems)-1)]
        head = self.elems[0] 
        head.change_coord(x_change, y_change)
        for i in range(1, len(self.elems)):
            elem = self.elems[i]
            elem.x = old[i-1].x
            elem.y = old[i-1].y

    def add_tail(self, direction):
        last_elem_index = len(self.elems)-1
        tail = self.elems[last_elem_index]
        x = tail.x 
        y = tail.y
        
        if direction == pygame.K_UP:
            y += SIZE_SNAKE_ELEMENT + STEP
        elif direction == pygame.K_DOWN:
            y -= STEP
        elif direction == pygame.K_LEFT:
            x += SIZE_SNAKE_ELEMENT + STEP
        elif direction == pygame.K_RIGHT:
            x -= STEP

        self.elems.append(self.Element(x, y))

    def eat_self(self):
        head = self.elems[0].get_all_coords()
        for i in range(3, len(self.elems)):
            tail = self.elems[i].get_all_coords()
            if len(head.intersection(tail)) > 0:
                return True
            
        return False

