import pygame, sys
from settings import *

class Main:
    def __init__(self):
        # Game window setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.title = pygame.display.set_caption(TITLE)
        self.icon = pygame.display.set_icon(pygame.image.load(ICON_PATH).convert_alpha())


        # Stages
        self.stage = 1

        # Font
        self.font = pygame.font.Font(FONT_PATH_2, 50)

    def author_stage(self, current_time):

        sys_font = pygame.font.SysFont('arial', 32)
        if current_time >= AUTHOR_TIME:
            self.stage = 2
        else:
            font_surf_1 = self.font.render(TITLE, True, 'white')
            font_surf_2 = sys_font.render(GIT_HUB, True, 'white')
            font_surf_3 = sys_font.render(E_MAIL, True, 'white')
            font_surf_4 = sys_font.render(TELEGRAM, True, 'white')

            font_rect_1 = font_surf_1.get_rect(center=(WINDOW_WIDTH // 2, 300))
            font_rect_2 = font_surf_2.get_rect(center=(WINDOW_WIDTH // 2, 500))
            font_rect_3 = font_surf_3.get_rect(center=(WINDOW_WIDTH // 2, 550))
            font_rect_4 = font_surf_4.get_rect(center=(WINDOW_WIDTH // 2, 600))

            if current_time < 3000:
                font_surf_1.set_alpha(int(current_time / 1000 * 1))
                font_surf_2.set_alpha(int(current_time / 1000 * 0.4))
                font_surf_3.set_alpha(int(current_time / 1000 * 0.4))
                font_surf_4.set_alpha(int(current_time / 1000 * 0.4))
            
            self.display_surface.blit(font_surf_1, font_rect_1)
            self.display_surface.blit(font_surf_2, font_rect_2)
            self.display_surface.blit(font_surf_3, font_rect_3)
            self.display_surface.blit(font_surf_4, font_rect_4)

    def lang_chosen_stage(self):
        print('stage 2')

    def run(self):
        self.display_surface.fill(BLACK_GRAY)
        while True:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                    self.stage = 2
            
            current_time = pygame.time.get_ticks()
            if self.stage == 1:
                self.author_stage(current_time)
            elif self.stage == 2:
                self.lang_chosen_stage()


            pygame.display.update()

if __name__ == '__main__':
    main = Main()
    main.run()