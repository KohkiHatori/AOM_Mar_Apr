import sys
import pygame
import random
from time import sleep
from settings import Settings
from stage import Stage
from barrier import Barriers
from mirror import Mirrors
from player import Player
from text import Text
from stats import Stats
from button import Button


class Main:

    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        self.settings.grid_width = (self.settings.screen_width - 200) // self.settings.num_column
        self.settings.grid_height = (self.settings.screen_height - 200) // self.settings.num_row
        pygame.display.set_caption("Kohki Hatori")
        self.stage = Stage(self)
        self.barriers = Barriers(self)
        self.mirrors = Mirrors(self)
        self.players = []
        self.text = Text(self)
        self.stats = Stats()
        self.start_button = Button("START")

    def run_game(self):

        self._create_environment()
        while True:
            if self.stats.active:
                pass
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
        sleep(2)
        self.barriers.create_barriers()
        sleep(2)
        self.mirrors.create_mirrors()
        sleep(2)
        self._create_players()
        sleep(2)

    def _create_players(self):
        indices = []
        for x in range(len(self.barriers.no_barrier_grids)):
            indices.append(x)
        for i in range(self.settings.num_player):
            new_player = Player(self)
            new_player.position = random.choice(indices)
            new_player.colour = self.settings.player_colours[i]
            self.players.append(new_player)
            indices.remove(new_player.position)


    def _draw_players(self):
        for player in self.players:
            player.blitme(player_allowed_grids=self.barriers.no_barrier_grids)


    def _update_screen(self):
        self.screen.fill(self.settings.bg_colour)
        self.stage.draw_stage()
        self.barriers.draw_barriers()
        self.mirrors.draw_mirrors()
        self._draw_players()
        pygame.display.flip()


if __name__ == "__main__":
    mygame = Main()
    mygame.run_game()
