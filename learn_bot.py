from desk.desk import Desk
from bots_and_uis.random_bot import RandomBot
from bots_and_uis.minimax_bot import MiniMaxBot
from bots_and_uis.neural_network_bot import NeuralNetworkBot
from bots_and_uis.console_game import ConsoleUI
from referee import Referee


neural_network_bot = NeuralNetworkBot(
    inputs=9,  # 9 входных нейровнов
    hidden=81,  # 81 скрытых нейровнов
    outputs=9,  # 9 выходных нейровнов
    learning=True,  # бот будет учиться, менять свой опыт
    new_experience=True,  # бот при инициализации создаст новый опыт
    learn_rate=1,  # коэффициент изменения веса для нейронов при одном цикле изучения
    learn_decrease_coef=.5,  # коэффициент, с которым падает вес изучения для каждого предыдущего
                             #  шага чтобы не переписывать имеющийся позитивный опыт
)

referee = Referee(
    MiniMaxBot(),  # X - player
    neural_network_bot,  # 0 - player
    Desk(3, 3, 3),
)

for i in range(500):
    print(i)
    referee.desk.clear()
    referee.game_loop()
    referee.swap_players()
neural_network_bot.save_experience()
print("опыт сохранён")

referee.player_0 = ConsoleUI()
for i in range(5):
    referee.desk.clear()
    referee.game_loop()
    referee.swap_players()
