from desk.desk import Desk
from bots_and_uis.deeplearning_bot import DeepLearningBot
from bots_and_uis.console_game import ConsoleUI
from bots_and_uis.random_bot import RandomBot
from bots_and_uis.minimax_bot import MiniMaxBot
from referee import Referee

referee = Referee(
    DeepLearningBot(),  # X - player
    ConsoleUI(),  # 0 - player
    Desk(3, 3, 3),
)
