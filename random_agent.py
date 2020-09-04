import random
from iagent import IAgent
from geister import Geister
from geister2 import Geister2


class RandomAgent(IAgent):
    def get_act_afterstates(self, states):
        act_i = self._rnd.randrange(len(states))
        return act_i

    # def get_next_action(self, state):
    #     moves = self._game.getLegalMove()
    #     action = self._rnd.choice(moves)
    #     return action

    def init_red(self):
        arr = ["A", "B", "C", "D", "E", "F", "G", "H"]
        self._rnd.shuffle(arr)
        return arr[0:4]

    def __init__(self, game, seed=1):
        self._game = game
        self._rnd = random.Random(seed)


if __name__ == "__main__":
    game = Geister2()
    agent1 = RandomAgent(game, -1)
    agent2 = RandomAgent(game, 2)
    game.printBoard()
    init1 = agent1.init_red()
    init2 = agent2.init_red()
    game.setRed(init1)
    game.changeSide()
    game.setRed(init2)
    game.changeSide()
    game.printBoard()
    for _ in range(10000):
        while game.checkResult() == 0:
            states = game.after_states()
            game.on_action_number_received(agent1.get_act_afterstates(states))
            game.changeSide()
            if game.checkResult() != 0:
                break
            states = game.after_states()
            game.on_action_number_received(agent2.get_act_afterstates(states))
            game.changeSide()
        game.changeSide()
        game.printAll()
