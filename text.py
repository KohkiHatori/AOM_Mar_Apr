import pygame.font


class Text:

    def __init__(self, main):
        self.main = main
        self.screen = main.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = main.settings
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 40)

    def prep_cheat_text(self, cheater_index):
        player_num = cheater_index + 1
        str = "Player {} Cheated !".format(player_num)
        self.cheat_image = self.font.render(str, True, self.text_color, self.settings.bg_colour)
        self.cheat_rect = self.cheat_image.get_rect()
        self.cheat_rect.centerx = self.screen.get_width() / 2
        self.cheat_rect.top = 50

    def prep_stats(self):
        list_of_strings = [x for x in range(self.settings.num_player)]
        for player in self.main.players:
            player_str = "P" + str(player.original_index + 1) + ": " + str(player.shot_left) + "  "
            list_of_strings[player.original_index] = player_str
        for item in list_of_strings:
            index = list_of_strings.index(item)
            if item == index:
                list_of_strings[index] = "P" + str(index + 1) + ": Dead  "
        starting_point = 100
        gap = (self.screen.get_width() - 100) / self.settings.num_player
        self.stats_list = []
        for i in range(self.settings.num_player):
            image = self.font.render(list_of_strings[i], True, self.settings.player_colours[i], self.settings.bg_colour)
            rect = image.get_rect()
            rect.centerx = starting_point + i * gap
            rect.top = 50
            li = [image, rect]
            self.stats_list.append(li)

    def prep_winner(self):
        self.winner_list = []
        for player in self.main.players:
            self.winner_list.append(player.original_index)
        string = "Winners are {}"
        sub_string = ""
        for i in self.winner_list:
            sub_string += "Player {}".format(i)
        string.format(sub_string)
        self.winner_image = self.font.render(string, True, self.text_color, self.settings.bg_colour)
        self.winner_rect = image.get_rect()
        rect.centerx = self.screen.get_width() / 2
        rect.top = 50

    def show_cheater(self):
        self.screen.blit(self.cheat_image, self.cheat_rect)

    def show_stats(self):
        for i in self.stats_list:
            self.screen.blit(i[0], i[1])

    def show_winner(self):
        self.screen.blit(self.winner_image, self.winner_rect)