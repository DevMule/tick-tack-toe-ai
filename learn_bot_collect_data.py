from bots_and_uis.console_game import coord_to_id
from desk.desk import Desk
from bots_and_uis.random_bot import RandomBot
from bots_and_uis.minimax_bot import MiniMaxBot
from referee import Referee
import json

mm = MiniMaxBot()
rand = RandomBot()
referee = Referee(
    mm,  # X - player
    rand,  # 0 - player
    Desk(3, 3, 3),
)

# collect data
N = 100
for i in range(N):
    referee.desk.clear()
    referee.game_loop()
    referee.swap_players()
    print(i + 1, "/", N)

# fix data
inputs = []
outputs = []
for k in mm.cache.keys():
    inp = k.strip('][').split(', ')
    for i in range(len(inp)): inp[i] = int(inp[i])
    inputs.append(inp)

    id = coord_to_id(referee.desk.h, mm.cache[k][0], mm.cache[k][1])
    out = [int(i == id) for i in range(referee.desk.h * referee.desk.w)]
    outputs.append(out)
    print(inp, out)

# save data
with open('bots_and_uis/perceptron_bot_experience/dataset.json', "w") as write_file:
    json.dump({
        "inputs": inputs,
        "outputs": outputs
    }, write_file)
