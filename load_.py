import random
import numpy as np
import matplotlib.pyplot as plt
from geister2 import Geister2
from vsenv import VsEnv
from mcagent import MCAgent
from reinforce_agent import REINFORCEAgent
from random_agent import RandomAgent


def battle2():
    seed = 301
    bttl_num = 50
    game = Geister2()
    agents = [[MCAgent(game, seed+i) for i in range(8)],
              [MCAgent(game, seed+i+8) for i in range(8)]]
    agents_str = ["weights_2/td_learned2_"+str(i)+".npy" for i in range(1, 9)]
    for agent, string in zip(agents[0], agents_str):
        agent.w = load(string)
    agents_str = ["weights_3/td_learned3_"+str(i)+".npy" for i in range(1, 9)]
    for agent, string in zip(agents[1], agents_str):
        agent.w = load(string)
    means = np.zeros(8*8).reshape(8, 8)
    for i in range(8):
        for j in range(8):
            r_list = np.zeros(bttl_num)
            for t in range(bttl_num):
                agent_s = (agents[0][i], agents[1][j])
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
            means[i][j] = r_list.mean()
    print(means)
    print("mean: ", means.mean())


def battle():
    seed = 29
    bttl_num = 10
    game = Geister2()
    agents_str = ["weights/weights_13/reinforce_"+str(i)+"_theta.npy" for i in range(1, 9)]
    agent_len = len(agents_str)
    agents = [REINFORCEAgent(game, seed+i) for i in range(agent_len)]
    for agent, string in zip(agents, agents_str):
        agent.theta = load(string)
    means = np.zeros((agent_len, agent_len))
    for i in range(len(agents)):
        for j in range(i, len(agents)):
            if i == j:
                continue
            r_list = np.zeros(bttl_num)
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
            means[i][j] = r_list.mean()
            means[j][i] = -means[i][j]
    print(means)


def battle_vsrandom():
    seed = 29
    bttl_num = 1
    game = Geister2()
    agents = [[MCAgent(game, seed+i) for i in range(8)],
              [MCAgent(game, seed+i+8) for i in range(8)]]
    agents_str = ["weights/td_"+str(i)+".npy" for i in range(1, 9)]
    for agent, string in zip(agents[0], agents_str):
        agent.w = load(string)
    agents_str = ["weights_2/td_learned2_"+str(i)+".npy" for i in range(1, 9)]
    for agent, string in zip(agents[1], agents_str):
        agent.w = load(string)
    rndagent = RandomAgent(game, seed-1)
    means = np.zeros((2, 8))
    for i in range(2):
        for j in range(len(agents[i])):
            r_list = np.zeros(bttl_num)
            for t in range(bttl_num):
                agent_s = (agents[i][j], rndagent)
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
            means[i][j] = r_list.mean()
    print(means)
    print(means.mean(axis=1))


def load_list(str_list, len=None):
    dst = []
    for str in str_list:
        dst.append(load(str))
    return dst


def load(str, len=None):
    dst = np.load(str)
    assert((len is None) or (len(dst) == len))
    return dst


def load_agent(ps_name, game, seed=None):
    agent = REINFORCEAgent(game, seed)
    agent.w = load(ps_name + '_w.npy')
    agent.theta = load(ps_name + '_theta.npy')
    return agent


def load_agents(pass_list, game, seed=None):
    agents = []
    for ps_name in pass_list:
        agents.append(load_agent(ps_name, game, seed))
        seed += 1
    return agents


if __name__ == "__main__":
    battle()
