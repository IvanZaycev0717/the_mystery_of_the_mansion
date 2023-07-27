import sys

import pygame


from settings import *


class Author:
    def __init__(self):

        # main setup
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(FONT_PATH_2, 50)
        self.display_surface.fill(BLACK_GRAY)


    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def run(self):
        self.current_time = pygame.time.get_ticks()
        sys_font = pygame.font.SysFont('arial', 32)
        if self.current_time >= AUTHOR_TIME:
            return 2
        else:
            font_surf_1 = self.font.render(TITLE, True, 'white')
            font_surf_2 = sys_font.render(GIT_HUB, True, 'white')
            font_surf_3 = sys_font.render(E_MAIL, True, 'white')
            font_surf_4 = sys_font.render(TELEGRAM, True, 'white')

            font_rect_1 = font_surf_1.get_rect(center=(WINDOW_WIDTH // 2, 300))
            font_rect_2 = font_surf_2.get_rect(center=(WINDOW_WIDTH // 2, 500))
            font_rect_3 = font_surf_3.get_rect(center=(WINDOW_WIDTH // 2, 550))
            font_rect_4 = font_surf_4.get_rect(center=(WINDOW_WIDTH // 2, 600))

            if self.current_time < 3000:
                font_surf_1.set_alpha(int(self.current_time / 1000 * 1))
                font_surf_2.set_alpha(int(self.current_time / 1000 * 0.4))
                font_surf_3.set_alpha(int(self.current_time / 1000 * 0.4))
                font_surf_4.set_alpha(int(self.current_time / 1000 * 0.4))

            self.display_surface.blit(font_surf_1, font_rect_1)
            self.display_surface.blit(font_surf_2, font_rect_2)
            self.display_surface.blit(font_surf_3, font_rect_3)
            self.display_surface.blit(font_surf_4, font_rect_4)
            return 1
        self.event_loop()