import pygame
import random


class Mirrors:

    def __init__(self, main):
        self.screen = main.screen
        self.settings = main.settings
        self.colour = self.settings.mirror_colour
        self.num = self.settings.num_mirror
        self.grid_width = self.settings.grid_width
        self.grid_height = self.settings.grid_height
        self.starting_x = main.stage.starting_x
        self.starting_y = main.stage.starting_y
        self.mirror_width = self.settings.mirror_width

    def create_mirrors(self):
        self.mirror_vertical_one = []
        self.mirror_vertical_two = []
        self.mirror_horizontal_one = []
        self.mirror_horizontal_two = []
        self.mirror_grids = []
        self.mirror_allowed_grids = [self.mirror_horizontal_one, self.mirror_horizontal_two, self.mirror_vertical_one,
                                     self.mirror_vertical_two]
        x = self.starting_x + self.grid_width
        y = self.starting_y - self.mirror_width
        for column in range(self.settings.num_column - 2):
            new_grid = pygame.Rect(x, y, self.grid_width, self.mirror_width)
            self.mirror_horizontal_one.append(new_grid)
            x += self.grid_width
        x = self.starting_x + self.grid_width
        y = self.starting_y + self.settings.grid_height * self.settings.num_row
        for column in range(self.settings.num_column - 2):
            new_grid = pygame.Rect(x, y, self.grid_width, self.mirror_width)
            self.mirror_horizontal_two.append(new_grid)
            x += self.grid_width
        x = self.starting_x - self.mirror_width
        y = self.starting_y + self.grid_height
        for row in range(self.settings.num_row - 2):
            new_grid = pygame.Rect(x, y, self.mirror_width, self.grid_height)
            self.mirror_vertical_one.append(new_grid)
            y += self.grid_height
        x = self.starting_x + self.grid_width * self.settings.num_column
        y = self.starting_y + self.grid_height
        for row in range(self.settings.num_row - 2):
            new_grid = pygame.Rect(x, y, self.mirror_width, self.grid_height)
            self.mirror_vertical_two.append(new_grid)
            y += self.grid_height

        for ind in range(4):

            limit = len(self.mirror_allowed_grids[ind])
            length = random.randint(1, limit)
            start = random.randint(0, limit - length)
            for n in range(start, start + length):
                self.mirror_grids.append(self.mirror_allowed_grids[ind][n])
            del self.mirror_allowed_grids[ind][start if start == 0 else start - 1: start + length if start + length >
                                                                                                     limit else start + length + 1]
        for i in range(self.num - 4):
            space_available = True
            valid = False
            while not valid:
                ind = random.randint(0,3)
                h_o_emp = len(self.mirror_horizontal_one) == 0
                h_t_emp = len(self.mirror_horizontal_two) == 0
                v_o_emp = len(self.mirror_vertical_one) == 0
                v_t_emp = len(self.mirror_vertical_two) == 0
                if len(self.mirror_allowed_grids[ind]) != 0:
                    valid = True
                elif h_o_emp and h_t_emp and v_o_emp and v_t_emp:
                    space_available = False
                    valid = True

            if space_available:
                limit = len(self.mirror_allowed_grids[ind])
                length = random.randint(1, limit)
                start = random.randint(0, limit - length)
                for n in range(start, start + length):
                    self.mirror_grids.append(self.mirror_allowed_grids[ind][n])
                del self.mirror_allowed_grids[ind][start if start == 0 else start - 1: start + length if start + length >
                                                                                                         limit else start + length + 1]

    def draw_mirrors(self):
        for grid in self.mirror_grids:
            pygame.draw.rect(self.screen, self.colour, grid)
