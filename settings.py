bg = (230, 230, 230)
grey = (128, 128, 128)
black = (0, 0, 0)
yellow = (255, 255, 0)

# Player colours
green = (0,255,0)
red = (255, 0, 0)
blue = (0, 0, 255)
purple = (127, 0, 255)


class Settings:
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_colour = bg

        self.stage_colour = black
        self.num_row = 9
        self.num_column = 16

        self.num_grid = self.num_row * self.num_column
        self.grid_width = 100
        self.grid_height = 100
        self.grid_line_width = 5

        self.num_barrier = self.num_grid // 10
        self.barrier_colour = yellow
        self.barrier_minimum_length = 2
        self.barrier_maximum_length = 3

        self.num_mirror = 5
        self.mirror_width = 10
        self.mirror_colour = grey

        self.num_player = 4
        self.player_colours = [green, red, blue, purple]
        self.num_shots = 5
