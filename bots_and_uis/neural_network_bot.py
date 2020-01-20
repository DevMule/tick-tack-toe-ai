from bots_and_uis.controller import Controller
from bots_and_uis.console_game import id_to_coord, coord_to_id
from desk.desk import desk_consts
import json
import numpy as np

# this bot is based on
# https://www.youtube.com/watch?v=6g4O5UOH304
# https://python-scripts.com/intro-to-neural-networks
#                                           tutorials
experience_data_folder = 'bots_and_uis/neural_network_bot_experience/'

game_result_weights = {
    "WIN": 1,
    "TIE": .2,
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
            # преобразовать поле таким образом, чтобы бот всегда видел свою фигуру как "X"
            if value != desk_consts['empty'] and my_figure != 'X':
                value = 1 - value
            inputs.append(value)

            # 'contains something' = 1, 'empty' = 0
            # inputs.append(int(value != desk_consts['empty']))

            # 'me' = 1, 'not me' = 0
            # inputs.append(int(value != desk_consts[my_figure]))
    return inputs


class NeuralNetworkBot(Controller):
    def __init__(self,
                 inputs=9,
                 hidden=81,
                 outputs=9,
                 learning=False,  # будет ли бот изменять свой опыт
                 new_experience=False,  # если истина, то бот создаст новый опыт, иначе загрузит старый
                 learn_rate=0.05,  # коэффициент изменения весов за один проход обучения
                 learn_decrease_coef=.75  # коэффициент, с которым падает вес изучения для каждого предыдущего шага
                 ):
        super().__init__()

        # learning values
        self.learning = learning  # do learn something new
        self.learn_rate = learn_rate
        self.learn_decrease_coef = learn_decrease_coef

        # neurons
        if new_experience:
            self._hidden_neurons = []
            self._output_neurons = []
            for i in range(hidden):
                weights = [.5 for x in range(inputs)]
                self._hidden_neurons.append(Neuron(weights))

            for i in range(outputs):
                weights = [.5 for x in range(hidden)]
                self._output_neurons.append(Neuron(weights))
        else:
            self._hidden_neurons, self._output_neurons = self.load_experience(inputs, hidden, outputs)

    def load_experience(self, inputs, hidden, outputs):
        # name = exp_9_81_9.json
        name = experience_data_folder + 'exp_' + str(inputs) + '_' + str(hidden) + '_' + str(outputs) + '.json'
        with open(name) as json_file:
            data = json.load(json_file)
            return [Neuron(data['hidden'][x]['weights'], data['hidden'][x]['bias'])
                    for x in range(len(data['hidden']))], \
                   [Neuron(data['outputs'][x]['weights'], data['outputs'][x]['bias'])
                    for x in range(len(data['outputs']))]

    def save_experience(self):
        # name = exp_9_81_9.json
        name = experience_data_folder + 'exp_' + \
               str(len(self._hidden_neurons[0].weights)) + '_' + \
               str(len(self._hidden_neurons)) + '_' + \
               str(len(self._output_neurons)) + '.json'

        data = {
            'inputs': len(self._hidden_neurons[0].weights),
            'hidden': [{
                'weights': neuron.weights,
                'bias': neuron.bias
            } for neuron in self._hidden_neurons],
            'outputs': [{
                'weights': neuron.weights,
                'bias': neuron.bias
            } for neuron in self._output_neurons],
        }

        with open(name, "w") as write_file:
            json.dump(data, write_file)

    def make_turn(self, desk):
        # set values to input nodes
        inputs = desk_to_inputs(desk.desk, desk.turn)

        # calculate values in output nodes
        outputs = self.feedforward(inputs)

        # make disable to choose not empty space
        for i in range(len(outputs)):
            if inputs[i] != -1:
                outputs[i] = 0

        chosen_index = 0
        for i in range(len(outputs)):
            if outputs[i] > outputs[chosen_index]:
                chosen_index = i
        '''
        summa = np.sum(outputs)

        # get one node randomly more value - more chance to be chosen
        rand_val = random() * summa
        summa = 0
        chosen_index = 0
        for i in range(len(outputs)):
            summa += outputs[i]
            if summa >= rand_val:
                chosen_index = i
                break'''

        coords = id_to_coord(len(desk.desk), chosen_index)
        return coords

    def feedforward(self, inputs):
        hiddens = []
        for i in range(len(self._hidden_neurons)):
            hiddens.append(self._hidden_neurons[i].feedforward(inputs))

        outputs = []
        for i in range(len(self._output_neurons)):
            outputs.append(self._output_neurons[i].feedforward(hiddens))

        return outputs

    def game_ended(self, desk, state, my_figure):
        if not self.learning:
            return

        TEMPORARY_LEARN_RATE = self.learn_rate
        # fixme переписывать свои проигрыши - плохая идея,
        #  ведь бот ходит всегда таким способом, который изучил чуть ранее
        #  потому стоит преимущественно заучивать победные ходы, и отучиваться
        #  только от самых дерьмовых, например, свой последний ход при проигрыше
        #  и как итог - бот постоянно находится в состоянии переписывания правильных ходов другими "правильными"
        #  ...
        #  попробую сделать это так: каждый предыдущий ход имеет сдвиг на меньший коэффициент относительно предыдущего
        true_value = game_result_weights[state]
        history = desk.history

        # если ничья, то не переделываем ничего
        # if state == 'TIE':
        #    return

        for story in history[::-1]:
            learning_figure = my_figure
            if state == "WIN":  # если выиграли - закрепляем свои ходы
                if story[2] == my_figure:
                    learning_figure = my_figure
                    true_value = 1
                else:  # и учимся не ходить как враг
                    learning_figure = desk_consts[1 - desk_consts[my_figure]]
                    true_value = 0

            elif state == "FAIL":  # если проиграли - отучиваемся ходить как раньше
                if story[2] == my_figure:
                    learning_figure = my_figure
                    true_value = 0
                else:  # и учимся ходить как враг
                    learning_figure = desk_consts[1 - desk_consts[my_figure]]
                    true_value = 1

            else:  # если ничья, то уменьшаем веса своего хода
                learning_figure = my_figure
                true_value = 0

            inputs = desk_to_inputs(story[0], learning_figure)
            outputs = []
            for i in range(len(inputs)):
                if i == coord_to_id(len(story[0]), story[1][1], story[1][0]):
                    outputs.append(true_value)
                else:
                    outputs.append((1 - true_value) / (len(inputs) - 1))

            # print(inputs, outputs)

            self.train(inputs, outputs)
            self.learn_rate *= self.learn_decrease_coef
        self.learn_rate = TEMPORARY_LEARN_RATE

    def train(self, inputs, outputs):
        for o_id in range(len(outputs)):
            true_value = outputs[o_id]

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
