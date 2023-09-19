import pygame
from pygame.image import load
import eng
import rus
from settings import *

class UI:
    def __init__(self, surface):

        # setup
        self.display_surface = surface

        # Font
        self.font = pygame.font.SysFont('arial', 40, True)

        # lives bar
        self.lives_bar = load('images/ui/lives_bar.png').convert_alpha()

        # hp_bar
        self.hp_bar = load('images/ui/hp_bar.png').convert_alpha()
        self.hp_bar_rect = self.hp_bar.get_rect(topleft=(20, 80))
        self.hp_bar_topleft = (61 ,93)
        self.bar_max_width = 140
        self.bar_height = 18
        
    
    def show_lives(self, amount):
        self.display_surface.blit(self.lives_bar, (20, 10))
        lives_amount_surf = self.font.render(f'x{str(amount)}', False, 'red')
        lives_amount_rect = lives_amount_surf.get_rect(x=70, y=20)
        self.display_surface.blit(lives_amount_surf, lives_amount_rect)
        
    
    def show_hp(self, current, full):
        self.display_surface.blit(self.hp_bar, self.hp_bar_rect)
        current_hp_ratio = current / full
        current_bar_width = self.bar_max_width * current_hp_ratio
        current_bar_width = 0 if current_bar_width < 0 else current_bar_width
        health_bar_rect = pygame.Rect(self.hp_bar_topleft, (current_bar_width, self.bar_height))
        pygame.draw.rect(self.display_surface, '#dc4949', health_bar_rect, border_bottom_right_radius=6, border_top_right_radius=6)

class Inventory:
    def __init__(self, surface, config):
        # setup
        self.display_surface = surface
        self.config = config

        # Font
        self.font = pygame.font.SysFont('arial', 40, True)
        self.lang = None


        # loading images
        self.gear_img = load('images/ui/inventory/gear.png').convert_alpha()
        self.gear_rect = self.gear_img.get_rect(x=1000, y=100)
        self.green_key_img = load('images/ui/inventory/green_key.png').convert_alpha()
        self.green_key_rect = self.green_key_img.get_rect(x=997, y=140)
        self.hammer_img = load('images/ui/inventory/hammer.png').convert_alpha()
        self.hammer_rect = self.hammer_img.get_rect(x=997, y=200)
        self.pink_key_img =  load('images/ui/inventory/pink_key.png').convert_alpha()
        self.pink_key_rect = self.pink_key_img.get_rect(x=1000, y=270)
        self.yellow_key_img =  load('images/ui/inventory/yellow_key.png').convert_alpha()
        self.yellow_key_rect = self.yellow_key_img.get_rect(x=1000, y=330)


    def show_inventory(self, gears_amount, player_stats):
        self.lang = self.config.get('LANG', 'Lang')
        pygame.draw.rect(self.display_surface, BLACK_GRAY, (960, 15, 300, 400))

        # inventory inscription
        self.inventory_insc = self.font.render(eng.INV_INSC if self.lang == 'eng' else rus.INV_INSC, False, 'yellow')
        self.inventory_insc_rect = self.inventory_insc.get_rect(x=1025, y=30)

        # Images of items
        self.display_surface.blit(self.inventory_insc, self.inventory_insc_rect)
        self.display_surface.blit(self.gear_img, self.gear_rect)
        self.display_surface.blit(self.green_key_img, self.green_key_rect)
        self.display_surface.blit(self.hammer_img, self.hammer_rect)
        self.display_surface.blit(self.pink_key_img, self.pink_key_rect)
        self.display_surface.blit(self.yellow_key_img, self.yellow_key_rect)

        # Status of items
        self.gears_amount = self.font.render(f'x{gears_amount}', False, 'yellow')
        self.gears_amount_rect = self.gears_amount.get_rect(x=1060, y=82)
        self.display_surface.blit(self.gears_amount, self.gears_amount_rect)

        self.green_status = self.font.render((eng.KEY_FOUND if player_stats['green_key'] else eng.KEY_NOT_FOUND) if self.lang == 'eng' else (rus.KEY_FOUND if player_stats['green_key'] else rus.KEY_NOT_FOUND), False, 'yellow')
        self.green_status_rect = self.green_status.get_rect(x=1060, y=140)
        self.display_surface.blit(self.green_status, self.green_status_rect)

        self.hammer_status = self.font.render((eng.KEY_FOUND if player_stats['hammer_key'] else eng.KEY_NOT_FOUND) if self.lang == 'eng' else (rus.KEY_FOUND if player_stats['hammer_key'] else rus.KEY_NOT_FOUND), False, 'yellow')
        self.hammer_status_rect = self.hammer_status.get_rect(x=1060, y=210)
        self.display_surface.blit(self.hammer_status, self.hammer_status_rect)

        self.pink_status = self.font.render((eng.KEY_FOUND if player_stats['pink_key'] else eng.KEY_NOT_FOUND) if self.lang == 'eng' else (rus.KEY_FOUND if player_stats['pink_key'] else rus.KEY_NOT_FOUND), False, 'yellow')
        self.pink_status_rect = self.pink_status.get_rect(x=1060, y=270)
        self.display_surface.blit(self.pink_status, self.pink_status_rect)

        self.yellow_status = self.font.render((eng.KEY_FOUND if player_stats['yellow_key'] else eng.KEY_NOT_FOUND) if self.lang == 'eng' else (rus.KEY_FOUND if player_stats['yellow_key'] else rus.KEY_NOT_FOUND), False, 'yellow')
        self.yellow_status_rect = self.yellow_status.get_rect(x=1060, y=335)
        self.display_surface.blit(self.yellow_status, self.yellow_status_rect)

class Helper:
    def __init__(self, surface, config):
        # setup
        self.display_surface = surface
        self.config = config
        self.timer = 0

        # Font
        self.font = pygame.font.SysFont('arial', 26, True)
        self.lang = None

    def show_helper(self, message):
        self.lang = self.config.get('LANG', 'Lang')
        pygame.draw.rect(self.display_surface, BLACK_GRAY, (365, 15, 550, 50))
        self.message = self.font.render(eng.HLP[message] if self.lang == 'eng' else rus.HLP[message], False, 'yellow')
        self.message_rect = self.message.get_rect(centerx=WINDOW_WIDTH / 2, centery=37)
        self.display_surface.blit(self.message, self.message_rect)


        


