from desk.desk import Desk
from bots_and_uis.neural_network_bot import NeuralNetworkBot
from bots_and_uis.perceptron_bot import PerceptronBot
from bots_and_uis.console_game import ConsoleUI
from bots_and_uis.random_bot import RandomBot
from bots_and_uis.minimax_bot import MiniMaxBot
from referee import Referee

pb = PerceptronBot("mySave", 9, 9, 9, 9)
pb.load_experience()

referee = Referee(
    pb,  # X - player
    ConsoleUI(),  # 0 - player
    Desk(3, 3, 3),
)
for i in range(1000):
    referee.desk.clear()
    referee.game_loop()
    referee.swap_players()
