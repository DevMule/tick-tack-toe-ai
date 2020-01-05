from bots_and_uis.controller import Controller


UIConsts = {
    "GREEN": '\033[92m',
    "RED": '\033[91m',
    "ENDC": '\033[0m',
    "BOLD": '\033[1m',
}


class ConsoleUI(Controller):
    def make_turn(self, desk):
        print("\n\nplayer \"" + desk.turn + "\", it\'s your turn:")
        self.print_desk(desk.desk)
        insert = input("write place to move: ")
        insert = int(insert)
        y = int((insert - 1) / len(desk.desk[0]))
        x = (insert - 1) % len(desk.desk[0])
        return [x, y]

    def game_ended(self, desk, state):
        print("\n\nplayer \"" + desk.turn + "\", wins:")
        self.print_desk(desk.desk)
        print(UIConsts['BOLD'] + state + UIConsts['ENDC'])
        return

    def print_desk(self, desk):
        for i in range(len(desk)):
            print_string = ""
            for j in range(len(desk[i])):
                if desk[i][j] == 1:
                    print_string += UIConsts['BOLD'] + UIConsts['RED'] + "[X]" + UIConsts['ENDC']
                elif desk[i][j] == 0:
                    print_string += UIConsts['BOLD'] + UIConsts['GREEN'] + "[0]" + UIConsts['ENDC']
                else:
                    print_string += "[" + str(len(desk[i]) * i + j + 1) + "]"
            print(print_string)
