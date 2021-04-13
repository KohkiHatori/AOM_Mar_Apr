import sys
import pygame
from settings import Settings
from stage import Stage


class Main:

    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Kohki Hatori")
        self.centre_screen = (self.settings.screen_width / 2, self.settings.screen_height / 2)
        self.starting_y = self.centre_screen[1] - self.settings.num_row / 2 * 100
        self.starting_x = self.centre_screen[0] - self.settings.num_column / 2 * 100
        self.stage = Stage(self)

    def run_game(self):
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

    def _update_screen(self):
        self.screen.fill(self.settings.bg_colour)
        self.stage.draw_stage()
        pygame.display.flip()



if __name__ == "__main__":
    mygame = Main()
    mygame.run_game()