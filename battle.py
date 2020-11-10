import random
import numpy as np
import matplotlib.pyplot as plt
from geister2 import Geister2
from vsenv import VsEnv
from mcagent import MCAgent
from reinforce_agent import REINFORCEAgent
from random_agent import RandomAgent
from load_ import load_agent


def battle(agent1, agent2, bttl_num=1, seed=None):
    game = Geister2()
    results = np.zeros(bttl_num)
    agents = [agent1, agent2]
    for t in range(bttl_num):
        arr0, arr1 = (agent.init_red() for agent in agents)
        game.__init__()
        game.setRed(arr0)
        game.changeSide()
        game.setRed(arr1)
        game.changeSide()
        player = 0
        while not game.is_ended():
            agent = agents[player]
            states = game.after_states()
            i_act = agent.get_act_afterstates(states)
            game.on_action_number_received(i_act)
            game.changeSide()

            player = (player+1) % 2
        if player == 1:
            game.changeSide()
        result = game.checkResult()
        r = (1 if (result > 0) else (-1 if (result < 0) else 0))
        results[t] = r
    return results.mean()


if __name__ == "__main__":
    seed = 100
    geister = Geister2()
    agent1 = load_agent("weights/rfvsrnd4", geister, seed)
    agent2 = load_agent("weights/rfvsrnd3", geister, seed)
    results = battle(agent1, agent2, 100)
    print(results)
