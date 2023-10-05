import sys


import pygame
from pygame.image import load


import eng
import rus
from settings import *


class Cutscene:
    """Renders cutscenes between the game's stages."""
    def __init__(self, current_stage,
                 next_stage, current_picture,
                 audio, config, transition):

        # main setup
        self.display_surface = pygame.display.get_surface()
        self.config = config

        # stages control
        self.current_stage = current_stage
        self.next_stage = next_stage
        self.show_transition = transition
        self.scene_during = 0

        # frames and pictures
        self.frame = load('images/cutscenes/frame.png').convert_alpha()
        self.frame_rect = self.frame.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        )
        self.current_picture = current_picture
        if self.current_picture is not None:
            self.current_picture_rect = self.current_picture.get_rect(
                center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
            )

        # audio
        self.is_audio_chosen = False
        self.audio = audio
        self.current_audio = None
        self.audio_duration = 0
        self.is_audio_duration_gotten = False
        self.is_audio_playing = False

        # fonts
        self.font = pygame.font.Font(FONT_PATH_2, 65)
        self.font_small = pygame.font.SysFont('arial', 40, True)

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def get_current_audio(self, current_lang):
        if isinstance(self.audio, tuple):
            if current_lang == 'rus':
                self.current_audio = self.audio[1]
            else:
                self.current_audio = self.audio[0]
        else:
            self.current_audio = self.audio
        self.is_audio_chosen = True

    def get_audio_duration(self):
        self.audio_duration = self.current_audio.get_length()
        self.is_audio_duration_gotten = True

    def run(self, dt, current_lang):
        if not self.is_audio_chosen:
            self.get_current_audio(current_lang)
        if not self.is_audio_duration_gotten:
            self.get_audio_duration()
        self.scene_during += dt

        if self.scene_during >= self.audio_duration:
            self.scene_during = 0
            pygame.mouse.set_visible(True)
            self.is_audio_playing = False
            self.show_transition()
            return self.next_stage
        else:
            pygame.mouse.set_visible(False)
            if not self.is_audio_playing:
                self.current_audio.set_volume(
                    float(self.config['SOUNDS']['music'])
                )
                self.current_audio.play()
                self.is_audio_playing = True

            if self.current_stage == 'GAME_OVER':
                if current_lang == 'eng':
                    self.font_surf = self.font.render(
                        eng.GAME_OVER, True, 'yellow'
                    )
                    self.font_rect = self.font_surf.get_rect(
                        centerx=WINDOW_WIDTH // 2,
                        centery=WINDOW_HEIGHT // 2
                    )
                else:
                    self.font_surf = self.font_small.render(
                        rus.GAME_OVER, True, 'yellow'
                    )
                    self.font_rect = self.font_surf.get_rect(
                        centerx=WINDOW_WIDTH // 2,
                        centery=WINDOW_HEIGHT // 2
                    )
                self.display_surface.fill(BLACK_GRAY)
                self.display_surface.blit(self.font_surf, self.font_rect)
            elif self.current_stage == 'END':
                self.the_end_surf = self.font.render(
                    eng.THE_END, True, 'yellow'
                )
                self.the_end_rect = self.the_end_surf.get_rect(
                    center=(WINDOW_WIDTH // 2, 200)
                )
                self.programmer_surf = self.font_small.render(
                    eng.PROGRAMMER if current_lang == 'eng'
                    else rus.PROGRAMMER, True, 'yellow'
                )
                self.programmer_rect = self.programmer_surf.get_rect(
                    center=(WINDOW_WIDTH // 2, 300)
                )
                self.graphics_surf = self.font_small.render(
                    eng.GRAPHICS if current_lang == 'eng'
                    else rus.GRAPHICS, True, 'yellow'
                )
                self.graphics_rect = self.graphics_surf.get_rect(
                    center=(WINDOW_WIDTH // 2, 350)
                )
                self.music_surf = self.font_small.render(
                    eng.MUSIC if current_lang == 'eng'
                    else rus.MUSIC, True, 'yellow'
                )
                self.music_rect = self.music_surf.get_rect(
                    center=(WINDOW_WIDTH // 2, 400)
                )
                self.sounds_surf = self.font_small.render(
                    eng.SOUNDS if current_lang == 'eng'
                    else rus.SOUNDS, True, 'yellow'
                )
                self.sounds_rect = self.sounds_surf.get_rect(
                    center=(WINDOW_WIDTH // 2, 450)
                )
                self.thanks_surf = self.font_small.render(
                    eng.THANKS if current_lang == 'eng'
                    else rus.THANKS, True, 'yellow'
                )
                self.thanks_rect = self.thanks_surf.get_rect(
                    center=(WINDOW_WIDTH // 2, 550)
                )
                self.christian_surf = self.font_small.render(
                    eng.CHRISTIAN_KOCH if current_lang == 'eng'
                    else rus.CHRISTIAN_KOCH, True, 'yellow'
                )
                self.christian_rect = self.christian_surf.get_rect(
                    center=(WINDOW_WIDTH // 2, 600)
                )
                self.sergey_surf = self.font_small.render(
                    eng.SERGEY_BALAKIREV if current_lang == 'eng'
                    else rus.SERGEY_BALAKIREV, True, 'yellow'
                )
                self.sergey_rect = self.sergey_surf.get_rect(
                    center=(WINDOW_WIDTH // 2, 650)
                )
                self.display_surface.fill(BLACK_GRAY)
                self.display_surface.blit(self.the_end_surf, self.the_end_rect)
                self.display_surface.blit(
                    self.programmer_surf, self.programmer_rect
                )
                self.display_surface.blit(
                    self.graphics_surf, self.graphics_rect
                )
                self.display_surface.blit(self.music_surf, self.music_rect)
                self.display_surface.blit(self.sounds_surf, self.sounds_rect)
                self.display_surface.blit(self.thanks_surf, self.thanks_rect)
                self.display_surface.blit(
                    self.christian_surf, self.christian_rect
                )
                self.display_surface.blit(self.sergey_surf, self.sergey_rect)
            else:
                self.display_surface.fill(BLACK_GRAY)
                self.display_surface.blit(self.frame, self.frame_rect)
                self.display_surface.blit(
                    self.current_picture, self.current_picture_rect
                )

        self.event_loop()
        return self.current_stage
