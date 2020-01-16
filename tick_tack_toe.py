from desk.desk import Desk
from bots_and_uis.neural_network_bot import NeuralNetworkBot, desk_to_inputs
from bots_and_uis.console_game import ConsoleUI
from bots_and_uis.random_bot import RandomBot
from bots_and_uis.minimax_bot import MiniMaxBot
from referee import Referee
import sys

sys.setrecursionlimit(2048)
file = open("data.txt", "w")


def write_line():
    return


console_player = ConsoleUI()
random_bot = RandomBot()
mini_max_bot = MiniMaxBot()
neural_network_bot = NeuralNetworkBot(inputs=9, learn_rate=.1, epochs=1000)

referee = Referee(
    mini_max_bot,  # X - player
    random_bot,  # 0 - player
    Desk(3, 3, 3),
)

for i in range(10):
    referee.play_matches(10)
    print('X:' + str(referee.rounds['X']) + ', 0:' + str(referee.rounds['0']) + ', TIE:' + str(referee.rounds['TIE']))
