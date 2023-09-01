import pygame
from objects.settings import *
from objects.snake import Snake
from objects.food import Food
from objects.button import Button
from objects.input import Input
from objects.text import Text
from objects.db_con import DBConnector

class Game:

    def __init__(self):
        pygame.init()
        self.font = pygame.font.Font(None, 30)
        self.dis = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        pygame.display.set_caption("Snake (Лемба Владимир, Бутово)")
        self.white = (255, 255, 255)
        self.blue = (0, 0, 255)
        self.red = (255, 0, 0)
        self.x_change = 0
        self.y_change = -STEP
        self.direction = pygame.K_UP
        
        self.clock = pygame.time.Clock()
        self.input = Input()
        self.input.init_textbox(195, 245, 400, 30, (0, 0, 0, 255))
        img_play = pygame.image.load("objects/pics/814097.png").convert_alpha()
        self.button_play = Button(350, 300, img_play, 0.2)

        self.text_name = Text("Введите ваше имя:", 300, 200)
        self.text_guide = Text(f"Чтобы выиграть, наберите не менее {POINTS_WIN} очков!", 180, 450)
        img_guide = pygame.image.load("objects/pics/keywords.png").convert_alpha()
        self.img_guide = Button(680, 0, img_guide, 0.1)

        img_arrow = pygame.image.load("objects/pics/arrow.png").convert_alpha()
        self.img_arrow = Button(150, 260, img_arrow, 0.3)
        img_close = pygame.image.load("objects/pics/x.png").convert_alpha()
        self.img_close = Button(500, 260, img_close, 0.3)
        self.back_menu = Text("Вернуться в меню", 150, 420)
        self.close_game = Text("Закрыть игру", 500, 420)

        self.db = DBConnector("objects/score.db")

    
    def _msg(self, text, x: int, y: int):
        debug_surf = self.font.render(str(text), True, "Black")
        debug_rect = debug_surf.get_rect(topleft = (x, y))
        self.dis.blit(debug_surf, debug_rect)
        
    def _menu(self):
        self.input.init_input_text("Имя", 200, 250)
        self.score = Text("Лучшие результаты:", 10, 10)
        self.leaders = self.db.get_leaders("score")
        settings = False
        while not settings:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.db.close_connection()
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.input.change_input(-1)
                    elif event.key != pygame.K_RETURN:
                        self.input.change_input(event.unicode)

                    if event.key == pygame.K_RETURN:
                        settings = True

            self.dis.fill(self.white)
            self.score.draw(self.font, self.dis)
            for i, l in enumerate(self.leaders):
                Text(f"{l[0]} {l[1]}", 10, 20*(i+2)).draw(self.font, self.dis)
            self.text_name.draw(self.font, self.dis)
            self.text_guide.draw(self.font, self.dis)
            self.input.draw_text(self.dis)
            self.input.draw_textbox(self.dis)
            if self.button_play.draw(self.dis): settings = True
            pygame.display.update()
            self.clock.tick(15)

    def _game_process(self):
        self.counter = 0
        self.sn = Snake()
        self.fd = Food()
        fd_coords = self.fd.get_all_coords()
        game_over=False 
        while not game_over:
            head = self.sn.elems[0]
            head_coords = head.get_all_coords()
            if len(head_coords.intersection(fd_coords)) > 0:
                self.fd.set_new_coords()
                fd_coords = self.fd.get_all_coords()
                self.sn.add_tail(self.direction)
                self.counter += 1

            if self.sn.eat_self():
                game_over = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  
                    self.db.close_connection()          
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and self.direction != pygame.K_RIGHT:
                        self.x_change = -STEP
                        self.y_change = 0
                        self.direction = pygame.K_LEFT
                    elif event.key == pygame.K_RIGHT and self.direction != pygame.K_LEFT:
                        self.x_change = STEP
                        self.y_change = 0
                        self.direction = pygame.K_RIGHT
                    elif event.key == pygame.K_UP and self.direction != pygame.K_DOWN:
                        self.x_change = 0
                        self.y_change = -STEP
                        self.direction = pygame.K_UP
                    elif event.key == pygame.K_DOWN and self.direction != pygame.K_UP:
                        self.x_change = 0
                        self.y_change = STEP
                        self.direction = pygame.K_DOWN
                
            self.sn.move(self.x_change, self.y_change)

            self.dis.fill(self.white)
            if self.counter < POINTS_WIN:
                self._msg(f"Очки: {self.counter}/{POINTS_WIN}", 10, 10)
            else:
                self._msg(f"Очки: {self.counter}", 10, 10)
            self.img_guide.draw(self.dis)
            for elem in self.sn.elems:
                pygame.draw.rect(self.dis, self.blue, (elem.x, elem.y, SIZE_SNAKE_ELEMENT, SIZE_SNAKE_ELEMENT))
            pygame.draw.rect(self.dis, self.red, (self.fd.x, self.fd.y, SIZE_FOOD, SIZE_FOOD))
            
            pygame.display.update()

            self.clock.tick(30)
        self.clock.tick(1)

        if self.input.is_empty():
            self.input.change_input("Unknown")

        name = self.input.input_text
        table = self.db.table
        if len(list(filter(lambda x: x[0]==name, self.leaders))) != 0:
            sql = f'update {table} set point = {self.counter} where name = "{name}"'
        else:
            sql = f'insert into {table} values ("{name}", {self.counter})'
        
        self.db.crud(sql)

    def _end_game(self):
        self.text_end_game = Text(f"Вы набрали {self.counter} очков!", 300, 200)
        
        game_over=False 
        while not game_over:
            for event in pygame.event.get():
                self.dis.fill(self.white)
                if event.type == pygame.QUIT or self.img_close.draw(self.dis):
                    self.db.close_connection()
                    pygame.quit()
                    quit()

                if self.img_arrow.draw(self.dis):
                    game_over = True
                
                self.back_menu.draw(self.font, self.dis)
                self.close_game.draw(self.font, self.dis)
                self.img_close.draw(self.dis)
                self.text_end_game.draw(self.font, self.dis)
            pygame.display.update()
            self.clock.tick(30)

    def play(self):
        while True:
            self._menu()
            self._game_process()
            self._end_game()