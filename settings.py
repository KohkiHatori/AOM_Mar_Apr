# Background colour
bg = (230, 230, 230)
# Mirror colour
grey = (128, 128, 128)
# Line colour
black = (0, 0, 0)
# Barrier colour
yellow = (255, 255, 0)
# Bullet colour
pink = (255, 51, 255)

# Player colours
green = (0,255,0)
red = (255, 0, 0)
blue = (0, 0, 255)
purple = (127, 0, 255)
orange = (255, 128, 0)
turqoise = (0 ,255, 255)



class Settings:
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_colour = bg

        self.stage_colour = black
        self.num_row = 9
        self.num_column = 16
        self.stage_top_left_x = 100
        self.stage_top_left_y = 150
        self.stage_bottom_right_x = self.screen_width - self.stage_top_left_x
        self.stage_bottom_right_y = self.screen_width - 50

        self.num_grid = self.num_row * self.num_column
        self.grid_width = 100
        self.grid_height = 100
        self.grid_line_width = 5

        self.num_barrier = self.num_grid // 10
        self.barrier_colour = yellow
        self.barrier_minimum_length = 1
        self.barrier_maximum_length = 3

        self.num_mirror = 5
        self.mirror_width = 10
        self.mirror_colour = grey

        self.num_player = 6
        self.player_colours = [green, red, blue, purple, orange, turqoise]

        self.num_shots = 5
        self.bullet_colour = pink
        self.bullet_width = 10
        self.bullet_height = 10


