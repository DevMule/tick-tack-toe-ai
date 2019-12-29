from desk import Desk

d = Desk()


def print_desk(desk):
    print("\n\n_| 0 1 2 ")
    for i in range(len(desk)):
        print_string = "" + str(i) + "| "
        for j in range(len(desk[i])):
            if desk[i][j] == 1:
                print_string += "X "
            elif desk[i][j] == 0:
                print_string += "0 "
            else:
                print_string += "_ "
        print(print_string)


game = True
while game:
    print_desk(d.desk)
    insert = input("Player " + d.turn + " its your turn, \nwrite coords like 'x, y': ")
    insert = insert.split(",")
    x = int(insert[0])
    y = int(insert[1])

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
