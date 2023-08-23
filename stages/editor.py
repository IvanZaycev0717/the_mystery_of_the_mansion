import pygame, sys
from pygame.math import Vector2 as vector
from pygame.mouse import get_pressed as mouse_buttons
from pygame.mouse import get_pos as mouse_pos
from settings import *
from menu import Menu
from pygame.image import load
from img_imports import import_folder

class Editor:
    """Игра в режиме редактора, для создания данных для уровней."""
    def __init__(self, land_tiles):
        self.display_surface = pygame.display.get_surface()
        self.canvas_data = {}

        # imports
        self.land_tiles = land_tiles
        self.imports()

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

        self.has_saved = False
        self.has_loaded = False

        # menu instance
        self.menu = Menu()

        # objects
        self.canvas_objects = pygame.sprite.Group()
        self.object_drag_active = False

        self.common_tile_id = 1

        # Player
        CanvasObjects(
            pos=(200, WINDOW_HEIGHT / 2),
            frames=self.animations[0]['frames'],
            tile_id=0,
            origin=self.origin,
            group=self.canvas_objects)
        
        # Sky
        self.sky_handle = CanvasObjects(
            pos=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2),
            frames=[self.sky_handle_surf],
            tile_id=1,
            origin=self.origin,
            group=self.canvas_objects
        )

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


    def get_current_cell(self):
        distance_to_origin = vector(mouse_pos()) - self.origin

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
            self.pan_input(event)
            self.selection_hotkeys(event)
            self.menu_click(event)
            self.object_drag(event)
            self.canvas_add()
            self.canvas_remove()


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
    
    # selection hotkeys
    def selection_hotkeys(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.selection_index += 1
            if event.key == pygame.K_LEFT:
                self.selection_index -= 1
        self.selection_index = max(2, min(self.selection_index, 106))
        if self.selection_index == 105:
            self.loading_data()
        if self.selection_index == 106:
            self.saving_data()
    
    def loading_data(self):
        print('LOADING')
        return
    
    def saving_data(self):
        print('SAVING')
        return

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
                CanvasObjects(
                    pos=mouse_pos(),
                    frames=self.animations[self.selection_index]['frames'],
                    tile_id = self.selection_index,
                    origin=self.origin,
                    group=self.canvas_objects)

    def canvas_remove(self):
        if mouse_buttons()[2] and not self.menu.rect.collidepoint(mouse_pos()):
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
        for cell_pos, tile in self.canvas_data.items():
            pos = self.origin + vector(cell_pos) * TILE_SIZE

            if tile.has_terrain:
                # tile.has_terrain == 2, 3, 4, 5, 6, 7, 8
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
        
        self.canvas_objects.draw(self.display_surface)

    def run(self, dt):
        self.animation_update(dt)
        self.canvas_objects.update(dt)

        self.event_loop()
        self.display_surface.fill('gray')
        self.draw_level()
        self.draw_tile_lines()
        pygame.draw.circle(self.display_surface, ORIGIN_COLOR, self.origin, 8)
        self.menu.display(self.selection_index)

class CanvasTile:
    def __init__(self, tile_id, terrain_id=0):

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

        self.load = None
        self.save = None

        # objects
        self.objects = []

        self.add_id(tile_id)

        self.is_empty = False
    
    def add_id(self, tile_id):
        options = {key: value['style'] for key, value in EDITOR_DATA.items()}
        match options[tile_id]:
            case 'common': self.has_terrain = tile_id
            case 'enemy': self.enemy = tile_id
            case 'key': self.key = tile_id
            case 'gear': self.gear = tile_id
        

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