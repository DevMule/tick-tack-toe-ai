from bots_and_uis.controller import Controller
from random import randint as rand


def pick_random(desk, w, h):
    x = rand(0, w-1)
    y = rand(0, h-1)
    while desk[y][x] != -1:
        x = rand(0, w-1)
        y = rand(0, h-1)
    return [x, y]


class RandomBot(Controller):
    def make_turn(self, desk):
        return pick_random(desk.desk, desk.w, desk.h)
