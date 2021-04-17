import pygame


class Stage:

    def __init__(self, main):
        self.screen = main.screen
        self.settings = main.settings
        self.screen_width, self.screen_height = self.screen.get_size()
        self.colour = self.settings.stage_colour
        self.grid_width = self.settings.grid_width
        self.grid_height = self.settings.grid_height
        self.starting_y = 150
        self.starting_x = 100
        self.grids = []
        self.width = self.settings.grid_line_width

    def create_stage(self):
        y = self.starting_y
        x = self.starting_x
        for row in range(self.settings.num_row):
            for column in range(self.settings.num_column):
                new_grid = pygame.Rect(x, y, self.grid_width, self.grid_height)
                self.grids.append(new_grid)
                x += self.grid_width
            y += self.grid_height
            x = self.starting_x

    def draw_stage(self):
        for grid in self.grids:
            pygame.draw.rect(self.screen, self.settings.stage_colour, grid, self.width)


