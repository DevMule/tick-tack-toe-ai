from desk import Desk

d = Desk(3, 3, 3)


class Bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_desk(desk):
    print("\n\n")
    for i in range(len(desk)):
        print_string = ""
        for j in range(len(desk[i])):
            if desk[i][j] == 1:
                print_string += Bcolors.BOLD + Bcolors.RED + "[X]" + Bcolors.ENDC
            elif desk[i][j] == 0:
                print_string += Bcolors.BOLD + Bcolors.GREEN + "[0]" + Bcolors.ENDC
            else:
                print_string += "[" + str(len(desk[i]) * i + j + 1) + "]"
        print(print_string)


game = True
while game:
    print_desk(d.desk)
    insert = int(input(Bcolors.HEADER + "Player " + d.turn + " its your turn, \nwrite place you like: " + Bcolors.ENDC))
    y = int((insert - 1) / len(d.desk[0]))
    x = (insert - 1) % len(d.desk[0])

    d.make_turn(x, y)

    if d.winner:
        print_desk(d.desk)
        if d.winner == "TIE":
            print(Bcolors.HEADER + "Ooops, seems like nobody wins this game!" + Bcolors.ENDC)
        else:
            print(Bcolors.HEADER + "player " + d.winner + " won the game!" + Bcolors.ENDC)
        if input("would you like to play again? \nY for yes, otherwise - no: ") == "Y":
            d.clear()
        else:
            game = False
