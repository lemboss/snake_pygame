import pygame

class Input:
    def __init__(self):
        pass

    def init_input_text(self, basic_input="", x=0, y=0, color=(0,0,0,255)):
        self.font = pygame.font.Font(None, 32)
        self.input_text = basic_input
        self.input_text_pos = (x, y)
        self.input_text_color = color

    def change_input(self, type):
        if type == -1:
            self.input_text = self.input_text[:-1]
        else:
            self.input_text += type

    def draw_text(self, dis):
        input_dis = self.font.render(self.input_text, True, self.input_text_color)
        dis.blit(input_dis, self.input_text_pos)

    def init_textbox(self, x: int, y: int, width: int, height: int, color=(0,0,0,255)):
        self.input_box = pygame.Rect(x, y, width, height)
        self.input_box_color = pygame.Color(color[0], color[1], color[2], color[3])

    def draw_textbox(self, dis):
        pygame.draw.rect(dis, self.input_box_color, self.input_box,2)

    def is_empty(self):
        if len(self.input_text) > 0:
            return False
        else:
            return True
        
    def set_text(self, text: str):
        self.input_text = text

    