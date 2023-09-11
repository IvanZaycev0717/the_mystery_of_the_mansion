import pickle
import pygame, sys
from pygame.image import load
import os
from pygame.math import Vector2 as vector



from settings import *
from author import Author
from editor import Editor
from level import Level, Common
from lang_choice import LangChoice
from main_menu import MainMenu
from ui import UI
from img_imports import import_folder_dict, import_folder


class Main:
    """Главное окно игры, где происходит игровой процесс."""
    def __init__(self):
        # Настройки главного окна игры
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.title = pygame.display.set_caption(TITLE)
        self.icon = pygame.display.set_icon(pygame.image.load(ICON_PATH))
        self.clock = pygame.time.Clock()
        self.imports()

        # folders
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.lang_file = 'lang.txt'
        self.file_path = os.path.join(self.path, self.lang_file)



        # Экземпляры классов соответсвующих уровней
        self.author = Author()
        self.lang_choice = LangChoice()
        self.main_menu = MainMenu()
        self.editor_active = True
        self.transition = Transition(self.toggle)
        self.editor = Editor(self.land_tiles, self.switch, self.file_path)

        # Выбор стадии игр
        self.stage = 0

        self.lives_amount = 5
        self.max_hp = 100
        self.current_hp = 20
        self.gears = 0
        self.has_green_key = False
        self.has_pink_key = False
        self.has_yellow_key = False
        self.hammer = False
        self.current_task = None
        self.ui = UI(self.display_surface)

        # Звуки
        self.level_sounds = {
             'gear': pygame.mixer.Sound('audio/sounds/gear.wav'),
             'hit': pygame.mixer.Sound('audio/sounds/hit.wav'),
             'jump': pygame.mixer.Sound('audio/sounds/jump.wav'),
        }

        # Замена курсора в игре
        surf = load('images/cursors/cursor.png').convert_alpha()
        cursor = pygame.cursors.Cursor((0, 0), surf)
        pygame.mouse.set_cursor(cursor)

        self.level_data = {
                 'land': self.land_tiles,
                 'green_key': self.green_key,
                 'hammer': self.hammer,
                 'pink_key': self.pink_key,
                 'yellow_key': self.yellow_key,
                 'gear': self.gear,
                 'taken': self.taken,
                 'cementry_stuff': self.cementry_stuff,
                 'common_stuff': self.common_stuff,
                 'cupboard_stuff': self.cupboard_stuff,
                 'desert_stuff': self.desert_stuff,
                 'first_floor_stuff': self.first_floor_stuff,
                 'floor_stuff': self.floor_stuff,
                 'garden_stuff': self.garden_stuff,
                 'heaven_stuff': self.heaven_stuff,
                 'poison_stuff': self.poison_stuff,
                 'activators': self.activators,
                 'bat': self.bat,
                 'bug': self.bug,
                 'cem_spikes': self.cem_spikes,
                 'camel': self.camel,
                 'fire': self.fire,
                 'bird': self.bird,
                 'goat': self.goat,
                 'hedgehog': self.hedgehog,
                 'gar_spikes': self.gar_spikes,
                 'wasp': self.wasp,
                 'angel': self.angel,
                 'harp': self.harp,
                 'scrolls': self.scrolls,
                 'heav_spikes': self.heav_spikes,
                 'disputes': self.disputes,
                 'slime': self.slime,
                 'player': self.player_graphics,
                 'splutter': self.splutter,
                 'arrow': self.arrow,
                 'clouds': self.clouds,
                }
        self.common_level_data = self.loading_level('my_level.mml')
        self.common_level = Common(self.common_level_data, self.switch, self.level_data, self.level_sounds)

    def loading_level(self, file_name):
        with open(f'stages/{file_name}', 'rb') as file:
            load_data = pickle.load(file)
        return load_data

    def imports(self):

        # TERRAIN, SOIL AND GROUND
        self.land_tiles = {}
        for key, value in EDITOR_DATA.items():
            if 2 <= key <= 8:
                data = []
                for image in value['menu_surf']:
                    data.append(load(image))
                self.land_tiles[key] = data
        
        # KEYS
        self.green_key = import_folder('images/objects/keys/green')
        self.hammer = import_folder('images/objects/keys/hammer')
        self.pink_key = import_folder('images/objects/keys/pink')
        self.yellow_key = import_folder('images/objects/keys/yellow')
        
        # GEARS
        self.gear = import_folder('images/objects/gear/rolated')
        self.taken = import_folder('images/objects/gear/taken')

        # STATIC
        self.cementry_stuff = {folder: import_folder(f'images/objects/cementry/{folder}') for folder in (list(os.walk('images/objects/cementry/')))[0][1]}
        self.common_stuff = {folder: import_folder(f'images/objects/common/{folder}') for folder in (list(os.walk('images/objects/common/')))[0][1]}
        self.desert_stuff = {folder: import_folder(f'images/objects/desert/{folder}') for folder in (list(os.walk('images/objects/desert/')))[0][1]}
        self.cupboard_stuff = {folder: import_folder(f'images/objects/cupboard/{folder}') for folder in (list(os.walk('images/objects/cupboard/')))[0][1]}
        self.first_floor_stuff = {folder: import_folder(f'images/objects/first_floor/{folder}') for folder in (list(os.walk('images/objects/first_floor/')))[0][1]}
        self.floor_stuff = {folder: import_folder(f'images/objects/floor/{folder}') for folder in (list(os.walk('images/objects/floor/')))[0][1]}
        self.garden_stuff = {folder: import_folder(f'images/objects/garden/{folder}') for folder in (list(os.walk('images/objects/garden/')))[0][1]}
        self.heaven_stuff = {folder: import_folder(f'images/objects/heaven/{folder}') for folder in (list(os.walk('images/objects/heaven/')))[0][1]}
        self.poison_stuff = {folder: import_folder(f'images/objects/poison/{folder}') for folder in (list(os.walk('images/objects/poison/')))[0][1]}
        
        # ACTIVATORS
        self.activators = {folder: import_folder(f'images/objects/activators/{folder}') for folder in (list(os.walk('images/objects/activators/')))[0][1]}

        # ENEMIES
        # cementry enemies
        self.bat = import_folder('images/enemies/cementry/bat/')
        self.bug = import_folder('images/enemies/cementry/bug/')
        self.cem_spikes = load('images/enemies/cementry/spikes/1.png').convert_alpha()
        
        # desert enemies
        self.camel = load('images/enemies/desert/camel/1.png').convert_alpha()
        self.fire = import_folder('images/enemies/desert/fire/')
        self.bird = {folder: import_folder(f'images/enemies/desert/fire_bird/{folder}') for folder in (list(os.walk('images/enemies/desert/fire_bird/')))[0][1]}
        self.goat =  {folder: import_folder(f'images/enemies/desert/goat/{folder}') for folder in (list(os.walk('images/enemies/desert/goat/')))[0][1]}
        self.splutter = load('images/enemies/desert/splutter/1.png').convert_alpha()
        
        # garden enemies
        self.hedgehog = import_folder('images/enemies/garden/hedgehog/')
        self.gar_spikes = load('images/enemies/garden/spikes/1.png').convert_alpha()
        self.wasp = load('images/enemies/garden/wasp/1.png').convert_alpha()

        # heaven enemies
        self.angel = {folder: import_folder(f'images/enemies/heaven/angel/{folder}') for folder in (list(os.walk('images/enemies/heaven/angel/')))[0][1]}
        self.harp = import_folder('images/enemies/heaven/harp/')
        self.scrolls = import_folder('images/enemies/heaven/scrolls/')
        self.heav_spikes = load('images/enemies/heaven/spikes/1.png').convert_alpha()
        self.arrow = load('images/enemies/heaven/arrow/1.png').convert_alpha()

        # poison
        self.disputes = import_folder('images/enemies/poison/disputes/')
        self.slime = import_folder('images/enemies/poison/slime/')

        # player
        self.player_graphics = {folder: import_folder(f'images/player/{folder}') for folder in (list(os.walk('images/player/')))[0][1]}

        self.clouds =import_folder('images/clouds/')

    def toggle(self):
        self.editor_active = not self.editor_active

    def switch(self, grid = None): 
        self.transition.active = True
        if grid:
            self.level = Level(grid, self.switch, self.level_data, self.level_sounds)

    def run(self):
        while True:
            dt = self.clock.tick() / 1000
            match self.stage:
                case 0:
                    if self.editor_active: 
                        self.editor.run(dt)
                    else:
                        self.level.run(dt)
                    self.transition.display(dt)
                case 1: self.stage = self.author.run()
                case 2:
                    if not os.path.isfile(self.file_path):
                        self.lang_choice.run(dt)
                    else:
                        self.stage = 3
                case 3: self.stage = self.main_menu.run(dt)
                case 4:
                    self.common_level.run(dt)
                    self.ui.show_lives(self.lives_amount)
                    self.ui.show_hp(self.current_hp, self.max_hp)
            pygame.display.update()


class Transition:
    def __init__(self, toggle):
        self.display_surface = pygame.display.get_surface()
        self.toggle = toggle
        self.active = False
        self.alpha = 0
        self.alpha_increment = 51
        self.alpha_threshold = 255
        

    
    def display(self, dt):
        if self.active:
            self.alpha += self.alpha_increment
            if self.alpha >= self.alpha_threshold:
                self.alpha_increment *= -1
                self.toggle()
            
            if self.alpha <= 0:
                self.active = False
                self.alpha = 0
                self.alpha_increment *= -1
            pygame.draw.rect(self.display_surface, BLACK_GRAY, (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))
            

if __name__ == '__main__':
    main = Main()
    main.run()