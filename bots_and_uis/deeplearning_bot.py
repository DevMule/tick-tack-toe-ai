from bots_and_uis.controller import Controller
from bots_and_uis.console_game import id_to_coord
from desk.desk import desk_consts
from random import random


# this bot is based on
# https://www.youtube.com/watch?v=6g4O5UOH304
#         tutorial, but without TensorFlow :3


class UniversalNode:
    def __init__(self):
        self.value = .5
        self.parent_nodes = []

    def add_parent_node(self, parent_node):
        self.parent_nodes.append({
            'node': parent_node,
            'weight': .5,
        })

    def calculate_value(self):
        val = 0
        for i in range(len(self.parent_nodes)):
            link = self.parent_nodes[i]
            val += link['node'].value * link['weight']
        self.value = positive_sigmoid(val)


def get_neurons(input_num, output_num):
    input_nodes = []
    output_nodes = []

    for i in range(input_num):  # two for each cell
        input_nodes.append(UniversalNode())

    for i in range(output_num):
        out_node = UniversalNode()
        for node in input_nodes:
            out_node.add_parent_node(node)
        output_nodes.append(out_node)

    return input_nodes, output_nodes


# todo sigmoid func returns value from 0 to 1
def positive_sigmoid(value):
    return value


class DeepLearningBot(Controller):
    def __init__(self):
        super().__init__()
        self.input_nodes, self.output_nodes = get_neurons(9 * 2, 9)

    def make_turn(self, desk):
        # set values to input nodes
        coord = 0
        me = desk.turn
        for i in range(len(desk.desk)):
            for j in range(len(desk.desk[i])):
                value = desk.desk[i][j]

                # 'contains something' = 1, 'empty' = 0
                self.input_nodes[coord].value = int(value != desk_consts['empty'])

                # 'me' = 1, 'not me' = 0
                self.input_nodes[coord + 1].value = int(value != desk_consts[me])
                coord += 2

        # calculate values in output nodes
        summa = 0
        for i in range(len(self.output_nodes)):
            node = self.output_nodes[i]
            node.calculate_value()
            summa += node.value

        # get one node randomly more value - more chance to be chosen
        rand_val = random() * summa
        summa = 0
        chosen_index = 0
        for i in range(len(self.output_nodes)):
            node = self.output_nodes[i]
            summa += node.value
            if summa >= rand_val:
                chosen_index = i
                break

        return id_to_coord(len(desk.desk[0]), chosen_index)

    def game_ended(self, desk, state):
        # history = desk.history
        return
