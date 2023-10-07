import pygame
from pygame.image import load

from settings import *


class Menu:
    """Class for upper menu in the editor's mode."""
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.create_data()
        self.create_buttons()

    def create_data(self):
        self.menu_surfs = {}
        for key, value in EDITOR_DATA.items():
            if value['menu']:
                if not isinstance(value['menu_surf'], tuple):
                    if not value['menu'] in self.menu_surfs:
                        self.menu_surfs[value['menu']] = [
                            (key, load(value['menu_surf']))]
                    else:
                        self.menu_surfs[value['menu']].append(
                            (key, load(value['menu_surf'])))
                else:
                    terrain_choices = []
                    for image in value['menu_surf']:
                        terrain_choices.append(load(image))
                    if not value['menu'] in self.menu_surfs:
                        self.menu_surfs[value['menu']] = [
                            (key, terrain_choices)]
                    else:
                        self.menu_surfs[value['menu']].append(
                            (key, terrain_choices))

    def create_buttons(self):
        size = 180
        self.rect = pygame.Rect((10, 10), (1270, size))

        # button areas
        generic_button_rect = pygame.Rect(self.rect.topleft, (90, 90))
        button_margin = 5
        self.terrain_button_rect = generic_button_rect.move(
            0, 0).inflate(-button_margin, -button_margin)
        self.enemies_button_rect = generic_button_rect.move(
            90, 0).inflate(-button_margin, -button_margin)
        self.keys_button_rect = generic_button_rect.move(
            180, 0).inflate(-button_margin, -button_margin)
        self.gears_button_rect = generic_button_rect.move(
            270, 0).inflate(-button_margin, -button_margin)
        self.statics_button_rect = generic_button_rect.move(
            360, 0).inflate(-button_margin, -button_margin)
        self.activators_button_rect = generic_button_rect.move(
            450, 0).inflate(-button_margin, -button_margin)
        self.load_button_rect = generic_button_rect.move(
            900, 0).inflate(-button_margin, -button_margin)
        self.save_button_rect = generic_button_rect.move(
            990, 0).inflate(-button_margin, -button_margin)
        self.level_save_button = generic_button_rect.move(
            1170, 0).inflate(-button_margin, -button_margin)

        # create buttons
        self.buttons = pygame.sprite.Group()
        Button(
            self.terrain_button_rect,
            self.buttons,
            self.menu_surfs['common'])
        Button(
            self.enemies_button_rect,
            self.buttons,
            self.menu_surfs['enemy'])
        Button(self.keys_button_rect, self.buttons, self.menu_surfs['key'])
        Button(self.gears_button_rect, self.buttons, self.menu_surfs['gear'])
        Button(
            self.statics_button_rect,
            self.buttons,
            self.menu_surfs['static'])
        Button(
            self.activators_button_rect,
            self.buttons,
            self.menu_surfs['activator'])
        Button(self.load_button_rect, self.buttons, self.menu_surfs['loading'])
        Button(self.save_button_rect, self.buttons, self.menu_surfs['saving'])
        Button(
            self.level_save_button,
            self.buttons,
            self.menu_surfs['level_save'])

    def click(self, mouse_pos, mouse_button):

        for sprite in self.buttons:
            if sprite.rect.collidepoint(mouse_pos):
                if mouse_button[1]:
                    if sprite.items['alt']:
                        sprite.main_active = not sprite.main_active
                if mouse_button[2]:
                    sprite.switch()
                if mouse_button[0] and self.terrain_button_rect.collidepoint(mouse_pos):
                    if sprite.land_index < len(
                            sprite.items['main'][sprite.get_id() - 2][1]) - 1:
                        sprite.land_index += 1
                    else:
                        sprite.land_index = 0

                return sprite.get_id()

    def highlight_indicator(self, index):
        if EDITOR_DATA[index]['menu'] == 'common':
            pygame.draw.rect(
                self.display_surface,
                'pink',
                self.terrain_button_rect.inflate(
                    4,
                    4),
                5,
                4)
        if EDITOR_DATA[index]['menu'] == 'enemy':
            pygame.draw.rect(
                self.display_surface,
                'pink',
                self.enemies_button_rect.inflate(
                    4,
                    4),
                5,
                4)
        if EDITOR_DATA[index]['menu'] == 'key':
            pygame.draw.rect(
                self.display_surface,
                'pink',
                self.keys_button_rect.inflate(
                    4,
                    4),
                5,
                4)
        if EDITOR_DATA[index]['menu'] == 'gear':
            pygame.draw.rect(
                self.display_surface,
                'pink',
                self.gears_button_rect.inflate(
                    4,
                    4),
                5,
                4)
        if EDITOR_DATA[index]['menu'] == 'static':
            pygame.draw.rect(
                self.display_surface,
                'pink',
                self.statics_button_rect.inflate(
                    4,
                    4),
                5,
                4)
        if EDITOR_DATA[index]['menu'] == 'activator':
            pygame.draw.rect(
                self.display_surface,
                'pink',
                self.activators_button_rect.inflate(
                    4,
                    4),
                5,
                4)
        if EDITOR_DATA[index]['menu'] == 'loading':
            pygame.draw.rect(
                self.display_surface,
                'pink',
                self.load_button_rect.inflate(
                    4,
                    4),
                5,
                4)
        if EDITOR_DATA[index]['menu'] == 'saving':
            pygame.draw.rect(
                self.display_surface,
                'pink',
                self.save_button_rect.inflate(
                    4,
                    4),
                5,
                4)
        if EDITOR_DATA[index]['menu'] == 'level_save':
            pygame.draw.rect(
                self.display_surface,
                'pink',
                self.level_save_button.inflate(
                    4,
                    4),
                5,
                4)

    def display(self, index):
        self.buttons.update()
        self.buttons.draw(self.display_surface)
        self.highlight_indicator(index)


class Button(pygame.sprite.Sprite):
    """Class for buttons in the editor's mode."""
    def __init__(self, rect, group, items, items_alt=None):
        super().__init__(group)
        self.image = pygame.Surface(rect.size)
        self.rect = rect

        # terrain_current_choices
        self.land_index = 0

        # items
        self.items = {'main': items, 'alt': items_alt}
        self.index = 0
        self.main_active = True

    def get_id(self):
        return self.items['main' if self.main_active else 'alt'][self.index][0]

    def switch(self):
        self.land_index = 0
        self.index += 1
        self.index = 0 if self.index >= len(
            self.items['main' if self.main_active else 'alt']) else self.index

    def update(self):
        self.image.fill(MM_BUT_COLOR)
        if not isinstance(
                self.items['main' if self.main_active else 'alt'][self.index][1], list):
            surf = self.items['main' if self.main_active else 'alt'][self.index][1]
        else:
            surf = self.items['main' if self.main_active else 'alt'][self.index][1][self.land_index]
        rect = surf.get_rect(
            center=(
                self.rect.width / 2,
                self.rect.height / 2))
        self.image.blit(surf, rect)
