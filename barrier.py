import pygame
import random
import copy
import itertools


class Barriers:

    def __init__(self, main):
        self.screen = main.screen
        self.settings = main.settings
        self.colour = self.settings.barrier_colour
        self.num = self.settings.num_barrier
        self.grids = main.stage.grids
        self.grid_height = self.settings.grid_height
        self.grid_width = self.settings.grid_width
        self.starting_y = main.stage.starting_y + self.grid_height
        self.starting_x = main.stage.starting_x + self.grid_width
        self.minimum_length = self.settings.barrier_minimum_length

    def create_barriers(self):
        self.barrier_allowed_grids = self.grids.copy()
        for i in range(len(self.barrier_allowed_grids)):
            self.barrier_allowed_grids[i] = self.barrier_allowed_grids[i].inflate(-15, -15)
        self.barrier_allowed_grids = [self.barrier_allowed_grids[x:x + self.settings.num_column] for x in
                                      range(0, len(self.barrier_allowed_grids), self.settings.num_column)]
        self.no_barrier_grids = copy.deepcopy(self.barrier_allowed_grids)
        self.barrier_grids = []
        for i in range(self.num):
            is_vertical = bool(random.getrandbits(1))
            length = random.randint(self.minimum_length, self.settings.barrier_maximum_length)
            if is_vertical:
                valid = False
                while not valid:
                    start_row_options = [row for row in range(0, self.settings.num_row - length + 1)]
                    start_column_options = [column for column in range(0, self.settings.num_column)]
                    random.shuffle(start_row_options)
                    random.shuffle(start_column_options)
                    for column, row in itertools.product(start_column_options, start_row_options):
                        start_column = column
                        start_row = row
                        list_boolean = []
                        for n in range(start_row, start_row + length):
                            there_is_no_barrier = self.barrier_allowed_grids[n][start_column] != 0
                            if there_is_no_barrier:
                                list_boolean.append(there_is_no_barrier)
                            else:
                                list_boolean.append(there_is_no_barrier)
                                break
                        if all(list_boolean):
                            valid = True
                            break
                    else:
                        continue
                    break

                for n in range(start_row, start_row + length):
                    self.barrier_grids.append(self.barrier_allowed_grids[n][start_column])
                    self.no_barrier_grids[n][start_column] = 0
                for m in range(-1, 2, 1):
                    if 0 <= start_column + m < self.settings.num_column:
                        for n in range(start_row if start_row == 0 else start_row - 1,
                                       start_row + length if start_row + length
                                                             == self.settings.
                                                                     num_row
                                       else start_row + length + 1):
                            self.barrier_allowed_grids[n][start_column + m] = 0
            else:
                valid = False
                while not valid:
                    start_column_options = [column for column in range(0, self.settings.num_column - length + 1)]
                    start_row_options = [row for row in range(0, self.settings.num_row)]
                    random.shuffle(start_column_options)
                    random.shuffle(start_row_options)
                    for row, column in itertools.product(start_row_options, start_column_options):
                        start_column = column
                        start_row = row
                        list_boolean = []
                        for n in range(start_column, start_column + length):
                            there_is_no_barrier = self.barrier_allowed_grids[start_row][n] != 0
                            if there_is_no_barrier:
                                list_boolean.append(there_is_no_barrier)
                            else:
                                list_boolean.append(there_is_no_barrier)
                                break
                        if all(list_boolean):
                            valid = True
                            break
                    else:
                        continue
                    break

                for n in range(start_column, start_column + length):
                    self.barrier_grids.append(self.barrier_allowed_grids[start_row][n])
                    self.no_barrier_grids[start_row][n] = 0
                for m in range(-1, 2, 1):
                    if 0 <= start_row + m < self.settings.num_row:
                        for n in range(start_column if start_column == 0 else start_column - 1, start_column + length if
                        start_column + length == self.settings.num_column else start_column + length + 1):
                            self.barrier_allowed_grids[start_row + m][n] = 0

        self.no_barrier_grids = [item for sublist in self.no_barrier_grids for item in sublist]
        self.no_barrier_grids = [item for item in self.no_barrier_grids if item != 0]
        for item in self.no_barrier_grids:
            self.no_barrier_grids[self.no_barrier_grids.index(item)] = item.inflate(15, 15)

    def draw_barriers(self):
        for grid in self.barrier_grids:
            pygame.draw.rect(self.screen, self.colour, grid)
