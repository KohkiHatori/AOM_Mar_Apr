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
        self.stats = Stats(self)
        self.start_button = Button(self, "START")
        self._create_environment()
        self.constructing = True
        self.cheating = False
        self.real_game = False
        self.bullets = []
        self.turn_ended = True
        self.shooter = 0

    def run_game(self):
        while True:
            self._check_events()
            if self.real_game:
                self._real_game()
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
        if not self.stats.game_active:
            if self.start_button.rect.collidepoint(mouse_pos):
                self.stats.game_active = True
                self.constructing = True
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

    def _observable(self, observer):
        observable_players = []
        other_players = self.players.copy()
        other_players.remove(observer)
        observer_x = observer.rect.centerx
        observer_y = observer.rect.centery

        def _collision(x, x_, y, y_, li):
            if x != x_:
                gradient = (y_ - y) / (x_ - x)
                y_axis_intersect = y - gradient * x
                for x in range(x, x_, -1 if x_ < x else 1):
                    y = gradient * x + y_axis_intersect
                    for i in li:
                        if i.collidepoint(x, y):
                            return True
                return False
            else:
                for y in range(y, y_, -1 if y_ < y else 1):
                    for i in li:
                        if i.collidepoint(x, y):
                            return True
                return False

        for player in other_players:
            searching_x = player.rect.centerx
            searching_y = player.rect.centery
            if not _collision(observer_x, searching_x, observer_y, searching_y, self.barriers.barrier_grids):
                observable_players.append(player)

        return observable_players

    @run_once
    def _cheat(self):
        cheater = self.players[random.randint(0, self.settings.num_player - 1)]
        observable_players = self._observable(cheater)
        if len(observable_players) > 0:
            self._create_bullet(cheater, random.choice(observable_players))
        else:
            self._create_bullet(cheater, 0)

    @run_once
    def _remove_cheater_start_real_game(self, cheater):
        self.players.remove(cheater)
        self.cheating = False
        self.real_game = True

    def _create_bullet(self, shooter, target):
        x, y = shooter.rect.centerx, shooter.rect.centery
        new_bullet = Bullet(self)
        new_bullet.shooter = shooter
        self.bullets.append(new_bullet)
        new_bullet.x, new_bullet.y = x, y
        if target != 0:
            x_, y_ = target.rect.centerx, target.rect.centery
            if x_ - x != 0:
                change_in_y = y_ - y
                change_in_x = x_ - x
                route_length = math.sqrt(change_in_y ** 2 + change_in_x ** 2)
                gradient = change_in_y / change_in_x
                num_loop = route_length / self.settings.bullet_speed
                new_bullet.x_change_rate = change_in_x / num_loop
                new_bullet.y_change_rate = new_bullet.x_change_rate * gradient
            else:
                new_bullet.x_change_rate = 0
                new_bullet.y_change_rate = self.settings.bullet_speed if y_ > y else -self.settings.bullet_speed
        else:
            # angle = random.randint(0, 360)
            angle = 90
            if angle == 90 or angle == 270:
                if angle == 90:
                    y_ = 0
                else:
                    y_ = self.screen.get_height()
                change_in_y = y_ - y
                route_length = abs(change_in_y)
                num_loop = route_length / self.settings.bullet_speed
                new_bullet.x_change_rate = 0
                new_bullet.y_change_rate = change_in_y / num_loop
            else:
                gradient = -round(math.tan(math.radians(angle)), 5)
                y_axis_intersect = y - gradient * x
                width = self.screen.get_width()
                height = self.screen.get_height()
                if 0 < angle < 180:
                    x_at_zero = -y_axis_intersect / gradient
                    x_at_maximum = (height - y_axis_intersect) / gradient
                    if 0 <= x_at_zero <= width:
                        x_ = x_at_zero
                        y_ = 0
                    else:
                        x_ = width if 0 < angle < 90 else 0
                        y_ = gradient * width + y_axis_intersect if 0 < angle < 90 else y_axis_intersect
                elif 180 < angle < 360:
                    x_at_zero = -y_axis_intersect / gradient
                    x_at_maximum = (height - y_axis_intersect) / gradient
                    if 0 <= x_at_maximum <= width:
                        x_ = x_at_maximum
                        y_ = height
                    else:
                        x_ = 0 if 180 < angle < 270 else width
                        y_ = y_axis_intersect if 180 < angle < 270 else gradient * width + y_axis_intersect
                else:
                    #     when angle is 0, 180 or 360
                    if angle == 0 or angle == 360:
                        x_ = width
                        y_ = y_axis_intersect
                    else:
                        x_ = 0
                        y_ = y_axis_intersect

                change_in_y = y_ - y
                change_in_x = x_ - x
                route_length = math.sqrt(change_in_y ** 2 + change_in_x ** 2)
                num_loop = route_length / self.settings.bullet_speed
                new_bullet.x_change_rate = change_in_x / num_loop
                new_bullet.y_change_rate = new_bullet.x_change_rate * gradient


    def _update_bullet(self):
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0 or bullet.rect.right <= 0 or bullet.rect.left >= self.settings.screen_width or \
                    bullet.rect.top >= self.settings.screen_height:
                self.bullets.remove(bullet)
                time.sleep(0.5)
                self._remove_cheater_start_real_game(bullet.shooter)
            bullet.update()
            self._check_bullet_barrier_collisions(bullet)
            self._check_bullet_player_collisions(bullet)
            self._check_bullet_mirror_collisions(bullet)

    def _check_bullet_barrier_collisions(self, bullet):
        for barrier in self.barriers.barrier_grids:
            collision = pygame.Rect.colliderect(bullet.rect, barrier)
            if collision:
                self.bullets.remove(bullet)
                time.sleep(0.5)
                self._remove_cheater_start_real_game(bullet.shooter)
                break

    def _check_bullet_player_collisions(self, bullet):
        players_copy = self.players.copy()
        try:
            players_copy.remove(bullet.shooter)
        except:
            pass
        for player in players_copy:
            collision = pygame.Rect.colliderect(bullet.rect, player.rect)
            if collision:
                self.bullets.remove(bullet)
                time.sleep(1)
                self.players.remove(player)
                self._remove_cheater_start_real_game(bullet.shooter)
                break

    def _check_bullet_mirror_collisions(self, bullet):
        for mirror in self.mirrors.mirror_grids:
            collision = pygame.Rect.colliderect(bullet.rect, mirror)
            if collision:
                if mirror.width > mirror.height:
                    bullet.y_change_rate *= -1
                else:
                    bullet.x_change_rate *= -1

    def _real_game(self):
        if len(self.players) != 1:
            if self.shooter > len(self.players) - 1:
                self.shooter = 0
            if self.turn_ended and self.players[self.shooter].shot_left != 0:
                self._shoot(self.players[self.shooter])
                if self.shooter != len(self.players) - 1:
                    self.shooter += 1
                else:
                    self.shooter = 0
                self.turn_ended = False
            if len(self.bullets) == 0:
                self.turn_ended = True
        else:
            self.stats.game_active = False

    def _shoot(self, player):
        observable_players = self._observable(player)
        if len(observable_players) > 0:
            self._create_bullet(player, random.choice(observable_players))
            player.shot_left -= 1
        else:
            self._create_bullet(player, 0)
            player.shot_left -= 1

    def _update_screen(self):
        self.screen.fill(self.settings.bg_colour)
        if self.stats.game_active:
            if self.constructing:
                if time.time() > self.timer + 1:
                    self.stage.draw_stage()
                if time.time() > self.timer + 2:
                    self.barriers.draw_barriers()
                if time.time() > self.timer + 3:
                    self.mirrors.draw_mirrors()
                if time.time() > self.timer + 4:
                    self._draw_players()
                if time.time() > self.timer + 7:
                    self.constructing = False
                    self.cheating = True
            elif self.cheating:
                self.stage.draw_stage()
                self.barriers.draw_barriers()
                self.mirrors.draw_mirrors()
                self._draw_players()
                self._cheat()
                self._update_bullet()
                for bullet in self.bullets:
                    bullet.draw_bullet()
            elif self.real_game:
                self.stage.draw_stage()
                self.barriers.draw_barriers()
                self.mirrors.draw_mirrors()
                self._draw_players()
                self._update_bullet()
                for bullet in self.bullets:
                    bullet.draw_bullet()
        else:
            self.start_button.draw_button()
        pygame.display.flip()


if __name__ == "__main__":
    mygame = Main()
    mygame.run_game()
