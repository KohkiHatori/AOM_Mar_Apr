import sys
import pygame
from settings import Settings
from stage import Stage
from barrier import Barriers


class Main:

    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Kohki Hatori")
        self.stage = Stage(self)
        self.barriers = Barriers(self)


    def run_game(self):
        self._create_environment()
        while True:
            self._check_events()
            self._update_screen()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

    def _check_keydown_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                sys.exit()

    def _create_environment(self):
        self.stage.create_stage()
        self.barriers.create_barriers()

    def _update_screen(self):
        self.screen.fill(self.settings.bg_colour)
        self.stage.draw_stage()
        self.barriers.draw_barriers()
        pygame.display.flip()


if __name__ == "__main__":
    mygame = Main()
    mygame.run_game()
