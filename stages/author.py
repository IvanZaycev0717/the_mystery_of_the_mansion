import sys


import pygame


from settings import *


class Author:
    """Стартовая заставка с названием и контактами автора."""
    def __init__(self):

        # main setup
        self.display_surface = pygame.display.get_surface()
        self.display_surface.fill(BLACK_GRAY)
        self.font = pygame.font.Font(FONT_PATH_2, 50)
        self.ticks = pygame.time.Clock()
        self.scene_during = 0

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def run(self):
        self.scene_during += self.ticks.tick()
        sys_font = pygame.font.SysFont('arial', 32)
        if self.scene_during >= AUTHOR_TIME:
            self.scene_during = 0
            pygame.mouse.set_visible(True)
            return 2
        else:
            pygame.mouse.set_visible(False)
            font_surf_1 = self.font.render(TITLE, True, 'white')
            font_surf_2 = sys_font.render(GIT_HUB, True, 'white')
            font_surf_4 = sys_font.render(TELEGRAM, True, 'white')

            font_rect_1 = font_surf_1.get_rect(center=(WINDOW_WIDTH // 2, 300))
            font_rect_2 = font_surf_2.get_rect(center=(WINDOW_WIDTH // 2, 500))
            font_rect_4 = font_surf_4.get_rect(center=(WINDOW_WIDTH // 2, 550))

            if self.scene_during < 5000:
                font_surf_1.set_alpha(int(self.scene_during / 1000 * 1))
                font_surf_2.set_alpha(int(self.scene_during / 1000 * 0.4))
                font_surf_4.set_alpha(int(self.scene_during / 1000 * 0.4))

            self.display_surface.blit(font_surf_1, font_rect_1)
            self.display_surface.blit(font_surf_2, font_rect_2)
            self.display_surface.blit(font_surf_4, font_rect_4)

        self.event_loop()
        return 1
