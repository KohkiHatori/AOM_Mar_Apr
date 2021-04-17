import pygame
from pygame.sprite import Sprite


class Players(Sprite):

    def __init__(self, main):
        super().__init__()
        self.screen = main.screen
        self.settings = main.settings
        self.stage = main.stage
        self.num = self.settings.num_player
        self.image = pygame.image.load("images/player.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (self.settings.grid_width - 10, self.settings.grid_height - 10))
        self.rect = self.image.get_rect()


    def blitme(self):
        self.rect.center = self.stage.grids[0].center
        self.screen.blit(self.image, self.rect)
