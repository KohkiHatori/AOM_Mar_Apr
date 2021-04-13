import pygame


class Stage():

    def __init__(self, main):
        self.screen = main.screen
        self.settings = main.settings
        self.colour = self.settings.stage_colour
        self.centre_screen = main.centre_screen
        self.starting_y = main.starting_y
        self.starting_x = main.starting_x
        self.rect = pygame.Rect(0, 0, 100, 100)

    def draw_stage(self):
        y = self.starting_y
        x = self.starting_x
        for row in range(0, self.settings.num_row):
            for column in range(0, self.settings.num_column):
                pygame.draw.lines(self.screen, self.settings.stage_colour, True,
                                  ((x, y), (x + 100, y), (x + 100, y + 100), (x, y + 100)), width=5)
                x += 100
            y += 100
            x = self.starting_x

