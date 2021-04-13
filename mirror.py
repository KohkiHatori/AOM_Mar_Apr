import pygame
import random


class Mirrors:

    def __init__(self, main):
        self.screen = main.screen
        self.settings = main.settings
        self.colour = self.settings.mirror_colour
        self.starting_x = main.stage.starting_x
        self.starting_y = main.stage.starting_y
        self.grid_width = self.settings.grid_width
        self.grid_height = self.settings.grid_height
        self.mirror_width = self.settings.mirror_width

    def create_mirrors(self):
        self.mirror_allowed_grids = []
        x = self.starting_x
        y = self.starting_y - self.mirror_width
        for row in range(2):
            for column in range(self.settings.num_column):
                new_grid = pygame.Rect(x, y, self.grid_width, self.mirror_width)
                self.mirror_allowed_grids.append(new_grid)
                x += self.grid_width
            y += self.settings.grid_height * self.settings.num_row + self.mirror_width
            x = self.starting_x
        x = self.starting_x - self.mirror_width
        y = self.starting_y
        for row in range(self.settings.num_row):
            for column in range(2):
                new_grid = pygame.Rect(x, y, self.mirror_width, self.grid_height)
                self.mirror_allowed_grids.append(new_grid)
                x += self.grid_width * self.settings.num_column + self.mirror_width
            y += self.grid_height
            x = self.starting_x - self.mirror_width
        self.mirror_grids = []

    def draw_mirrors(self):
        for grid in self.mirror_allowed_grids:
            obj = grid
            pygame.draw.rect(self.screen, self.colour, obj)
