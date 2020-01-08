from bots_and_uis.controller import Controller
from bots_and_uis.random_bot import pick_random
from desk.desk import desk_consts, check_win


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


def first_step(desk):
    for row in desk:
        for state in row:
            if state != desk_consts["empty"]:
                return False
    return True


class MiniMaxBot(Controller):
    def __init__(self):
        super().__init__()
        self.win_row = None

    def make_turn(self, desk):
        if first_step(desk.desk):
            return pick_random(desk.desk, desk.w, desk.h)

        cloned = clone_desk(desk.desk)
        figure = desk_consts[desk.turn]
        self.win_row = desk.win_row
        ways = self.calc_states_tree(cloned, figure, get_all_ways(cloned))
        for potential_way in ways:
            if potential_way[2] == 1:
                return potential_way
        for potential_way in ways:
            if potential_way[2] == 0:
                return potential_way
        return ways[0]

    def calc_states_tree(self, desk, figure, ways):
        for potential_way in ways:
            potential_way.append(self.get_value(desk, potential_way, figure))
            potential_way[2] *= -1  # swap weight
        return ways

    def get_value(self, desk, way, figure):
        # if we know value of this case, return value
        desk = clone_desk(desk)
        desk[way[1]][way[0]] = figure
        if check_win(way[0], way[1], desk, self.win_row):
            return -1  # it will be swapped later

        # if we need to go deeper, go deeper
        ways = get_all_ways(desk)
        if len(ways) > 0:
            valued_ways = self.calc_states_tree(desk, 1 - figure, ways)
            for potential_way in valued_ways:
                if potential_way[2] == 1:
                    return 1
            return 0

        # if we dont have any ways to go, return value = 0
        return 0
