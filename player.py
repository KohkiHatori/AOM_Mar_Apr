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
        self.position = 0
        self.colour = 0
        self.width = self.settings.grid_line_width

    def blitme(self, player_allowed_grids):
        self.rect.center = player_allowed_grids[self.position].center
        self.screen.blit(self.image, self.rect)
        pygame.draw.rect(self.screen, self.colour, player_allowed_grids[self.position], width=self.width)
