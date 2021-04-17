import sys
import pygame
import random
import time
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
        self.start_button = Button(self, "START")
        self._create_environment()
        self.constructing = True

    def run_game(self):
        while True:
            self._check_events()
            if self.stats.active:
                pass
            self._update_screen()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_start_button(mouse_pos)

    def _check_keydown_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                sys.exit()

    def _check_start_button(self, mouse_pos):
        if self.start_button.rect.collidepoint(mouse_pos):
            self.stats.active = True
            self.timer = time.time()

    def _create_environment(self):
        self.stage.create_stage()
        self.barriers.create_barriers()
        self.mirrors.create_mirrors()
        self._create_players()

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
        if self.stats.active:
            if self.constructing:
                if time.time() > self.timer + 1:
                    self.stage.draw_stage()
                if time.time() > self.timer + 2:
                    self.barriers.draw_barriers()
                if time.time() > self.timer + 3:
                    self.mirrors.draw_mirrors()
                if time.time() > self.timer + 4:
                    self._draw_players()
                if time.time() > self.timer + 8:
                    self.constructing = False
            if not self.constructing:
                self.stage.draw_stage()
                self.barriers.draw_barriers()
                self.mirrors.draw_mirrors()
                self._draw_players()
        if not self.stats.active:
            self.start_button.draw_button()
        pygame.display.flip()


if __name__ == "__main__":
    mygame = Main()
    mygame.run_game()
