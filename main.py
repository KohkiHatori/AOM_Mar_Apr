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
from button import Button
from bullet import Bullet
from text import  Text


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
        self.start_button = Button(self, "START")
        self._create_environment()
        self.constructing = True
        self.cheating = False
        self.real_game = False
        self.end = False
        self.bullets = []
        self.turn_ended = True
        self.no_bullet = True
        self.player_moved = False
        self.shooter = 0
        self.text = Text(self)
        self.game_active = False
        self.end_button = Button(self, "END")

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
                self._check_end_button(mouse_pos)

    @staticmethod
    def _check_keydown_events(event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                sys.exit()

    def _check_start_button(self, mouse_pos):
        if not self.game_active:
            if self.start_button.rect.collidepoint(mouse_pos):
                self.game_active = True
                self.constructing = True
                pygame.mouse.set_visible(False)
                self.timer = time.time()

    def _check_end_button(self, mouse_pos):
        if self.end:
            if self.end_button.rect.collidepoint(mouse_pos):
                sys.exit()

    def _create_environment(self):
        self.stage.create_stage()
        self.barriers.create_barriers()
        self.mirrors.create_mirrors()
        self._create_players()

    def _create_players(self):
        no_barrier = self.barriers.no_barrier_grids.copy()
        for i in range(self.settings.num_player):
            new_player = Player(self)
            new_player.colour = self.settings.player_colours[i]
            valid = False
            while not valid:
                random.shuffle(no_barrier)
                for item in no_barrier:
                    if item != 0:
                        choice = item
                        break
                new_player.rect = choice
                if no_barrier[no_barrier.index(new_player.rect)] != 0:
                    x, y = new_player.rect.centerx, new_player.rect.centery

                    for row in range(-1, 2):
                        for column in range(-1, 2):
                            for grid in no_barrier:
                                try:
                                    collision = grid.collidepoint(x - self.settings.grid_width * column,
                                                                  y - self.settings.grid_height * row)
                                    if collision:
                                        no_barrier[no_barrier.index(grid)] = 0
                                except:
                                    pass
                    valid = True
            for grid in self.stage.grids:
                collision = choice.collidepoint(grid.centerx, grid.centery)
                if collision:
                    index = self.stage.grids.index(grid)
                    break

            self.players.append(new_player)
            new_player.original_index = i
            new_player.original_grid_y = index // self.settings.num_column + 1
            new_player.original_grid_x = index - self.settings.num_column * (new_player.original_grid_y - 1) + 1

    def _draw_players(self):
        for player in self.players:
            player.blitme()

    def _collision(self, x, x_, y, y_, li):
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

    def _observable(self, observer):
        observable_players = []
        other_players = self.players.copy()
        other_players.remove(observer)
        observer_x = observer.rect.centerx
        observer_y = observer.rect.centery
        for player in other_players:
            searching_x = player.rect.centerx
            searching_y = player.rect.centery
            if not self._collision(observer_x, searching_x, observer_y, searching_y, self.barriers.barrier_grids):
                observable_players.append(player)

        return observable_players

    @run_once
    def _cheat(self):
        cheater_index = random.randint(0, self.settings.num_player - 1)
        self.text.prep_cheat_text(cheater_index)
        cheater = self.players[cheater_index]
        observable_players = self._observable(cheater)
        if len(observable_players) > 0:
            self._create_bullet(cheater, random.choice(observable_players))
        else:
            self._create_bullet(cheater, 0)

    @run_once
    def _remove_cheater_start_real_game(self, cheater):
        self.players.remove(cheater)
        time.sleep(1)
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
            if x_ != x:
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
            angle = random.randint(0, 360)
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
                self._no_bullet_left()
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
                self._no_bullet_left()
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
                shooter_index = self.players.index(bullet.shooter)
                if self.players.index(player) < shooter_index:
                    self.shooter -= 1
                try:
                    self.bullets.remove(bullet)
                except:
                    pass
                self._no_bullet_left()
                time.sleep(0.5)
                self.players.remove(player)
                self._remove_cheater_start_real_game(bullet.shooter)
                break

    def _check_bullet_mirror_collisions(self, bullet):
        for mirror in self.mirrors.mirror_grids:
            collision = pygame.Rect.colliderect(bullet.rect, mirror)
            if collision and time.time() - self.timer > 0.1:
                if mirror.width > mirror.height:
                    bullet.y_change_rate *= -1
                else:
                    bullet.x_change_rate *= -1
                self.timer = time.time()

    def _real_game(self):
        if len(self.players) != 1:
            if self.turn_ended and self.players[self.shooter].shot_left != 0:
                self._shoot(self.players[self.shooter])
                self.turn_ended = False
                self.no_bullet = False
            if len(self.bullets) == 0:
                self.no_bullet = True
            if self.no_bullet:
                self.player_moved = False
                self._move(self.players[self.shooter])
            if self.no_bullet and self.player_moved:
                self.turn_ended = True
        else:
            self.text.prep_winner()
            self.end = True
            pygame.mouse.set_visible(True)
            self.game_active = False

    def _no_bullet_left(self):
        has_no_bullets = []
        for player in self.players:
            if player.shot_left == 0:
                has_no_bullets.append(True)
            else:
                has_no_bullets.append(False)
        if all(has_no_bullets):
            self.text.prep_winner()
            self.end = True
            pygame.mouse.set_visible(True)
            self.game_active = False

    def _move(self, player):
        available_grids = []
        x, y = player.rect.centerx, player.rect.centery
        for row in range(-1, 2):
            for column in range(-1, 2):
                for grid in self.stage.grids:
                    if row == 0 and column == 0:
                        pass
                    else:
                        collision = grid.collidepoint(x - self.settings.grid_width * column,
                                                      y - self.settings.grid_height * row)
                        if collision and grid in self.barriers.no_barrier_grids:
                            player_player_collision_list = []
                            for p in self.players:
                                player_player_collision = p.rect.collidepoint(grid.centerx, grid.centery)
                                player_player_collision_list.append(player_player_collision)
                            if any(player_player_collision_list):
                                pass
                            else:
                                available_grids.append(grid)

        other_players = self.players.copy()
        other_players.remove(player)
        safe_grids = []
        for grid in available_grids:
            x_ = grid.centerx
            y_ = grid.centery
            safe_or_not_list = []
            for p in other_players:
                x = p.rect.centerx
                y = p.rect.centery
                if self._collision(x, x_, y, y_, self.barriers.barrier_grids):
                    safe_or_not = True
                    safe_or_not_list.append(safe_or_not)
            if all(safe_or_not_list):
                safe_grids.append(grid)

        if len(safe_grids) == 0:
            destination = random.choice(available_grids)
            player.rect.centerx, player.rect.centery = destination.centerx, destination.centery
        else:
            destination = random.choice(safe_grids)
            player.rect.centerx, player.rect.centery = destination.centerx, destination.centery

        self.player_moved = True
        if self.shooter < len(self.players) - 1:
            self.shooter += 1
        else:
            self.shooter = 0
        time.sleep(0.5)

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
        if self.game_active:
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
                self.text.show_cheater()
            elif self.real_game:
                self.stage.draw_stage()
                self.barriers.draw_barriers()
                self.mirrors.draw_mirrors()
                self._draw_players()
                self._update_bullet()
                for bullet in self.bullets:
                    bullet.draw_bullet()
                self.text.prep_stats()
                self.text.show_stats()
        elif self.end:
            self.text.show_winner()
            self.end_button.draw_button()
        else:
            self.start_button.draw_button()
        pygame.display.flip()


if __name__ == "__main__":
    mygame = Main()
    mygame.run_game()
