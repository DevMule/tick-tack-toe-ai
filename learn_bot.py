from bots_and_uis.perceptron_bot import PerceptronBot
import json
import numpy as np

with open('bots_and_uis/perceptron_bot_experience/dataset.json') as json_file:
    loaded = json.load(json_file)
    inp = loaded["inputs"]
    out = loaded["outputs"]

# learn bot
np.random.seed(1)
perc = PerceptronBot('mySave', 9, 18, 36, 9)  # error = 0.11111111114856236
perc.network.learn(inp, out)
perc.save_experience()
