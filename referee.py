from tick_tack_toe import *


class Referee:
    def __init__(self, player_1, player_2, desk=Desk(3, 3, 3)):
        self.player_1 = player_1
        self.player_2 = player_2
        self.desk = desk
