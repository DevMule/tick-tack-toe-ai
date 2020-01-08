desk_consts = {
    "0": 0,
    0: "0",
    "X": 1,
    1: "X",
    "empty": -1,
}


def num_of_ways(desk):
    num = 0
    for i in range(len(desk)):
        for j in range(len(desk[i])):
            if desk[i][j] == desk_consts["empty"]:
                num += 1
    return num


def out_of_desk_range(x, y, desk):
    return x > len(desk[0]) - 1 or x < 0 or y > len(desk) - 1 or y < 0


def check_win(x, y, desk, win_row):
    turn = desk[y][x]

    #  vertical
    shift = in_row = 0
    while (not out_of_desk_range(x, y + shift, desk)) and (desk[y + shift][x] == turn):
        in_row += 1
        shift += 1
    shift = 0
    while (not out_of_desk_range(x, y + shift, desk)) and (desk[y + shift][x] == turn):
        in_row += 1
        shift -= 1
    if in_row - 1 >= win_row:
        return True

    #  horizontal
    shift = in_row = 0
    while (not out_of_desk_range(x + shift, y, desk)) and (desk[y][x + shift] == turn):
        in_row += 1
        shift += 1
    shift = 0
    while (not out_of_desk_range(x + shift, y, desk)) and (desk[y][x + shift] == turn):
        in_row += 1
        shift -= 1
    if in_row - 1 >= win_row:
        return True

    #  diagonal left up
    shift = in_row = 0
    while (not out_of_desk_range(x + shift, y + shift, desk)) and (
            desk[y + shift][x + shift] == turn):
        in_row += 1
        shift += 1
    shift = 0
    while (not out_of_desk_range(x + shift, y + shift, desk)) and (
            desk[y + shift][x + shift] == turn):
        in_row += 1
        shift -= 1
    if in_row - 1 >= win_row:
        return True

    #  diagonal right up
    shift = in_row = 0
    while (not out_of_desk_range(x - shift, y + shift, desk)) and (
            desk[y + shift][x - shift] == turn):
        in_row += 1
        shift += 1
    shift = 0
    while (not out_of_desk_range(x - shift, y + shift, desk)) and (
            desk[y + shift][x - shift] == turn):
        in_row += 1
        shift -= 1
    if in_row - 1 >= win_row:
        return True

    return False


class Desk:
    def __init__(self, w=3, h=3, win_row=3, desk=None, turn=desk_consts["X"]):
        self.w = w
        self.h = h
        self.desk = desk
        self.__turn = turn
        self.win_row = win_row
        self.winner = None
        if not desk:
            self.clear(w, h, win_row)

    def clone(self):
        return Desk(self.w, self.h, self.win_row, self.desk, self.__turn)

    def get_turn(self):
        return desk_consts[self.__turn]

    turn = property(get_turn)

    # main funcs
    def clear(self, w=3, h=3, win_row=3):
        self.__turn = desk_consts["X"]  # 0 - 0, 1 - X
        self.desk = []
        self.win_row = win_row
        self.winner = None
        for i in range(h):
            self.desk.append([])
            for j in range(w):
                self.desk[i].append(desk_consts["empty"])
        #  -1 = empty, 0 = "0", 1 = "X"

    def make_turn(self, x, y):

        # todo refactor function
        if not type(x) is int or not type(y) is int:
            return False

        if out_of_desk_range(x, y, self.desk):
            return False

        # if cell is not empty, do not write
        if self.desk[y][x] != desk_consts["empty"]:
            return False

        self.desk[y][x] = self.__turn
        if not check_win(x, y, self.desk, self.win_row):
            if num_of_ways(self.desk) == 0:
                self.winner = "TIE"
                return False
            else:
                self.__turn = 1 - self.__turn
        else:
            self.winner = desk_consts[self.__turn]
        return True
