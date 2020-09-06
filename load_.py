import numpy as np
from geister2 import Geister2
from mcagent import MCAgent
from random_agent import RandomAgent

def battle():
    seed = 50
    bttl_num = 50
    game = Geister2()
    agents_str = ["weights/td_"+str(i)+".npy" for i in range(1, 9)]
    agents = [MCAgent(game, seed+i) for i in range(8)]
    for agent, string in zip(agents, agents_str):
        agent.w = load(string)
        print(agent.w)
    for i in range(len(agents)):
        for j in range(i, len(agents)):
            if i == j:
                continue
            r_list = np.array([0 for _ in range(bttl_num)])
            for t in range(bttl_num):
                agent_s = (agents[i], agents[j])
                arr0, arr1 = (agent.init_red() for agent in agent_s)
                game.__init__()
                game.setRed(arr0)
                game.changeSide()
                game.setRed(arr1)
                game.changeSide()
                player = 0
                while not game.is_ended():
                    agent = agent_s[player]
                    states = game.after_states()
                    i_act = agent.get_act_afterstates(states)
                    game.on_action_number_received(i_act)
                    game.changeSide()

                    player = (player+1) % 2
                if player == 1:
                    game.changeSide()
                result = game.checkResult()
                r = (1 if (result > 0) else (-1 if (result < 0) else 0))
                r_list[t] = r
            print("i: ", i, "j: ", j, "mean: ", r_list.mean())


def load_list(str_list, len=None):
    dst = []
    for str in str_list:
        dst.append(load(str))
    return dst

def load(str, len=None):
    dst = np.load(str)
    assert((len is None) or (len(dst) == len))
    return dst


if __name__=="__main__":
    battle()
