from bots_and_uis.controller import Controller
from desk.desk import desk_consts


def clone_desk(desk):
    new_desk = []
    for i in range(len(desk)):
        new_desk.append([])
        for j in range(len(desk[i])):
            new_desk[i].append(desk[i][j])
    return new_desk


def get_all_ways(desk):
    ways = []
    for y in range(len(desk)):
        for x in range(len(desk[y])):
            if desk[y][x] == desk_consts["empty"]:
                ways.append([x, y])
    return ways


class MiniMaxBot(Controller):
    def __init__(self, max_depth=10):
        super().__init__()
        self.max_depth = max_depth
        self.our_figure = None
        self.desk = None

    def make_turn(self, desk):
        self.desk = desk
        self.our_figure = desk.turn

        # clone state to manipulate it
        state = clone_desk(desk.desk)
        steps = min(self.max_depth, desk.num_of_ways(state))

        potential_ways = self.get_ways_and_value(state, 1)
        my_step = None
        for value in potential_ways:
            val = self.calc_states_tree(value, steps, -1)
            if val["val"] == 1 or (val["val"] == 0 and not my_step):
                my_step = val["way"]
        return my_step

    # recursive function
    def calc_states_tree(self, value, steps, is_our_turn):
        couuu()
        if steps <= 0:
            return {
                "val": 0,
            }

        # прямой ход - просчитываем состояния и значения
        value["ways"] = self.get_ways_and_value(value["state"], -1 * is_our_turn)
        for potential_way in value["ways"]:
            if potential_way["val"] == 0:
                potential_way["ways"] = self.calc_states_tree(potential_way, steps - 1, -1 * is_our_turn)

        # обратный ход - назначаем веса объектам выше
        for potential_way in value["ways"]:
            if potential_way["val"] == is_our_turn:
                value["val"] = is_our_turn

        return value

    def get_ways_and_value(self, state, is_our_turn):
        figure = self.our_figure
        if is_our_turn != 1:
            figure = desk_consts[1 - desk_consts[self.our_figure]]

        values = []
        ways = get_all_ways(state)
        for i in range(len(ways)):
            new_state = clone_desk(state)
            new_state[ways[i][1]][ways[i][0]] = desk_consts[figure]
            if_win = self.desk.check_win(ways[i][0], ways[i][1], new_state)
            values.append({
                "way": ways[i],
                "val": int(if_win) * is_our_turn,
                "state": new_state,
                "ways": []
            })
        return values


aii = 1
def couuu():
    global aii
    print(aii)
    aii += 1
