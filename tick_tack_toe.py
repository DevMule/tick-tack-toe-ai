from desk.desk import Desk
from bots_and_uis.console_game import ConsoleUI
from bots_and_uis.ai_bot import AIBot
from bots_and_uis.random_bot import RandomBot
from referee import Referee

referee = Referee(
    ConsoleUI(),  # X - player
    ConsoleUI(),  # 0 - player
    Desk(3, 3, 3),
)
