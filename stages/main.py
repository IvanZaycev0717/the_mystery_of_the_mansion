import pickle
from pprint import pprint
import pygame, sys
from pygame.image import load
import os
from pygame.math import Vector2 as vector
import configparser



from settings import *
from author import Author
from editor import Editor
from level import Level, Common, Cementry, Hall, Cupboard, Heaven, FirstFloor, Desert, SecondFloor, Garden, Poison
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
        self.icon = pygame.display.set_icon(pygame.image.load(ICON_PATH).convert_alpha())
        self.clock = pygame.time.Clock()
        self.imports()
        self.level = None
        


        # folders
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.lang_file = 'config.ini'
        self.file_path = os.path.join(self.path, self.lang_file)

        # Game Configuration
        self.config = configparser.ConfigParser()
        if not os.path.isfile(self.file_path):
            self.config['LANG'] = {'Lang': 'None'}
            self.config['SOUNDS'] = {'Sounds': '0.2', 'Music': '0.2'}
            self.config['FULLSCREEN'] = {'Fullscreen': 'False'}
            with open(self.file_path, 'w') as configfile:
                self.config.write(configfile)
        self.config.read(self.file_path)


        
        self.toggle_to_fullscreen = True

    
        self.prev_stage = 3

        self.gears = 0
        self.player_stats = {'max_hp': 100, 'current_hp': 100, 'lives': 1, 'green_key': False, 'pink_key': False, 'hammer_key': False, 'yellow_key': False}



        # Выбор стадии иг
        self.stage = 3

        
        

        # Звуки
        self.level_sounds = {
             'gear': pygame.mixer.Sound('audio/sounds/gear.wav'),
             'hit': pygame.mixer.Sound('audio/sounds/hit.wav'),
             'jump': pygame.mixer.Sound('audio/sounds/jump.wav'),
             'key': pygame.mixer.Sound('audio/sounds/key.wav'),
             'walk': pygame.mixer.Sound('audio/sounds/walk.wav'),
             'main_theme': pygame.mixer.Sound('audio/music/main_theme.ogg'),
             'common_theme': pygame.mixer.Sound('audio/music/common.ogg'),
             'cementry_theme': pygame.mixer.Sound('audio/music/cementry.ogg'),
             'heaven_theme': pygame.mixer.Sound('audio/music/heaven.ogg'),
             'inside_theme': pygame.mixer.Sound('audio/music/inside.ogg'),
             'desert_theme': pygame.mixer.Sound('audio/music/desert.ogg'),
             'garden_theme': pygame.mixer.Sound('audio/music/garden.ogg'),
             'poison_theme': pygame.mixer.Sound('audio/music/poison.ogg'),
        }

        # Замена курсора в игре
        surf = pygame.image.load('images/cursors/cursor.png').convert_alpha()
        cursor = pygame.cursors.Cursor((0, 0), surf)
        pygame.mouse.set_cursor(cursor)

        # Экземпляры классов соответсвующих уровней
        self.author = Author()
        self.lang_choice = LangChoice(self.file_path, self.config)
        self.main_menu = MainMenu(self.set_prev_stage, self.start_new_game, self.level_sounds, self.config, self.file_path, self.switch_full_screen)
        self.editor_active = True
        self.transition = Transition(self.toggle)
        self.editor = Editor(self.land_tiles, self.switch, self.file_path, self.set_prev_stage)
        self.ui = UI(self.display_surface)
        self.dead_time = 0


        # LEVELS INITIALIZATION

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
        
    # load levels data
    def start_new_game(self):
        self.gears = 0
        self.player_stats = {'max_hp': 100, 'current_hp': 100, 'lives': 1, 'green_key': False, 'pink_key': False, 'hammer_key': False, 'yellow_key': False}
        self.current_task = None
        self.common_level = Common(
            grid=self.loading_level('common.mml'),
            switch=self.switch,
            asset_dict=self.level_data,
            audio=self.level_sounds,
            gear_change=self.change_gears,
            hp=self.change_hp,
            change_keys=self.change_keys,
            set_prev_stage=self.set_prev_stage,
            transition=self.show_transition,
            config=self.config,
            sky_color=LV_BG['common']['SKY'],
            ground_color=LV_BG['common']['GRD'],
            )
        
        self.cementry_level = Cementry(
            grid=self.loading_level('cementry.mml'),
            switch=self.switch,
            asset_dict=self.level_data,
            audio=self.level_sounds,
            gear_change=self.change_gears,
            hp=self.change_hp,
            change_keys=self.change_keys,
            set_prev_stage=self.set_prev_stage,
            transition=self.show_transition,
            config=self.config,
            sky_color=LV_BG['cementry']['SKY'],
            ground_color=LV_BG['cementry']['GRD'],
            
        )

        self.hall_level = Hall(
            grid=self.loading_level('hall.mml'),
            switch=self.switch,
            asset_dict=self.level_data,
            audio=self.level_sounds,
            gear_change=self.change_gears,
            hp=self.change_hp,
            change_keys=self.change_keys,
            set_prev_stage=self.set_prev_stage,
            transition=self.show_transition,
            sky_color=LV_BG['inside']['SKY'],
            ground_color=LV_BG['inside']['GRD'],
            config=self.config,
            has_clouds=False,
            has_horizon=False,
        )

        self.cupboard_level = Cupboard(
            grid=self.loading_level('cupboard.mml'),
            switch=self.switch,
            asset_dict=self.level_data,
            audio=self.level_sounds,
            gear_change=self.change_gears,
            hp=self.change_hp,
            change_keys=self.change_keys,
            set_prev_stage=self.set_prev_stage,
            transition=self.show_transition,
            sky_color=LV_BG['inside']['SKY'],
            ground_color=LV_BG['inside']['GRD'],
            config=self.config,
            has_clouds=False,
            has_horizon=False,
        )

        self.heaven_level = Heaven(
            grid=self.loading_level('heaven.mml'),
            switch=self.switch,
            asset_dict=self.level_data,
            audio=self.level_sounds,
            gear_change=self.change_gears,
            hp=self.change_hp,
            change_keys=self.change_keys,
            set_prev_stage=self.set_prev_stage,
            transition=self.show_transition,
            config=self.config,
            sky_color=LV_BG['heaven']['SKY'],
            ground_color=LV_BG['heaven']['GRD'],
        )

        self.first_floor_level = FirstFloor(
            grid=self.loading_level('first_floor.mml'),
            switch=self.switch,
            asset_dict=self.level_data,
            audio=self.level_sounds,
            gear_change=self.change_gears,
            hp=self.change_hp,
            change_keys=self.change_keys,
            set_prev_stage=self.set_prev_stage,
            transition=self.show_transition,
            sky_color=LV_BG['inside']['SKY'],
            ground_color=LV_BG['inside']['GRD'],
            config=self.config,
            has_clouds=False,
            has_horizon=False,
        )

        self.desert_level = Desert(
            grid=self.loading_level('desert.mml'),
            switch=self.switch,
            asset_dict=self.level_data,
            audio=self.level_sounds,
            gear_change=self.change_gears,
            hp=self.change_hp,
            change_keys=self.change_keys,
            set_prev_stage=self.set_prev_stage,
            transition=self.show_transition,
            sky_color=LV_BG['desert']['SKY'],
            ground_color=LV_BG['desert']['GRD'],
            config=self.config,
            has_clouds=False,
            has_horizon=True,
        )

        self.second_floor_level = SecondFloor(
            grid=self.loading_level('second_floor.mml'),
            switch=self.switch,
            asset_dict=self.level_data,
            audio=self.level_sounds,
            gear_change=self.change_gears,
            hp=self.change_hp,
            change_keys=self.change_keys,
            set_prev_stage=self.set_prev_stage,
            transition=self.show_transition,
            config=self.config,
            sky_color=LV_BG['inside']['SKY'],
            ground_color=LV_BG['inside']['GRD'],
            has_clouds=False,
            has_horizon=False,
        )

        self.garden_level = Garden(
            grid=self.loading_level('garden.mml'),
            switch=self.switch,
            asset_dict=self.level_data,
            audio=self.level_sounds,
            gear_change=self.change_gears,
            hp=self.change_hp,
            change_keys=self.change_keys,
            set_prev_stage=self.set_prev_stage,
            transition=self.show_transition,
            config=self.config,
            sky_color=LV_BG['garden']['SKY'],
            ground_color=LV_BG['garden']['GRD'],
            
        )

        self.poison_level = Poison(
            grid=self.loading_level('poison.mml'),
            switch=self.switch,
            asset_dict=self.level_data,
            audio=self.level_sounds,
            gear_change=self.change_gears,
            hp=self.change_hp,
            change_keys=self.change_keys,
            set_prev_stage=self.set_prev_stage,
            transition=self.show_transition,
            config=self.config,
            sky_color=LV_BG['poison']['SKY'],
            ground_color=LV_BG['poison']['GRD'],
            has_clouds=False,
        )
        self.prev_stage = 3

    def show_transition(self):
        self.transition.active = True

    def set_prev_stage(self, prev_stage, current_stage):
        self.transition.active = True
        self.stage = current_stage
        self.prev_stage = prev_stage

    def change_gears(self, amount):
        self.gears += amount

    def change_hp(self, damage):
        self.player_stats['current_hp'] -= damage
    
    def change_keys(self, key_type):
        self.player_stats[key_type] = True
    
    def level_transmission(self, dt):
        self.level.player.current_hp = self.player_stats['current_hp']
        if self.level.player.status == 'death':
            self.dead_time += dt
            if self.dead_time >= 5:
                self.player_stats['lives'] -= 1
                self.player_stats['current_hp'] = 100
                self.dead_time = 0
    
    def common_transmission(self, stage_name, dt):
        stage_name.player.current_hp = self.player_stats['current_hp']
        if self.player_stats['lives'] < 0:
            print('Game  Over')
            self.stage = 3
            self.prev_stage = 3
        if stage_name.player.status == 'death':
            self.dead_time += dt
            if self.dead_time >= 5:
                self.player_stats['lives'] -= 1
                self.player_stats['current_hp'] = 100
                self.dead_time = 0
        
    def switch_full_screen(self):
        self.toggle_to_fullscreen = not self.toggle_to_fullscreen

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
                    data.append(pygame.image.load(image))
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
            self.level = Level(
                grid=grid,
                switch=self.switch,
                asset_dict=self.level_data,
                audio=self.level_sounds,
                gear_change=self.change_gears,
                hp=self.change_hp,
                change_keys=self.change_keys,
                set_prev_stage=self.set_prev_stage,
                config=self.config,
                sky_color=SKY_COLOR,
                ground_color=SEA_COLOR
            )

    def run(self):
        while True:
            dt = self.clock.tick() / 1000
            self.fullscreen_mode = self.config.getboolean('FULLSCREEN', 'fullscreen')
            if self.toggle_to_fullscreen:
                if self.fullscreen_mode:
                    self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)
                else:
                    self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
                self.toggle_to_fullscreen = False
            match self.stage:
                case 0:
                    if self.editor_active: 
                        self.editor.run(dt)
                    else:
                        self.level.run(dt, self.gears, self.player_stats, self.stage)
                        self.level_transmission(dt)
                    self.transition.display(dt)
                case 1:
                    self.stage = self.author.run()
                case 2:
                    if self.config.get('LANG', 'Lang') not in ('eng', 'rus'):
                        self.lang_choice.run(dt)
                    else:
                        self.stage = 3
                case 3:
                    self.stage = self.main_menu.run(dt, self.stage, self.prev_stage)
                    self.transition.display(dt)
                case 4:
                    self.stage = self.common_level.run(dt, self.gears, self.player_stats, self.stage, self.prev_stage)                                    
                    self.ui.show_lives(self.player_stats['lives'])
                    self.ui.show_hp(self.player_stats['current_hp'], self.player_stats['max_hp'])
                    self.common_transmission(self.common_level, dt)
                    self.transition.display(dt)
                case 5:
                    self.stage = self.cementry_level.run(dt, self.gears, self.player_stats, self.stage)                                    
                    self.ui.show_lives(self.player_stats['lives'])
                    self.ui.show_hp(self.player_stats['current_hp'], self.player_stats['max_hp'])
                    self.common_transmission(self.cementry_level, dt)
                    self.transition.display(dt)
                case 6:
                    self.stage = self.hall_level.run(dt, self.gears, self.player_stats, self.stage)                                    
                    self.ui.show_lives(self.player_stats['lives'])
                    self.ui.show_hp(self.player_stats['current_hp'], self.player_stats['max_hp'])
                    self.common_transmission(self.hall_level, dt)
                    self.transition.display(dt)
                case 7:
                    self.stage = self.cupboard_level.run(dt, self.gears, self.player_stats, self.stage)                                    
                    self.ui.show_lives(self.player_stats['lives'])
                    self.ui.show_hp(self.player_stats['current_hp'], self.player_stats['max_hp'])
                    self.common_transmission(self.cupboard_level, dt)
                    self.transition.display(dt)
                case 8:
                    self.stage = self.heaven_level.run(dt, self.gears, self.player_stats, self.stage)                                    
                    self.ui.show_lives(self.player_stats['lives'])
                    self.ui.show_hp(self.player_stats['current_hp'], self.player_stats['max_hp'])
                    self.common_transmission(self.heaven_level, dt)
                    self.transition.display(dt)
                case 9:
                    self.stage = self.first_floor_level.run(dt, self.gears, self.player_stats, self.stage)                                    
                    self.ui.show_lives(self.player_stats['lives'])
                    self.ui.show_hp(self.player_stats['current_hp'], self.player_stats['max_hp'])
                    self.common_transmission(self.first_floor_level, dt)
                    self.transition.display(dt)
                case 10:
                    self.stage = self.desert_level.run(dt, self.gears, self.player_stats, self.stage)                                    
                    self.ui.show_lives(self.player_stats['lives'])
                    self.ui.show_hp(self.player_stats['current_hp'], self.player_stats['max_hp'])
                    self.common_transmission(self.desert_level, dt)
                    self.transition.display(dt)
                case 11:
                    self.stage = self.second_floor_level.run(dt, self.gears, self.player_stats, self.stage)                                    
                    self.ui.show_lives(self.player_stats['lives'])
                    self.ui.show_hp(self.player_stats['current_hp'], self.player_stats['max_hp'])
                    self.common_transmission(self.second_floor_level, dt)
                    self.transition.display(dt)
                case 12:
                    self.stage = self.garden_level.run(dt, self.gears, self.player_stats, self.stage)                                    
                    self.ui.show_lives(self.player_stats['lives'])
                    self.ui.show_hp(self.player_stats['current_hp'], self.player_stats['max_hp'])
                    self.common_transmission(self.garden_level, dt)
                    self.transition.display(dt)
                case 13:
                    self.stage = self.poison_level.run(dt, self.gears, self.player_stats, self.stage)                                    
                    self.ui.show_lives(self.player_stats['lives'])
                    self.ui.show_hp(self.player_stats['current_hp'], self.player_stats['max_hp'])
                    self.common_transmission(self.poison_level, dt)
                    self.transition.display(dt)
            pygame.display.update()


class Transition:
    def __init__(self, toggle):
        self.display_surface = pygame.display.get_surface()
        self.toggle = toggle
        self.active = False
        self.width = 720
        

    
    def display(self, dt):
        if self.active:
            
            self.width -= int(1200 * dt)
            
            if self.width <= 0:
                self.active = False
                self.width = 720
                self.toggle()
            pygame.draw.rect(self.display_surface, CURTAIN_COLOR, (0, 0, WINDOW_WIDTH, self.width), border_bottom_left_radius=30, border_bottom_right_radius=30)

if __name__ == '__main__':
    main = Main()
    main.run()