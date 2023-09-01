class Text:
    def __init__(self, text = "", x=0, y=0, color=(0,0,0,255)):
        self.x = x
        self.y = y
        self.text = text
        self.color = color

    def draw(self, font, dis):
        surf = font.render(self.text, True, self.color)
        rect = surf.get_rect(topleft = (self.x, self.y))
        dis.blit(surf, rect)
