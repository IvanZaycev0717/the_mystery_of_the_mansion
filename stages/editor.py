import json
from random import choice, randint
import tkinter as tk
from tkinter import filedialog
import pickle
import os

import pygame, sys
from pygame.math import Vector2 as vector
from pygame.mouse import get_pressed as mouse_buttons
from pygame.mouse import get_pos as mouse_pos
from settings import *
from menu import Menu
from pygame.image import load
from img_imports import import_folder
import timer

class Editor:
    """Игра в режиме редактора, для создания данных для уровней."""
    def __init__(self, land_tiles, switch, file_path, set_stage):
        self.display_surface = pygame.display.get_surface()
        self.canvas_data = {}
        self.switch = switch
        self.set_stage= set_stage

        #tkinter window
        self.dialog = tk.Tk()
        self.dialog.withdraw()
        self.game_directory = os.path.dirname(file_path)
        self.next_stage = 0

        # imports
        self.land_tiles = land_tiles
        self.imports()

         # clouds
        self.current_clouds = []
        self.cloud_surf = import_folder('images/clouds')
        self.cloud_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.cloud_timer, 2000)
        self.startup_clouds()


        # Навигация
        self.origin = vector()
        self.pan_active = False
        self.pan_offset = vector()

        # Вспомогательные линии
        self.support_line_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.support_line_surf.set_colorkey('yellow')
        self.support_line_surf.set_alpha(5)

    
        # Индекс выбора
        self.selection_index = 2
        self.current_land_tile = 2
        self.last_selected_cell = None
        self.selection_terrain = 0


        # Timer obj
        

        # menu instance
        self.menu = Menu()

        # objects
        self.canvas_objects = pygame.sprite.Group()
        self.background = pygame.sprite.Group()
        self.foreground = pygame.sprite.Group()
        self.object_drag_active = False
        self.object_timer = timer.Timer(1000)

        self.common_tile_id = 1

        # Player
        CanvasObjects(
            pos=(200, WINDOW_HEIGHT / 2),
            frames=self.animations[0]['frames'],
            tile_id=0,
            origin=self.origin,
            group = [self.canvas_objects, self.foreground])
        
        # Sky
        self.sky_handle = CanvasObjects(
            pos=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2),
            frames=[self.sky_handle_surf],
            tile_id=1,
            origin=self.origin,
            group = [self.canvas_objects, self.background])

    def imports(self):
        self.sky_handle_surf = load('images/main_menu/up.png').convert_alpha()

        self.animations = {}
        for key, value in EDITOR_DATA.items():
            if value['graphics']:
                graphics = import_folder(value['graphics'])
                self.animations[key] = {
					'frame index': 0,
					'frames': graphics,
					'length': len(graphics)
				}


    def get_current_cell(self, obj=None):
        distance_to_origin = vector(mouse_pos()) - self.origin if not obj else vector(obj.distance_to_origin) - self.origin

        if distance_to_origin.x > 0:
            col = int(distance_to_origin.x / TILE_SIZE)
        else:
            col = int(distance_to_origin.x / TILE_SIZE) - 1
        
        if distance_to_origin.y > 0:
            row = int(distance_to_origin.y / TILE_SIZE)
        else:
            row = int(distance_to_origin.y / TILE_SIZE) - 1
        return col, row
    

    def animation_update(self, dt):
        for value in self.animations.values():
            value['frame index'] += ANIMATION_SPEED * dt
            if value['frame index'] >= value['length']:
                value['frame index'] = 0

    def event_loop(self):
        """Цикл событий."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.switch(self.create_grid())
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.set_stage(0, 3)

            self.pan_input(event)
            self.selection_hotkeys(event)
            self.menu_click(event)

            self.object_drag(event)

            self.canvas_add()
            self.canvas_remove()

            self.create_clouds(event)


    def pan_input(self, event):
        """Добавляет в цикл события события для мыши."""

        # Нажата средняя кнопка мыши
        if event.type == pygame.MOUSEBUTTONDOWN and mouse_buttons()[1]:
            self.pan_active = True
            self.pan_offset = vector(mouse_pos()) - self.origin
        
        # Если не нажата средняя кнопка мыши
        if not mouse_buttons()[1]:
            self.pan_active = False

        # Событие для прокрутки колесика мышки
        if event.type == pygame.MOUSEWHEEL:
            if pygame.key.get_pressed()[pygame.K_LCTRL]:
                self.origin.y -= event.y * 50
            else:
                self.origin.x -= event.y * 50
        
        # Обновление ввода
        if self.pan_active:
            self.origin = vector(mouse_pos()) - self.pan_offset
            
            for sprite in self.canvas_objects:
                sprite.pan_pos(self.origin)
    
    def mouse_on_object(self):
        for sprite in self.canvas_objects:
            if sprite.rect.collidepoint(mouse_pos()):
                return sprite

    # selection hotkeys
    def selection_hotkeys(self, event):
        self.selection_index = max(2, min(self.selection_index, 108))
        if self.selection_index == 105:
            self.loading_data()
        if self.selection_index == 106:
            self.saving_data()
        if self.selection_index == 107:
            self.save_level()
    
    def save_level(self):
        self.selection_index = 108
        self.file_path = filedialog.asksaveasfilename(filetypes=(
                        ("MML-файл", "*.mml"),
                        ("All files", "*.*"),
                    ), initialfile='my_level.mml', initialdir=self.game_directory)
        if self.file_path:
            with open(self.file_path, 'wb') as file:
                pickle.dump(self.create_grid(), file)
    
    def loading_data(self):
        self.selection_index = 108
        self.file_path = filedialog.askopenfilename(filetypes=(
                        ("Bin-файл", "*.bin"),
                        ("All files", "*.*"),
                    ), initialdir=self.game_directory)
        if self.file_path:
            with open(self.file_path, 'rb') as file:
                load_data = pickle.load(file)
            self.canvas_data = load_data
    
    def saving_data(self):
        self.selection_index = 108
        self.file_path = filedialog.asksaveasfilename(filetypes=(
                        ("Bin-файл", "*.bin"),
                        ("All files", "*.*"),
                    ), initialfile='area1.bin', initialdir=self.game_directory)
        if self.file_path:
            with open(self.file_path, 'wb') as file:
                pickle.dump(self.canvas_data, file)

    def menu_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.menu.rect.collidepoint(mouse_pos()):
            new_index = self.menu.click(mouse_pos(), mouse_buttons())
            self.selection_index = new_index if new_index else self.selection_index
        if event.type ==  pygame.MOUSEBUTTONDOWN and self.menu.terrain_button_rect.collidepoint(mouse_pos()) and mouse_buttons()[2]:
            self.selection_terrain = 0
        if event.type ==  pygame.MOUSEBUTTONDOWN and self.menu.terrain_button_rect.collidepoint(mouse_pos()) and mouse_buttons()[0]:
            limits_dct = {2: 9, 3: 6, 4: 6, 5: 6, 6: 6, 7: 6, 8: 2}
            if self.selection_terrain < limits_dct[self.current_land_tile]:
                self.selection_terrain += 1
            else:
                self.selection_terrain = 0

    def canvas_add(self):
        if mouse_buttons()[0] and not self.menu.rect.collidepoint(mouse_pos()) and not self.object_drag_active:
            current_cell = self.get_current_cell()
            if EDITOR_DATA[self.selection_index]['type'] == 'tile':
                if current_cell != self.last_selected_cell:

                    if current_cell in self.canvas_data:
                        self.canvas_data[current_cell].add_id(self.selection_index)
                    else:
                        self.canvas_data[current_cell] = CanvasTile(self.selection_index, self.selection_terrain)
                
                    self.last_selected_cell = current_cell
            else:
                if not self.object_timer.active:
                    if EDITOR_DATA[self.selection_index]['style'] == 'activator' or EDITOR_DATA[self.selection_index]['style'] == 'static':
                        groups = [self.canvas_objects, self.background]
                        CanvasObjects(
                            pos=mouse_pos(),
                            frames=self.animations[self.selection_index]['frames'],
                            tile_id = self.selection_index,
                            origin=self.origin,
                            group=groups)
                        self.object_timer.activate()

    def canvas_remove(self):
        if mouse_buttons()[2] and not self.menu.rect.collidepoint(mouse_pos()):

            selected_object = self.mouse_on_object()
            if selected_object:
                if EDITOR_DATA[selected_object.tile_id]['style'] not in ('player', 'sky'):
                    selected_object.kill()

            if self.canvas_data:
                current_cell = self.get_current_cell()
                if current_cell in self.canvas_data:
                    self.canvas_data[current_cell].remove_id(self.selection_index)

                    if self.canvas_data[current_cell].is_empty:
                        del self.canvas_data[current_cell]
    
    def object_drag(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and mouse_buttons()[0]:
            for sprite in self.canvas_objects:
                if sprite.rect.collidepoint(event.pos):
                    sprite.start_drag()
                    self.object_drag_active = True
        
        if event.type == pygame.MOUSEBUTTONUP and self.object_drag_active:
            for sprite in self.canvas_objects:
                if sprite.selected:
                    sprite.drag_end(self.origin)
                    self.object_drag_active = False      


    def draw_tile_lines(self):
        """Рисует линии для размещения плиток."""
        cols = WINDOW_WIDTH // TILE_SIZE
        rows = WINDOW_HEIGHT // TILE_SIZE

        origin_offset = vector(
            x = self.origin.x - int(self.origin.x / TILE_SIZE) * TILE_SIZE,
            y = self.origin.y - int(self.origin.y / TILE_SIZE) * TILE_SIZE
        )

        self.support_line_surf.fill(BLACK_GRAY)
        
        for col in range(cols + 1):
            x = origin_offset.x + col * TILE_SIZE
            pygame.draw.line(self.support_line_surf, LINE_COLOR, (x,0), (x, WINDOW_HEIGHT))
        
        for row in range(rows + 1):
            y = origin_offset.y + row * TILE_SIZE
            pygame.draw.line(self.support_line_surf, LINE_COLOR, (0,y), (WINDOW_WIDTH, y))
            self.display_surface.blit(self.support_line_surf, (0, 0))
    
    def draw_level(self):
        self.background.draw(self.display_surface)
        for cell_pos, tile in self.canvas_data.items():
            pos = self.origin + vector(cell_pos) * TILE_SIZE

            if tile.has_terrain and isinstance(tile.has_terrain, int):
                self.current_land_tile = tile.has_terrain
                surf = self.land_tiles[tile.has_terrain][tile.terrain_id]
                rect = surf.get_rect(midbottom = (pos[0] + TILE_SIZE // 2, pos[1] + TILE_SIZE))
                self.display_surface.blit(surf, rect)
            
            if tile.enemy:
                frames = self.animations[tile.enemy]['frames']
                index =  int(self.animations[tile.enemy]['frame index'])
                surf = frames[index]
                rect = surf.get_rect(midbottom = (pos[0] + TILE_SIZE // 2, pos[1] + TILE_SIZE))
                self.display_surface.blit(surf, rect)

            if tile.key:
                frames = self.animations[tile.key]['frames']
                index =  int(self.animations[tile.key]['frame index'])
                surf = frames[index]
                rect = surf.get_rect(midbottom = (pos[0] + TILE_SIZE // 2, pos[1] + TILE_SIZE))
                self.display_surface.blit(surf, rect)
            
            if tile.gear:
                frames = self.animations[tile.gear]['frames']
                index =  int(self.animations[tile.gear]['frame index'])
                surf = frames[index]
                rect = surf.get_rect(midbottom = (pos[0] + TILE_SIZE // 2, pos[1] + TILE_SIZE))
                self.display_surface.blit(surf, rect)
        
        self.foreground.draw(self.display_surface)

    def preview(self):
        selected_object = self.mouse_on_object()
        if not self.menu.rect.collidepoint(mouse_pos()):
            if selected_object:
                rect = selected_object.rect.inflate(10,10)
                color = 'black'
                width = 3
                size = 15

				# topleft
                pygame.draw.lines(self.display_surface, color, False, ((rect.left,rect.top + size), rect.topleft, (rect.left + size,rect.top)), width)
				#topright
                pygame.draw.lines(self.display_surface, color, False, ((rect.right - size,rect.top), rect.topright, (rect.right,rect.top + size)), width)
				# bottomright
                pygame.draw.lines(self.display_surface, color, False, ((rect.right - size, rect.bottom), rect.bottomright, (rect.right,rect.bottom - size)), width)
				# bottomleft
                pygame.draw.lines(self.display_surface, color, False, ((rect.left,rect.bottom - size), rect.bottomleft, (rect.left + size,rect.bottom)), width)

    
    def display_sky(self, dt):
        self.display_surface.fill(SKY_COLOR)
        y = self.sky_handle.rect.centery

		# horizon lines
        if y > 0:	
            horizon_rect1 = pygame.Rect(0,y - 10,WINDOW_WIDTH,10)
            horizon_rect2 = pygame.Rect(0,y - 16,WINDOW_WIDTH,4)
            horizon_rect3 = pygame.Rect(0,y - 20,WINDOW_WIDTH,2)
            pygame.draw.rect(self.display_surface, HORIZON_TOP_COLOR, horizon_rect1)
            pygame.draw.rect(self.display_surface, HORIZON_TOP_COLOR, horizon_rect2)
            pygame.draw.rect(self.display_surface, HORIZON_TOP_COLOR, horizon_rect3)

            self.display_clouds(dt, y)
		# sea 
        if 0 < y < WINDOW_HEIGHT:
            sea_rect = pygame.Rect(0,y,WINDOW_WIDTH,WINDOW_HEIGHT)
            pygame.draw.rect(self.display_surface, SEA_COLOR, sea_rect)
            pygame.draw.line(self.display_surface, HORIZON_COLOR, (0,y), (WINDOW_WIDTH,y),3)
        if y < 0:
            self.display_surface.fill(SEA_COLOR)

    def display_clouds(self, dt, horizon_y):
        for cloud in self.current_clouds:
            cloud['pos'][0] -= cloud['speed'] * dt
            x = cloud['pos'][0]
            y = horizon_y - cloud['pos'][1]
            self.display_surface.blit(cloud['surf'], (x,y))

    def create_clouds(self, event):
        if event.type == self.cloud_timer:
            surf = choice(self.cloud_surf)
            surf = pygame.transform.scale2x(surf) if randint(0,4) < 2 else surf
            pos = [WINDOW_WIDTH + randint(50,100),randint(0,WINDOW_HEIGHT)]
            self.current_clouds.append({'surf': surf, 'pos': pos, 'speed': randint(20,50)})
            self.current_clouds = [cloud for cloud in self.current_clouds if cloud['pos'][0] > -400]

    def startup_clouds(self):
        for i in range(10):
            surf = pygame.transform.scale2x(choice(self.cloud_surf)) if randint(0,4) < 2 else choice(self.cloud_surf)
            pos = [randint(0, WINDOW_WIDTH),randint(0, WINDOW_HEIGHT)]
            self.current_clouds.append({'surf': surf, 'pos': pos, 'speed': randint(20,50)})

    def create_grid(self):
        for tile in self.canvas_data.values():
            tile.objects = []
        
        for obj in self.canvas_objects:
            current_cell = self.get_current_cell(obj)
            offset = vector(obj.distance_to_origin) - (vector(current_cell) * TILE_SIZE)

            if current_cell in self.canvas_data:
                self.canvas_data[current_cell].add_id(obj.tile_id, offset)
            else: 
                self.canvas_data[current_cell] = CanvasTile(obj.tile_id, offset)
        
        layers = {
            'common': {},
            'enemy': {},
            'key': {},
            'gear': {},
            'static': {},
            'activators': {},
            'fg objects': {},
        }

        left = sorted(self.canvas_data.keys(), key = lambda tile: tile[0])[0][0]
        top = sorted(self.canvas_data.keys(), key = lambda tile: tile[1])[0][1]


        # fill the grid
        for tile_pos, tile in self.canvas_data.items():
            row_adjusted = tile_pos[1] - top
            col_adjusted = tile_pos[0] - left
            x = col_adjusted * TILE_SIZE
            y = row_adjusted * TILE_SIZE

            if tile.has_terrain:
                layers['common'][x, y] = tile.has_terrain, tile.terrain_id
            
            if tile.enemy:
                layers['enemy'][x, y] = tile.enemy
            
            if tile.key:
                layers['key'][x, y] = tile.key
            
            if tile.gear:
                layers['gear'][(x + TILE_SIZE // 2, y + TILE_SIZE // 2)] = tile.gear
            
            if tile.objects:
                for obj, offset in tile.objects:
                    if obj in [key for key, value in EDITOR_DATA.items() if value['style'] == 'activator']:
                        layers['activators'][(int(x + offset.x), int(y + offset.y))] = obj
                    elif obj in [key for key, value in EDITOR_DATA.items() if value['style'] == 'static']:
                        layers['static'][(int(x + offset.x), int(y + offset.y))] = obj
                    else:
                        layers['fg objects'][int(x + offset.x), int(y + offset.y)] = obj
        return layers
                    


    def run(self, dt):
        self.event_loop()

        self.animation_update(dt)
        self.canvas_objects.update(dt)
        self.object_timer.update()

       
        self.display_surface.fill('gray')
        self.display_sky(dt)
        self.draw_level()
        self.draw_tile_lines()
        # pygame.draw.circle(self.display_surface, ORIGIN_COLOR, self.origin, 8)
        self.menu.display(self.selection_index)

class CanvasTile:
    def __init__(self, tile_id, terrain_id=0, offset=vector()):

        # terrain
        self.has_terrain = None
        self.terrain_neighbors = []
        self.terrain_id = terrain_id
        # enemy
        self.enemy = None

        # key
        self.key = None
        self.gear = None
        self.static = None
        self.activator = None

        # objects
        self.objects = []

        self.add_id(tile_id, offset = offset)

        self.is_empty = False
    
    def add_id(self, tile_id, offset=vector()):
        options = {key: value['style'] for key, value in EDITOR_DATA.items()}
        match options[tile_id]:
            case 'common': self.has_terrain = tile_id
            case 'enemy': self.enemy = tile_id
            case 'key': self.key = tile_id
            case 'gear': self.gear = tile_id
            case _:
                if (tile_id, offset) not in self.objects:
                    self.objects.append((tile_id, offset))
        

    def remove_id(self, tile_id):
        options = {key: value['style'] for key, value in EDITOR_DATA.items()}
        match options[tile_id]:
            case 'common': self.has_terrain = False
            case 'enemy': self.enemy = None
            case 'key': self.key = None
            case 'gear': self.gear = None
        self.check_content()

    
    def check_content(self):
        if not self.has_terrain and not self.key and not self.gear and not self.enemy:
            self.is_empty = True

class CanvasObjects(pygame.sprite.Sprite):
    def __init__(self, pos, frames, tile_id, origin, group):
        super().__init__(group)
        self.tile_id = tile_id

        self.frames = frames
        self.frame_index = 0

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)

        # movement
        self.distance_to_origin = vector(self.rect.topleft) - origin
        self.selected = False
        self.mouse_offset = vector()
    
    def start_drag(self):
        self.selected = True
        self.mouse_offset = vector(mouse_pos()) - vector(self.rect.topleft)
    
    def drag(self):
        if self.selected:
            self.rect.topleft = mouse_pos() - self.mouse_offset

    def animate(self, dt):
        self.frame_index += ANIMATION_SPEED * dt
        self.frame_index = 0 if self.frame_index >= len(self.frames) else self.frame_index
        self.image = self.frames[int(self.frame_index)]
        self.rect = self.image.get_rect(midbottom = self.rect.midbottom)

    def drag_end(self, origin):
        self.selected = False
        self.distance_to_origin = vector(self.rect.topleft) - origin
    
    def pan_pos(self, origin):
        self.rect.topleft = origin + self.distance_to_origin
    
    def update(self, dt):
        self.animate(dt)
        self.drag()