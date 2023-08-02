import pygame, sys
from settings import *

class LangChoice:
    def __init__(self):

        # main setup
        self.display_surface = pygame.display.get_surface()
        self.bg_surface = pygame.Surface((LANG_WIDTH, LANG_HEIGHT))
        self.bg_surface.fill(BG_COLOR)

        # Font
        self.font = pygame.font.SysFont('arial', 46)

        # Header
        self.rus_text = self.font.render('Выберите язык', True, BLACK_GRAY)
        self.eng_text = self.font.render('Choose your language', True, BLACK_GRAY)
        self.rus_text_rect = self.rus_text.get_rect(centerx = (WINDOW_WIDTH // 2), centery = 120)
        self.eng_text_rect = self.eng_text.get_rect(centerx = (WINDOW_WIDTH // 2), centery = 190)
        self.rus_choice = self.font.render('Русский', True, 'white')
        self.eng_choice = self.font.render('English', True, 'white')
        self.rus_choice_rect = self.rus_choice.get_rect(centerx = (WINDOW_WIDTH // 2) + 150, centery = 520)
        self.eng_choice_rect = self.eng_choice.get_rect(centerx = (WINDOW_WIDTH // 2) + 150, centery = 395)

        # English choice
        self.eng_surf = pygame.Surface((600, 100))
        self.eng_surf.fill(BLACK_GRAY)

        # Russian choice
        self.rus_surf = pygame.Surface((600, 100))
        self.rus_surf.fill(BLACK_GRAY)

        # Flags objects
        self.uk_flag_surf = pygame.image.load('images/flags/UK.png').convert_alpha()
        self.usa_flag_surf = pygame.image.load('images/flags/USA.png').convert_alpha()
        self.uk_flag_rect = self.uk_flag_surf.get_rect(centerx = 420, centery=400)
        self.usa_flag_rect = self.usa_flag_surf.get_rect(centerx = 550, centery=400)
        self.rus_flag_surf = pygame.image.load('images/flags/russia.png').convert_alpha()
        self.rus_flag_rect = self.rus_flag_surf.get_rect(centerx=420, centery=525)
        
        

    
    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def run(self, dt):
        self.display_surface.fill(BLACK_GRAY)
        self.display_surface.blit(self.bg_surface, (LANG_X, LANG_Y))
        self.display_surface.blit(self.rus_text, self.rus_text_rect)
        self.display_surface.blit(self.rus_text, self.rus_text_rect)
        pygame.draw.line(self.bg_surface, BLACK_GRAY, (100, 100), (700, 100), 4)
        self.display_surface.blit(self.eng_text, self.eng_text_rect)
        self.display_surface.blit(self.eng_surf, (340, 350))
        self.display_surface.blit(self.rus_surf, (340, 475))
        self.display_surface.blit(self.uk_flag_surf, self.uk_flag_rect)
        self.display_surface.blit(self.usa_flag_surf, self.usa_flag_rect)
        self.display_surface.blit(self.rus_flag_surf, self.rus_flag_rect)
        self.display_surface.blit(self.rus_choice, self.rus_choice_rect)
        self.display_surface.blit(self.eng_choice, self.eng_choice_rect)
        self.event_loop()