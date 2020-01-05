from bots_and_uis.controller import Controller
from random import randint as rand


class RandomBot(Controller):
    def make_turn(self, desk):
        h = len(desk.desk)
        w = len(desk.desk[0])
        return self.pick_random(desk.desk, w, h)

    def pick_random(self, desk, w, h):
        x = rand(0, w-1)
        y = rand(0, h-1)
        while desk[y][x] != -1:
            x = rand(0, w-1)
            y = rand(0, h-1)
        return [x, y]
