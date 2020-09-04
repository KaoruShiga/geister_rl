import unittest
import numpy as np
from geister2 import Geister2
from vsenv import VsEnv
from tdagent import TDAgent
from random_agent import RandomAgent


class TestActFromQ(unittest.TestCase):
    def setUp(self):
        self.S_SIZE = VsEnv(None, None).S_SIZE
        self.w = np.array([
            0.9, 0, 0, 0, 0, 0,
            0.8, 0, 0, 0, 0, 0,
            0.7, 0, 0, 0, 0, 0,
            0.6, 0, 0, 0, 0, 0,
            0.5, 0, 0, 0, 0, 0,
            0.1, 0, 0, 0, 0, 0,
            0,   0, 0, 0, 0, 1,

            0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0,

            0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0
        ])
        self.w2 = np.array([
            0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0.1, 0,

            0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0,

            0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0
        ])

    # テストは一例のみ()
    def test_get_1ht_afterstates(self):
        seed = 0
        game = Geister2()

        tdagent = TDAgent(game, seed)
        tdagent.w = self.w2
        tdagent.S_SIZE = self.S_SIZE
        rndagent = RandomAgent(game, seed)
        agents = (tdagent, rndagent)
        init_red0, init_red1 = (agent.init_red() for agent in agents)
        turn = 0
        max = 100
        for _ in range(max):
            game.__init__()
            game.setRed(init_red0)
            game.changeSide()
            game.setRed(init_red1)
            game.changeSide()
            while not game.is_ended():
                agent = agents[0]
                afterstate = game.after_states()
                act_i = agent.get_act_afterstates(afterstate)
                game.on_action_number_received(act_i)
                game.changeSide()
                if game.is_ended():
                    break

                agent = agents[1]
                afterstate = game.after_states()
                act_i = agent.get_act_afterstates(afterstate)
                game.on_action_number_received(act_i)
                game.changeSide()
                # game.printBoard()

            print(game._turn)
            turn += game._turn
        print(turn/max)


if __name__ == "__main__":
    unittest.main()
