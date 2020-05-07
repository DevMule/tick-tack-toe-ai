from desk.desk import Desk
from bots_and_uis.perceptron_bot import PerceptronBot
from bots_and_uis.random_bot import RandomBot
from bots_and_uis.minimax_bot import MiniMaxBot
from referee import Referee

rb = RandomBot()
mmb = MiniMaxBot()
pb = PerceptronBot("mySave", 9, 9, 9, 9)
pb.load_experience()

referee = Referee(
    rb,  # X - player
    rb,  # 0 - player
    Desk(3, 3, 3),
)

battles = [
    (rb, mmb, "Random_bot", "MiniMax_bot"),
    (mmb, pb, "MiniMax_bot", "Perceptron_bot"),
    (pb, rb, "Perceptron_bot", "Random_bot")
]

N = 1000
for battle in battles:
    referee.player_X = battle[0]
    referee.player_0 = battle[1]
    p1_wins = p2_wins = ties = 0
    for i in range(N):
        referee.desk.clear()
        referee.game_loop()

        if referee.desk.winner == "TIE":
            ties += 1
        elif referee.desk.winner == "X":
            if referee.player_X == battle[0]:
                p1_wins += 1
            else:
                p2_wins += 1
        else:
            if referee.player_0 == battle[0]:
                p1_wins += 1
            else:
                p2_wins += 1
        referee.swap_players()
    print(battle[2], p1_wins, ":", battle[3], p2_wins, ": TIE", ties)
