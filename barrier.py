import pygame
import random


class Barriers:

    def __init__(self, main):
        self.screen = main.screen
        self.settings = main.settings
        self.stage_grids = main.stage.grids
        self.colour = self.settings.barrier_colour
        self.grid_height = self.settings.grid_height
        self.grid_width = self.settings.grid_width
        self.starting_y = main.stage.starting_y + self.grid_height
        self.starting_x = main.stage.starting_x + self.grid_width

    def create_barriers(self):
        self.barrier_allowed_grids = []
        y = self.starting_y
        x = self.starting_x
        for row in range(self.settings.num_row - 2):
            for column in range(self.settings.num_column - 2):
                new_grid = pygame.Rect(x, y, self.grid_width, self.grid_height)
                self.barrier_allowed_grids.append(new_grid)
                x += self.grid_width
            y += self.grid_height
            x = self.starting_x
        self.barrier_grids = (random.sample(self.barrier_allowed_grids, self.settings.num_barrier))

    def draw_barriers(self):
        for grid in self.barrier_grids:
            obj = grid
            obj = obj.inflate(-10, -10)
            pygame.draw.rect(self.screen, self.colour, obj)

