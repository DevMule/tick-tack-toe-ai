from bots_and_uis.controller import Controller
from bots_and_uis.console_game import id_to_coord
from desk.desk import desk_consts
from random import random
import numpy as np


# this bot is based on
# https://www.youtube.com/watch?v=6g4O5UOH304
# https://python-scripts.com/intro-to-neural-networks
#                                           tutorials


class Neuron:
    def __init__(self, weights=None, bias=0):
        if weights is None:
            weights = []
        self.weights = weights
        self.bias = bias

    def feedforward(self, inputs):
        total = np.dot(self.weights, inputs) + self.bias
        return sigmoid(total)


def sigmoid(x):
    # Функция активации sigmoid: f(x) = 1 / (1 + e^(-x))
    return 1 / (1 + np.exp(-x))


def deriv_sigmoid(x):
    # Производная от sigmoid: f'(x) = f(x) * (1 - f(x))
    fx = sigmoid(x)
    return fx * (1 - fx)


def mse_loss(y_true, y_pred):
    # y_true и y_pred являются массивами numpy с одинаковой длиной
    return ((y_true - y_pred) ** 2).mean()


def desk_to_inputs(desk, my_figure):
    inputs = []
    for i in range(len(desk.desk)):
        for j in range(len(desk.desk[i])):
            value = desk.desk[i][j]

            # 'contains something' = 1, 'empty' = 0
            inputs.append(int(value != desk_consts['empty']))

            # 'me' = 1, 'not me' = 0
            inputs.append(int(value != desk_consts[my_figure]))
    return inputs


class DeepLearningBot(Controller):
    def __init__(self, inputs=3 * 3, learn_rate=0.1, epochs=250):
        super().__init__()

        # learning values
        self.learn_rate = learn_rate
        self.epochs = epochs  # epochs after game ended

        # neurons
        self._hidden_neurons = []
        self._output_neurons = []
        for i in range(inputs):
            weights = [.5 for x in range(inputs * 2)]
            self._hidden_neurons.append(Neuron(weights))

            weights = [.5 for x in range(inputs)]
            self._output_neurons.append(Neuron(weights))

    def make_turn(self, desk):
        # set values to input nodes
        inputs = desk_to_inputs(desk.desk, desk.turn)

        # calculate values in output nodes
        outputs = self.feedforward(inputs)
        print(outputs)
        summa = np.sum(outputs)

        # get one node randomly more value - more chance to be chosen
        rand_val = random() * summa
        summa = 0
        chosen_index = 0
        for i in range(len(outputs)):
            summa += outputs[i]
            if summa >= rand_val:
                chosen_index = i
                break

        return id_to_coord(len(desk.desk[0]), chosen_index)

    def feedforward(self, inputs):
        hiddens = []
        for i in range(len(self._hidden_neurons)):
            hiddens.append(self._hidden_neurons[i].feedforward(inputs))

        outputs = []
        for i in range(len(self._output_neurons)):
            outputs.append(self._output_neurons[i].feedforward(hiddens))

        return outputs

    def game_ended(self, desk, state):
        history = desk.history
        for state in history[::-1]:


    def train(self, inputs, outputs):
        return
