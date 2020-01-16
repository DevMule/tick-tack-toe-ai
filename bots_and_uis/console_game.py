from bots_and_uis.controller import Controller
from desk.desk import desk_consts

UIConsts = {
    "GREEN": '\033[92m',
    "RED": '\033[91m',
    "ENDC": '\033[0m',
    "BOLD": '\033[1m',
}


def id_to_coord(height, index):
    y = int(index / height)
    x = index % height
    return [x, y]


def coord_to_id(height, y, x):
    return len(height) * y + x


def print_desk(desk):
    for i in range(len(desk)):
        print_string = ""
        for j in range(len(desk[i])):
            if desk[i][j] == desk_consts['X']:
                print_string += UIConsts['BOLD'] + UIConsts['RED'] + "[X]" + UIConsts['ENDC']
            elif desk[i][j] == desk_consts['0']:
                print_string += UIConsts['BOLD'] + UIConsts['GREEN'] + "[0]" + UIConsts['ENDC']
            else:
                print_string += "[" + str(coord_to_id(desk[i], i, j) + 1) + "]"
        print(print_string)


class ConsoleUI(Controller):
    def make_turn(self, desk):
        print("\n\nplayer \"" + desk.turn + "\", it\'s your turn:")
        print_desk(desk.desk)
        insert = int(input("write place to move: "))
        return id_to_coord(len(desk.desk[0]), insert - 1)

    def game_ended(self, desk, state):
        if state == "TIE":
            print("\n\nnobody wins:")
        else:
            print("\n\nplayer \"" + desk.turn + "\", wins:")
        print_desk(desk.desk)
        print(UIConsts['BOLD'] + state + UIConsts['ENDC'])
        return
