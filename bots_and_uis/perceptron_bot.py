from random import random

from bots_and_uis.neural_network_bot import desk_to_inputs
from bots_and_uis.console_game import id_to_coord
import json
from bots_and_uis.controller import Controller
import numpy as np
from typing import Dict, List, Union

experience_data_folder = 'bots_and_uis/perceptron_bot_experience/'


def sigmoid(x: Union[int, float, np.ndarray]) -> float:
    return 1 / (1 + np.exp(-x))


def deriv_sigmoid(x: Union[int, float, np.ndarray]) -> float:
    fx = sigmoid(x)
    return fx * (1 - fx)


class Rumelhart:
    def __init__(self, layer_1: int, layer_2: int, *other_layers: int):
        layers = [layer_1, layer_2] + list(other_layers)
        self._synapses = []
        self._biases = []
        for i in range(len(layers) - 1):
            self._synapses.append((2 * np.random.random((layers[i], layers[i + 1])) - 1))
            self._biases.append((2 * np.random.random(layers[i + 1]) - 1))

    def feedforward(self, inp: Union[List[float], np.ndarray]) -> List[float]:
        li = np.array(inp)
        for i in range(len(self._synapses)):
            li = sigmoid(np.dot(li, self._synapses[i]) + self._biases[i])
        return li.tolist()

    @property
    def raw(self) -> Dict[str, list]:
        return {
            "synapses": [x.tolist() for x in self._synapses],
            "biases": [x.tolist() for x in self._biases]
        }

    @raw.setter
    def raw(self, raw: Dict[str, list]):
        self._synapses = [np.array(x) for x in raw["synapses"]]
        self._biases = [np.array(x) for x in raw["biases"]]

    def learn(self,
              inp: List[List[float]],
              out: List[List[float]],
              epochs: int = 100000,
              learning_rate: Union[float, int] = .1,
              err_print: bool = True,
              err_print_frequency: int = 10000,
              ):
        inp = np.array(inp)
        out = np.array(out)
        for epoch in range(epochs):
            Si = [inp]
            Xi = [sigmoid(Si[-1])]
            for i in range(len(self._synapses)):
                Si.append(np.dot(Xi[i], self._synapses[i]) + self._biases[i])
                Xi.append(sigmoid(Si[-1]))

            Ei = [out - Xi[-1]]
            for i in range(len(Xi) - 2, 0, -1): Ei.insert(0, Ei[0].dot(self._synapses[i].T))

            for i in range(len(self._synapses)):
                grad = np.multiply(Ei[i], deriv_sigmoid(Si[i + 1]))
                dw = np.dot(grad.T, Xi[i]).T
                self._synapses[i] += dw * learning_rate
                self._biases[i] += np.mean(dw, axis=0) * learning_rate

            if err_print and (epoch % err_print_frequency) == 0:
                print("Error: ", str(np.mean(np.abs(Ei[-1]))))


class PerceptronBot(Controller):
    def __init__(self,
                 tag: str = None,  # name with which will be saved and load exp
                 *layers: int
                 ):
        super().__init__()
        self.network: Rumelhart = Rumelhart(*layers)
        self.tag: str = tag

    def load_experience(self):
        with open(experience_data_folder + self.tag + '.json') as json_file:
            self.network.raw = json.load(json_file)

    def save_experience(self):
        with open(experience_data_folder + self.tag + '.json', "w") as write_file:
            json.dump(self.network.raw, write_file)

    def make_turn(self, desk):
        inputs = desk_to_inputs(desk.desk, desk.turn)
        outputs = self.network.feedforward(inputs)

        for i in range(len(outputs)):
            if inputs[i] != -1:
                outputs[i] = 0

        chosen_index = 0
        for i in range(len(outputs)):
            if outputs[i] > outputs[chosen_index]:
                chosen_index = i

        coords = id_to_coord(len(desk.desk), chosen_index)
        return coords
