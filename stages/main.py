import pygame, sys
from pygame.image import load
import os


from settings import *
from author import Author
from editor import Editor
from lang_choice import LangChoice
from main_menu import MainMenu
from img_imports import import_folder_dict


class Main:
    """Главное окно игры, где происходит игровой процесс."""
    def __init__(self):
        # Настройки главного окна игры
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.title = pygame.display.set_caption(TITLE)
        # self.icon = pygame.display.set_icon(pygame.image.load(ICON_PATH))
        self.clock = pygame.time.Clock()
        self.imports()

        # Экземпляры классов соответсвующих уровней
        self.editor = Editor(self.land_tiles)
        self.author = Author()
        self.lang_choice = LangChoice()
        self.main_menu = MainMenu()

        # Выбор стадии игры
        self.stage = 0

        # folders
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.lang_file = 'lang.txt'
        self.file_path = os.path.join(self.path, self.lang_file)

        # Замена курсора в игре
        surf = load('images/cursors/cursor.png').convert_alpha()
        cursor = pygame.cursors.Cursor((0, 0), surf)
        pygame.mouse.set_cursor(cursor)


    def imports(self):
        self.land_tiles = {}
        for key, value in EDITOR_DATA.items():
            if 2 <= key <= 8:
                data = []
                for image in value['menu_surf']:
                    data.append(load(image))
                self.land_tiles[key] = data


    def run(self):
        while True:
            dt = self.clock.tick() / 1000
            # Switching stages
            match self.stage:
                case 0: self.editor.run(dt)
                case 1: self.stage = self.author.run()
                case 2:
                    if not os.path.isfile(self.file_path):
                        self.lang_choice.run(dt)
                    else:
                        self.stage = 3
                case 3:
                    self.stage = self.main_menu.run(dt)

            pygame.display.update()

if __name__ == '__main__':
    main = Main()
    main.run()