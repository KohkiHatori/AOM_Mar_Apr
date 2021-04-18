import pygame


class Bullet:

    def __init__(self, main):
        self.screen = main.screen
        self.settings = main.settings
        self.colour = self.settings.bullet_colour
        self.rect = pygame.Rect(0,0, self.settings.bullet_width, self.settings.bullet_height)
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.x_change_rate = 1
        self.y_change_rate = 1

    def update(self):
        self.x += self.x_change_rate
        self.y += self.y_change_rate
        self.rect.x = self.x
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.colour, self.rect, border_radius=4)