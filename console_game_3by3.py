from desk import Desk

d = Desk(3, 3, 3)


def print_desk(desk):
    print("\n\n")
    for i in range(len(desk)):
        print_string = ""
        for j in range(len(desk[i])):
            if desk[i][j] == 1:
                print_string += "[X]"
            elif desk[i][j] == 0:
                print_string += "[0]"
            else:
                print_string += "[" + str(len(desk[i])*i + j + 1) + "]"
        print(print_string)


game = True
while game:
    print_desk(d.desk)
    insert = int(input("Player " + d.turn + " its your turn, \nwrite place you like: "))
    y = int((insert - 1) / len(d.desk[0]))
    x = (insert - 1) % len(d.desk[0])

    d.make_turn(x, y)

    if d.winner:
        print_desk(d.desk)
        if d.winner == "TIE":
            print("Ooops, seems like nobody wins this game!")
        else:
            print("player " + d.winner + " won the game!")
        if input("would you like to play again? \nY for yes, otherwise - no: ") == "Y":
            d.clear()
        else:
            game = False
