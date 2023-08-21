import pygame
from settings import *

from pygame.image import load

class Menu:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.create_data()
        self.create_buttons()
    
    def create_data(self):
        self.menu_surfs = {}
        for key, value in EDITOR_DATA.items():
            if value['menu']:
                if not value['menu'] in self.menu_surfs:
                    self.menu_surfs[value['menu']] = [(key, load(value['menu_surf']))]
                else:
                    self.menu_surfs[value['menu']].append((key, load(value['menu_surf'])))
        
    def create_buttons(self):
        size = 180
        margin = 6
        self.rect = pygame.Rect((10, 10), (1250, size))

        # button areas
        generic_button_rect = pygame.Rect(self.rect.topleft, (90, 90))
        button_margin = 5
        self.terrain_button_rect = generic_button_rect.move(0, 0).inflate(-button_margin, -button_margin)
        self.enemies_button_rect = generic_button_rect.move(90,0).inflate(-button_margin, -button_margin)
        self.keys_button_rect = generic_button_rect.move(180,0).inflate(-button_margin, -button_margin)
        self.gears_button_rect = generic_button_rect.move(270,0).inflate(-button_margin, -button_margin)
        self.statics_button_rect = generic_button_rect.move(360,0).inflate(-button_margin, -button_margin)
        self.activators_button_rect = generic_button_rect.move(450, 0).inflate(-button_margin, -button_margin)
        self.save_button_rect = generic_button_rect.move(540, 0).inflate(-button_margin, -button_margin)


        # create buttons
        self.buttons = pygame.sprite.Group()
        Button(self.terrain_button_rect, self.buttons, self.menu_surfs['common'])
        Button(self.enemies_button_rect, self.buttons, self.menu_surfs['enemy'])
        Button(self.keys_button_rect, self.buttons, self.menu_surfs['key'])
        Button(self.gears_button_rect, self.buttons, self.menu_surfs['gear'])
        Button(self.statics_button_rect, self.buttons, self.menu_surfs['static'])
        Button(self.activators_button_rect, self.buttons, self.menu_surfs['activator'])
        Button(self.save_button_rect, self.buttons, self.menu_surfs['saving'])
        
    def click(self, mouse_pos, mouse_button):

        for sprite in self.buttons:
            if sprite.rect.collidepoint(mouse_pos):
                if mouse_button[1]: #middle mouse button click
                    if sprite.items['alt']:
                        sprite.main_active = not sprite.main_active
                if mouse_button[2]: #right click
                    sprite.switch()

                return sprite.get_id()
        
    def highlight_indicator(self, index):
            if EDITOR_DATA[index]['menu'] == 'common':
                pygame.draw.rect(self.display_surface, 'pink', self.terrain_button_rect.inflate(4,4), 5, 4)
            if EDITOR_DATA[index]['menu'] == 'enemy':
                pygame.draw.rect(self.display_surface, 'pink', self.enemies_button_rect.inflate(4,4), 5, 4)
            if EDITOR_DATA[index]['menu'] == 'key':
                pygame.draw.rect(self.display_surface, 'pink', self.keys_button_rect.inflate(4,4), 5, 4)
            if EDITOR_DATA[index]['menu'] == 'gear':
                pygame.draw.rect(self.display_surface, 'pink', self.gears_button_rect.inflate(4,4), 5, 4)
            if EDITOR_DATA[index]['menu'] == 'static':
                pygame.draw.rect(self.display_surface, 'pink', self.statics_button_rect.inflate(4,4), 5, 4)
            if EDITOR_DATA[index]['menu'] == 'activator':
                pygame.draw.rect(self.display_surface, 'pink', self.activators_button_rect.inflate(4,4), 5, 4)
            if EDITOR_DATA[index]['menu'] == 'saving':
                pygame.draw.rect(self.display_surface, 'pink', self.save_button_rect.inflate(4,4), 5, 4)
            
    def display(self,index):
        self.buttons.update()
        self.buttons.draw(self.display_surface)
        self.highlight_indicator(index)


class Button(pygame.sprite.Sprite):
    def __init__(self, rect, group, items, items_alt=None):
        super().__init__(group)
        self.image = pygame.Surface(rect.size)
        self.rect = rect

        #items
        self.items = {'main': items, 'alt': items_alt}
        self.index = 0
        self.main_active = True

    def get_id(self):
        return self.items['main' if self.main_active else 'alt'][self.index][0]
    
    def switch(self):
        self.index += 1
        self.index = 0 if self.index >= len(self.items['main' if self.main_active else 'alt']) else self.index

    

    def update(self):
        self.image.fill(MM_BUT_COLOR)
        surf = self.items['main' if self.main_active else 'alt'][self.index][1]
        rect = surf.get_rect(center = (self.rect.width / 2, self.rect.height / 2))
        self.image.blit(surf, rect)