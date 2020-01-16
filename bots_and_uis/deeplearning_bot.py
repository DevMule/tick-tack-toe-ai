from bots_and_uis.controller import Controller
# this bot is based on
# https://www.youtube.com/watch?v=6g4O5UOH304
#                                    tutorial


class DeepLearningBot(Controller):
    def make_turn(self, desk):
        return [0, 0]

    def game_ended(self, desk, state):
        return
