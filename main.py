import sys
import pygame
import random
import time
import math
from settings import Settings
from stage import Stage
from barrier import Barriers
from mirror import Mirrors
from player import Player
from text import Text
from stats import Stats
from button import Button
from bullet import Bullet

def run_once(func):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return func(*args, **kwargs)

    wrapper.has_run = False
    return wrapper


class Main:

    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        self.settings.grid_width = (self.settings.screen_width - 200) // self.settings.num_column
        self.settings.grid_height = (self.settings.screen_height - 200) // self.settings.num_row
        pygame.display.set_caption("Kohki Hatori")
        self.stage = Stage(self)
        self.barriers = Barriers(self)
        self.mirrors = Mirrors(self)
        self.players = []
        self.text = Text(self)
        self.stats = Stats()
        self.start_button = Button(self, "START")
        self._create_environment()
        self.constructing = True
        self.bullets = pygame.sprite.Group()


    def run_game(self):
        while True:
            self._check_events()
            if self.stats.active:
                pass
            self._update_screen()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_start_button(mouse_pos)

    def _check_keydown_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                sys.exit()

    def _check_start_button(self, mouse_pos):
        if self.start_button.rect.collidepoint(mouse_pos):
            self.stats.active = True
            self.timer = time.time()

    def _create_environment(self):
        self.stage.create_stage()
        self.barriers.create_barriers()
        self.mirrors.create_mirrors()
        self._create_players()

    def _create_players(self):
        indices = []
        for x in range(len(self.barriers.no_barrier_grids)):
            indices.append(x)
        for i in range(self.settings.num_player):
            new_player = Player(self)
            new_player.position = random.choice(indices)
            new_player.colour = self.settings.player_colours[i]
            self.players.append(new_player)
            indices.remove(new_player.position)

    def _draw_players(self):
        for player in self.players:
            player.blitme(player_allowed_grids=self.barriers.no_barrier_grids)

    def observable(self, observer):
        self.observable_players = []
        other_players = self.players.copy()
        other_players.remove(observer)
        observer_x = observer.rect.centerx
        observer_y = observer.rect.centery

        def checker(x, y, x_, y_, li):
            for x in range(x, x_, -1 if x_ < x else 1):
                for y in range(y, y_, -1 if y_ < y else 1):
                    for i in li:
                        if i.collidepoint(x, y):
                            return False
            return True

        for player in other_players:
            searching_x = player.rect.centerx
            searching_y = player.rect.centery
            if checker(observer_x, observer_y, searching_x, searching_y, self.barriers.barrier_grids):
                self.observable_players.append(player)

        return self.observable_players


    @run_once
    def _cheat(self):
        cheater = self.players[random.randint(0, self.settings.num_player - 1)]
        observable_players = self.observable(cheater)
        if len(observable_players) > 0:
            self._create_bullet(cheater, random.choice(observable_players))
        else:
            self._create_bullet(cheater, 0)

    def _create_bullet(self, shooter, target):
        x, y = shooter.rect.centerx, shooter.rect.centery
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)
        new_bullet.x, new_bullet.y = x, y
        if target != 0:
            x_, y_ = target.rect.centerx, target.rect.centery
            if x_ - x != 0:
                gradient = (y_ - y) / (x_ - x)
                new_bullet.x_change_rate = 1 if x_ - x > 0 else -1
                new_bullet.y_change_rate = gradient if x_ -x > 0 else - gradient
            else:
                new_bullet.x_change_rate = 0
                new_bullet.y_change_rate = 1 if y_ > y else -1
        else:
            # angle = random.randint(0.360)
            angle = 90
            if angle != 90 or 270:
                gradient = math.tan(angle)
                new_bullet.x_change_rate = 1 if 0 <= angle < 90 or 270 < angle <= 360 else -1
                new_bullet.y_change_rate = gradient if 0 <= angle < 90 or 270 < angle <= 360 else -gradient
            else:
                new_bullet.x_change_rate = 0
                new_bullet.y_change_rate = 1 if angle == 90 else -1


    def _update_bullet(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0 or bullet.rect.right <= 0 or bullet.rect.left >= self.settings.screen_width or \
                    bullet.rect.top >= self.settings.screen_height:
                self.bullets.remove(bullet)

    def _check_bullet_collisions(self):
        barrier_coll = pygame.rect.colliderect()
        mirror_coll = pygame.rect.colliderect()
        player_coll = pygame.rect.colliderect()


    def _update_screen(self):
        self.screen.fill(self.settings.bg_colour)
        if self.stats.active:
            if self.constructing:
                if time.time() > self.timer + 1:
                    self.stage.draw_stage()
                if time.time() > self.timer + 2:
                    self.barriers.draw_barriers()
                if time.time() > self.timer + 3:
                    self.mirrors.draw_mirrors()
                if time.time() > self.timer + 4:
                    self._draw_players()
                if time.time() > self.timer + 8:
                    self.constructing = False
            else:
                self.stage.draw_stage()
                self.barriers.draw_barriers()
                self.mirrors.draw_mirrors()
                self._draw_players()
                self._cheat()
                for bullet in self.bullets.sprites():
                    bullet.draw_bullet()
                self._update_bullet()
        if not self.stats.active:
            self.start_button.draw_button()
        pygame.display.flip()


if __name__ == "__main__":
    mygame = Main()
    mygame.run_game()
