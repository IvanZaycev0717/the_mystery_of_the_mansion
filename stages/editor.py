import pygame, sys
from pygame.math import Vector2 as vector
from pygame.mouse import get_pressed as mouse_buttons
from pygame.mouse import get_pos as mouse_pos
from settings import *
from menu import Menu

class Editor:
    """Игра в режиме редактора, для создания данных для уровней."""
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.canvas_data = {}

        # Навигация
        self.origin = vector()
        self.pan_active = False
        self.pan_offset = vector()

        # Вспомогательные линии
        self.support_line_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.support_line_surf.set_colorkey('yellow')
        self.support_line_surf.set_alpha(10)

        # Индекс выбора
        self.selection_index = 2
        self.last_selected_cell = None

        # menu instance
        self.menu = Menu()

        # support
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

    def event_loop(self):
        """Цикл событий."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self.pan_input(event)
            self.selection_hotkeys(event)
            self.menu_click(event)
            self.canvas_add()
    
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
        self.selection_index = max(2, min(self.selection_index, 105))

    def menu_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.menu.rect.collidepoint(mouse_pos()):
            new_index = self.menu.click(mouse_pos(), mouse_buttons())
            self.selection_index = new_index if new_index else self.selection_index

    def canvas_add(self):
        if mouse_buttons()[0] and not self.menu.rect.collidepoint(mouse_pos()):
            current_cell = self.get_current_cell()
            if current_cell != self.last_selected_cell:

                if current_cell in self.canvas_data:
                    self.canvas_data[current_cell].add_id(self.selection_index)
                else:
                    self.canvas_data[current_cell] = CanvasTile(self.selection_index)
                
                self.last_selected_cell = current_cell

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
    
    def run(self, dt):
        self.event_loop()
        self.display_surface.fill(BLACK_GRAY)
        self.draw_tile_lines()
        pygame.draw.circle(self.display_surface, ORIGIN_COLOR, self.origin, 8)
        self.menu.display(self.selection_index)

class CanvasTile:
    def __init__(self, tile_id):

        # terrain
        self.has_terrain = False
        self.terrain_neighbors = []

        # water
        self.has_water = False
        self.water_on_top = False

        # coin
        self.coin = None

        # enemy
        self.enemy = None

        # objects
        self.objects = []

        self.add_id(tile_id)
    
    def add_id(self, tile_id):
        options = {key: value['style'] for key, value in EDITOR_DATA.items()}
        match options[tile_id]:
            case 'common': self.has_terrain = True
            case 'enemy': self.enemy = tile_id
            case 'key': self.key = tile_id
            case 'gear': self.enemy = tile_id
            case 'static': self.static = True
            case 'activator': self.activator = tile_id
            case 'saving': self.save = True

