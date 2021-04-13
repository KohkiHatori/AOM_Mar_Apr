import pygame


class Stage:

    def __init__(self, main):
        self.screen = main.screen
        self.settings = main.settings
        self.colour = self.settings.stage_colour
        self.centre_screen = (self.settings.screen_width / 2, self.settings.screen_height / 2)
        self.starting_y = self.centre_screen[1] - self.settings.num_row / 2 * 100
        self.starting_x = self.centre_screen[0] - self.settings.num_column / 2 * 100
        self.grids = []

    def create_stage(self):
        y = self.starting_y
        x = self.starting_x
        for row in range(0, self.settings.num_row):
            for column in range(0, self.settings.num_column):
                new_grid = pygame.Rect(x, y, self.settings.grid_width, self.settings.grid_height)
                self.grids.append(new_grid)
                x += 100
            y += 100
            x = self.starting_x

    def draw_stage(self):
        for grid in self.grids:
            pygame.draw.lines(self.screen, self.settings.stage_colour, True,
                              (grid.topleft, grid.topright, grid.bottomright, grid.bottomleft),
                              width=5)

