desk_consts = {
    "0": 0,
    0: "0",
    "X": 1,
    1: "X",
    "empty": -1,
}


class Desk:
    def __init__(self, w=3, h=3, win_row=3):
        self.__desk = None
        self.__turn = desk_consts["X"]
        self.__row_to_win = 3
        self.winner = None
        self.clear(w, h, win_row)

    # getters & setters
    def get_desk(self):
        return self.__desk

    def get_turn(self):
        return desk_consts[self.__turn]

    desk = property(get_desk)
    turn = property(get_turn)

    # main funcs
    def clear(self, w=3, h=3, win_row=3):
        self.__turn = desk_consts["X"]  # 0 - 0, 1 - X
        self.__desk = []
        self.__row_to_win = win_row
        self.winner = None
        for i in range(h):
            self.__desk.append([])
            for j in range(w):
                self.__desk[i].append(desk_consts["empty"])
        #  -1 = empty, 0 = "0", 1 = "X"

    def __check_win(self, x, y):
        #  todo try to refactor
        #  vertical
        shift = in_row = 0
        while (not self.__out_of_desk_range(x, y + shift)) and (self.__desk[y + shift][x] == self.__turn):
            in_row += 1
            shift += 1
        shift = 0
        while (not self.__out_of_desk_range(x, y + shift)) and (self.__desk[y + shift][x] == self.__turn):
            in_row += 1
            shift -= 1
        if in_row - 1 >= self.__row_to_win:
            return True

        #  horizontal
        shift = in_row = 0
        while (not self.__out_of_desk_range(x + shift, y)) and (self.__desk[y][x + shift] == self.__turn):
            in_row += 1
            shift += 1
        shift = 0
        while (not self.__out_of_desk_range(x + shift, y)) and (self.__desk[y][x + shift] == self.__turn):
            in_row += 1
            shift -= 1
        if in_row - 1 >= self.__row_to_win:
            return True

        #  diagonal left up
        shift = in_row = 0
        while (not self.__out_of_desk_range(x + shift, y + shift)) and (
                self.__desk[y + shift][x + shift] == self.__turn):
            in_row += 1
            shift += 1
        shift = 0
        while (not self.__out_of_desk_range(x + shift, y + shift)) and (
                self.__desk[y + shift][x + shift] == self.__turn):
            in_row += 1
            shift -= 1
        if in_row - 1 >= self.__row_to_win:
            return True

        #  diagonal right up
        shift = in_row = 0
        while (not self.__out_of_desk_range(x - shift, y + shift)) and (
                self.__desk[y + shift][x - shift] == self.__turn):
            in_row += 1
            shift += 1
        shift = 0
        while (not self.__out_of_desk_range(x - shift, y + shift)) and (
                self.__desk[y + shift][x - shift] == self.__turn):
            in_row += 1
            shift -= 1
        if in_row - 1 >= self.__row_to_win:
            return True

        return False

    def __check_ways(self):
        num = 0
        for i in range(len(self.__desk)):
            for j in range(len(self.__desk[i])):
                if self.desk[i][j] == desk_consts["empty"]:
                    num += 1
        return num

    def __out_of_desk_range(self, x, y):
        return x > len(self.__desk[0]) - 1 or x < 0 or y > len(self.__desk) - 1 or y < 0

    def make_turn(self, x, y):

        # todo refactor function
        if not type(x) is int or not type(y) is int:
            return False

        if self.__out_of_desk_range(x, y):
            return False

        # if cell is not empty, do not write
        if self.__desk[y][x] != desk_consts["empty"]:
            return False

        self.__desk[y][x] = self.__turn
        if not self.__check_win(x, y):
            if self.__check_ways() == 0:
                self.winner = "TIE"
                return False
            else:
                self.__turn = 1 - self.__turn
        else:
            self.winner = desk_consts[self.__turn]
        return True
