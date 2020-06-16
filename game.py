from desk.desk import Desk
from bots_and_uis.neural_network_bot import NeuralNetworkBot
from bots_and_uis.perceptron_bot import PerceptronBot
from bots_and_uis.console_game import ConsoleUI
from bots_and_uis.random_bot import RandomBot
from bots_and_uis.minimax_bot import MiniMaxBot
from referee import Referee


class Game:
    def __init__(self):
        self.UI = ConsoleUI()

        self.rb = RandomBot()

        self.mb = MiniMaxBot()

        self.pb = PerceptronBot("mySave", 9, 9)
        self.pb.load_experience()

        self.referee = Referee(
            self.pb,  # X - player
            self.UI,  # 0 - player
            Desk(3, 3, 3),
        )

    def play(self, num_of_parties=1):
        for i in range(num_of_parties):
            self.referee.desk.clear()
            self.referee.game_loop()
            self.referee.swap_players()

    def set_options(self, pX=None, p0=None, desk_w=None, desk_h=None, win_row=None):
        if pX: self.referee.player_X = pX
        if p0: self.referee.player_0 = p0

        if not desk_w: desk_w = self.referee.desk.w
        if not desk_h: desk_h = self.referee.desk.h
        self.referee.desk.clear(desk_w, desk_h, win_row)


g = Game()
g.play(1)
