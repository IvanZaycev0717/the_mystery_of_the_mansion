import pygame, sys
from pygame.image import load


from settings import *
from author import Author
from editor import Editor


class Main:
    """Главное окно игры, где происходит игровой процесс."""
    def __init__(self):
        # Настройки главного окна игры
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.title = pygame.display.set_caption(TITLE)
        self.icon = pygame.display.set_icon(pygame.image.load(ICON_PATH))
        self.clock = pygame.time.Clock()

        # Экземпляры классов соответсвующих уровней
        self.editor = Editor()
        self.author = Author()

        # Выбор стадии игры
        self.stage = 0

        # Замена курсора в игре
        surf = load('images/cursors/cursor.png').convert_alpha()
        cursor = pygame.cursors.Cursor((0, 0), surf)
        pygame.mouse.set_cursor(cursor)


    def run(self):
        while True:
            dt = self.clock.tick() / 1000
            # Switching stages
            if self.stage == 0:
                self.editor.run(dt)
            elif self.stage == 1:
                self.stage = self.author.run()

            pygame.display.update()

if __name__ == '__main__':
    main = Main()
    main.run()