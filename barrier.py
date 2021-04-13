import pygame
import random


class Barriers:

    def __init__(self, main):
        self.screen = main.screen
        self.settings = main.settings
        self.stage_grids = main.stage.grids
        self.colour = self.settings.barrier_colour
        self.barrier_grids = []

    def create_barriers(self):
        for i in range(0, self.settings.num_barrier):
            self.barrier_grids.append(random.randint(0, len(self.stage_grids) - 1))

    def draw_barriers(self):
        for i in self.barrier_grids:
            obj = self.stage_grids[i]
            obj = obj.inflate(-10,-10)
            pygame.draw.rect(self.screen, self.colour, obj,width=0,)

