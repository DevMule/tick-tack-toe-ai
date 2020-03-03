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
    new_experience=False,  # бот при инициализации создаст новый опыт
    learn_rate=.2,  # коэффициент изменения веса для нейронов при одном цикле изучения
    learn_decrease_coef=.75,  # коэффициент, с которым падает вес изучения для каждого предыдущего
    #  шага чтобы не переписывать имеющийся позитивный опыт
)

referee = Referee(
    neural_network_bot,  # X - player
    ConsoleUI(),  # 0 - player
    Desk(3, 3, 3),
)

N = 1000
for i in range(1000):
    print(str(i+1) + '/' + str(N))
    referee.desk.clear()
    referee.game_loop()
    referee.swap_players()
    if i+1 % 10:
        neural_network_bot.save_experience()
        print("опыт сохранён")
