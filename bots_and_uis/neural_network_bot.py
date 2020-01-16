from bots_and_uis.controller import Controller
from bots_and_uis.console_game import id_to_coord, coord_to_id, print_desk
from desk.desk import desk_consts
from random import random
import numpy as np

# this bot is based on
# https://www.youtube.com/watch?v=6g4O5UOH304
# https://python-scripts.com/intro-to-neural-networks
#                                           tutorials


game_result_weights = {
    "WIN": 1,
    "TIE": .1,
    "FAIL": 0,
}


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
    for i in range(len(desk)):
        for j in range(len(desk[i])):
            value = desk[i][j]

            # 'contains something' = 1, 'empty' = 0
            inputs.append(int(value != desk_consts['empty']))

            # 'me' = 1, 'not me' = 0
            inputs.append(int(value != desk_consts[my_figure]))
    return inputs


class NeuralNetworkBot(Controller):
    def __init__(self, inputs=3 * 3, learn_rate=0.1, epochs=25):
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
        # print(outputs)
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

        return id_to_coord(len(desk.desk), chosen_index)

    def feedforward(self, inputs):
        hiddens = []
        for i in range(len(self._hidden_neurons)):
            hiddens.append(self._hidden_neurons[i].feedforward(inputs))

        outputs = []
        for i in range(len(self._output_neurons)):
            outputs.append(self._output_neurons[i].feedforward(hiddens))

        return outputs

    def game_ended(self, desk, state, my_figure):
        true_value = game_result_weights[state]
        history = desk.history
        for story in history[::-1]:
            inputs = desk_to_inputs(story[0], my_figure)
            output_id = coord_to_id(len(story[0]), story[1][1], story[1][0])
            self.train(inputs, output_id, true_value)

    def train(self, inputs, o_id, true_value):
        for epoch in range(self.epochs):

            # calculate hidden layer
            hidden_summas = []  # sum(i)
            hidden_values = []  # h(i)
            for i in range(len(self._hidden_neurons)):
                hidden_sum = np.dot(self._hidden_neurons[i].weights, inputs) + self._hidden_neurons[i].bias
                hidden_summas.append(hidden_sum)
                hidden_values.append(sigmoid(hidden_sum))

            # current value
            output_sum = np.dot(self._output_neurons[o_id].weights, hidden_values) + self._output_neurons[o_id].bias
            deriv_sigmoid_out_sum = deriv_sigmoid(output_sum)
            y_pred = sigmoid(output_sum)

            # --- Подсчет частных производных
            # dL/dY_pred
            dl_dy_pred = -2 * (true_value - y_pred)

            # ------ выходной нейрон O(id) ------
            # задаём производную изменения весов для соединений со скрытыми нейронами
            d_ypred_d_weights = []
            for i in range(len(hidden_values)):
                h = hidden_values[i]
                d_ypred_d_weights.append(h * deriv_sigmoid_out_sum)

            # задаём производную для сдвига для выходного нейрона
            d_ypred_d_bias = deriv_sigmoid(output_sum)

            # задаём производную для изменения для скрытых нейронов
            d_ypred_d_hi_s = []  # dYpred/dh(i)
            for i in range(len(self._output_neurons[o_id].weights)):
                weight = self._output_neurons[o_id].weights[i]
                d_ypred_d_hi_s.append(weight * deriv_sigmoid_out_sum)

            # ------ скрытые нейроны h(i) ------
            hidden_derivatives = []
            for i in range(len(hidden_summas)):
                sum_hi = hidden_summas[i]
                d_hi_d_wj_s = []
                for j in range(len(inputs)):
                    d_hi_d_wj_s.append(inputs[j] * deriv_sigmoid(sum_hi))
                d_hi_d_biasi = deriv_sigmoid(sum_hi)
                hidden_derivatives.append([d_hi_d_wj_s, d_hi_d_biasi])

            # ------ Обновляем вес и смещения ------
            # для h(i)
            for i in range(len(self._hidden_neurons)):
                neuron = self._hidden_neurons[i]
                d_ypred_d_hi = d_ypred_d_hi_s[i]
                for j in range(len(neuron.weights)):
                    d_hi_d_wj = hidden_derivatives[i][0][j]
                    self._hidden_neurons[i].weights[j] -= self.learn_rate * dl_dy_pred * d_ypred_d_hi * d_hi_d_wj
                d_hi_d_bi = hidden_derivatives[i][1]
                self._hidden_neurons[i].bias -= self.learn_rate * dl_dy_pred * d_ypred_d_hi * d_hi_d_bi

            # для выходного нейрона O(id)
            for i in range(len(self._output_neurons[o_id].weights)):
                d_ypred_d_wi = d_ypred_d_weights[i]
                self._output_neurons[o_id].weights[i] -= self.learn_rate * dl_dy_pred * d_ypred_d_wi
            self._output_neurons[o_id].bias -= self.learn_rate * dl_dy_pred * d_ypred_d_bias
