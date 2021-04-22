import pygame


class Player:
    def __init__(self, main):
        super().__init__()
        self.screen = main.screen
        self.settings = main.settings
        self.stage = main.stage
        self.num = self.settings.num_player
        self.image = pygame.image.load("images/player.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (self.settings.grid_width - 10, self.settings.grid_height - 10))
        self.rect = self.image.get_rect()
        self.colour = 0
        self.line_width = self.settings.grid_line_width
        self.shot_left = self.settings.num_shots
        self.original_index = 0

    def blitme(self):
        self.screen.blit(self.image, self.rect)
        pygame.draw.rect(self.screen, self.colour, self.rect, width=self.line_width)
