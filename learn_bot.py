from bots_and_uis.perceptron_bot import PerceptronBot
import json

with open('bots_and_uis/perceptron_bot_experience/dataset.json') as json_file:
    loaded = json.load(json_file)
    inp = loaded["inputs"]
    out = loaded["outputs"]

# learn bot

perc = PerceptronBot('mySave', 9, 9, 9, 9)
perc.network.learn(inp, out)
perc.save_experience()
