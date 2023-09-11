import pygame
from pygame.image import load

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
        health_bar_rect = pygame.Rect(self.hp_bar_topleft, (current_bar_width, self.bar_height))
        pygame.draw.rect(self.display_surface, '#dc4949', health_bar_rect, border_bottom_right_radius=6, border_top_right_radius=6)