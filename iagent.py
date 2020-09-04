import random


class IAgent:
    def get_act_afterstates(self, states):
        act_i = 0
        raise Exception
        return act_i

    def get_next_action(self, state):
        action = 0
        raise Exception
        return action

    def init_red(self):
        arr = ["A", "B", "C", "D", "E", "F", "G", "H"]
        raise Exception
        return arr

    def __init__(self, game, seed=1):
        self._game = game
        self._rnd = random.Random(seed)
        raise Exception
