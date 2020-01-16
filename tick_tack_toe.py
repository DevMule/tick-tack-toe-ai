from desk.desk import Desk
from bots_and_uis.neural_network_bot import NeuralNetworkBot
from bots_and_uis.console_game import ConsoleUI
from bots_and_uis.random_bot import RandomBot
from bots_and_uis.minimax_bot import MiniMaxBot
from referee import Referee
import sys

sys.setrecursionlimit(1000)

random_bot = RandomBot()
mini_max_bot = MiniMaxBot()
neural_network_bot = NeuralNetworkBot(inputs=9, learn_rate=0.05, epochs=3)

referee = Referee(
    neural_network_bot,  # X - player
    random_bot,  # 0 - player
    Desk(3, 3, 3),
)

for i in range(0):
    referee.play_matches(25)
    print('X:' + str(referee.rounds['X']) + ', 0:' + str(referee.rounds['0']) + ', TIE:' + str(referee.rounds['TIE']))

referee.player_0 = mini_max_bot
print('minimax_bot')
for i in range(30):
    referee.play_matches(1)
    print('X:' + str(referee.rounds['X']) + ', 0:' + str(referee.rounds['0']) + ', TIE:' + str(referee.rounds['TIE']))

