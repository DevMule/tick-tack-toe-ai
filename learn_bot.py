from desk.desk import Desk, desk_consts
from bots_and_uis.neural_network_bot import NeuralNetworkBot, desk_to_inputs, game_result_weights
from bots_and_uis.console_game import coord_to_id
from bots_and_uis.random_bot import RandomBot
from bots_and_uis.minimax_bot import MiniMaxBot
from bots_and_uis.console_game import ConsoleUI
from referee import Referee, RefereeConsts


# [('cp37', 'cp37m', 'win32'),
# ('cp37', 'none', 'win32'),
# ('py3', 'none', 'win32'),
# ('cp37', 'none', 'any'),
# ('cp3', 'none', 'any'),
# ('py37', 'none', 'any'),
# ('py3', 'none', 'any'),
# ('py36', 'none', 'any'),
# ('py35', 'none', 'any'),
# ('py34', 'none', 'any'),
# ('py33', 'none', 'any'),
# ('py32', 'none', 'any'),
# ('py31', 'none', 'any'),
# ('py30', 'none', 'any')]


def inputs_to_key(inputs):
    key = 0
    for k in range(len(inputs)):
        key += pow(2, k) * inputs[k]
    return key


neural_network_bot = NeuralNetworkBot(inputs=9, learn_rate=.05, epochs=100)

referee = Referee(
    MiniMaxBot(),  # X - player
    RandomBot(),  # 0 - player
    Desk(3, 3, 3),
)

for i in range(1, 101):
    print(i)
    referee.desk.clear()
    referee.game_loop()
    neural_network_bot.game_ended(referee.desk, RefereeConsts[1][referee.desk.winner], referee.desk.winner)

referee.swap_players()

for i in range(101, 201):
    print(i)
    referee.desk.clear()
    referee.game_loop()
    neural_network_bot.game_ended(referee.desk, RefereeConsts[0][referee.desk.winner], referee.desk.winner)

referee.player_1 = neural_network_bot
referee.player_0 = ConsoleUI()

for i in range(1000):
    referee.desk.clear()
    referee.game_loop()
    referee.swap_players()
