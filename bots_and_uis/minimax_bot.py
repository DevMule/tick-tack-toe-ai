from bots_and_uis.controller import Controller


def clone_desk(desk):
    new_desk = []
    for i in range(len(desk)):
        new_desk.append([])
        for j in range(len(desk[i])):
            new_desk[i].append(desk[i][j])
    return new_desk


class MiniMaxBot(Controller):
    def __init__(self, max_depth=10):
        super().__init__()
        self.max_depth = max_depth

    def make_turn(self, desk):
        # todo проверить если бот играет за нолик - инвертировать
        #  бот должен играть за крестик, так легче рассмотреть свои и вражеские
        # clone state to manipulate it
        state = clone_desk(desk.desk)
        print(state)

    def calc_states_tree(self, state):
        return
