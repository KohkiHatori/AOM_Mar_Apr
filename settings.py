class Settings:
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_colour = (230, 230, 230)
        self.stage_colour = (0,0,0)
        self.num_row = 8
        self.num_column = 10
        self.num_grid = self.num_row * self.num_column
        self.grid_width = 100
        self.grid_height = 100
        self.num_barrier = self.num_grid // 10
        self.barrier_colour = (255,255,0)
        self.num_mirror = 4
        self.num_player = 4
        self.num_shots = 5



