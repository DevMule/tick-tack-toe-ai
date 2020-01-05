from bots_and_uis.controller import Controller


class Bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class ConsoleUI(Controller):
    def make_turn(self, desk):
        self.print_desk(desk)

        input_line = input("write x,y: ").split(",")
        x = int(input_line[0])
        y = int(input_line[1])
        return [x, y]

    def print_desk(self, desk):
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
