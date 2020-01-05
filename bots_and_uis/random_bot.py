from bots_and_uis.controller import Controller
from random import randint as rand


class RandomBot(Controller):
    def make_turn(self, desk):
        h = len(desk)
        w = len(desk[0])
        return self.pick_random(desk, w, h)

    def pick_random(self, desk, w, h):
        x = rand(w)
        y = rand(h)
        while desk[y][x] != -1:
            x = rand(w)
            y = rand(h)
        return [x, y]
