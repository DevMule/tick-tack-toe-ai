from desk.desk import Desk, desk_consts

RefereeConsts = {
    0: {
        "X": "FAIL",
        "0": "WIN",
        "TIE": "TIE",
    },
    1: {
        "X": "WIN",
        "0": "FAIL",
        "TIE": "TIE",
    },
}


class Referee:
    def __init__(self, player_x, player_0, desk=Desk(3, 3, 3)):
        self.player_0 = player_0
        self.player_X = player_x
        self.desk = desk

        # self.game_loop()

    def swap_players(self):
        tmp_player = self.player_X
        self.player_X = self.player_0
        self.player_0 = tmp_player

    def game_loop(self):
        if not self.desk.winner:
            t = self.ask_for_turn()
            self.desk.make_turn(t[0], t[1])
            self.game_loop()
        else:
            self.player_0.game_ended(self.desk, RefereeConsts[0][self.desk.winner], desk_consts[0])
            self.player_X.game_ended(self.desk, RefereeConsts[1][self.desk.winner], desk_consts[1])

    def ask_for_turn(self):
        current_player = self.player_0
        if self.desk.turn == "X":
            current_player = self.player_X
        return current_player.make_turn(self.desk)
