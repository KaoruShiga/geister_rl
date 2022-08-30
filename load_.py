import numpy as np
from reinforce_agent import REINFORCEAgent


def load_list(str_list, len=None):
    dst = []
    for str in str_list:
        dst.append(load(str))
    return dst


def load(str, len=None):
    dst = np.load(str)
    assert((len is None) or (len(dst) == len))
    return dst


def load_agent(ps_name, game, seed=None, AgentClass=REINFORCEAgent):
    agent = AgentClass(game, seed)
    agent.w = load(ps_name + '_w.npy')
    agent.theta = load(ps_name + '_theta.npy')
    return agent


def load_agents(path_list, game, seed=None, AgentClass=REINFORCEAgent):
    agents = []
    for ps_name in path_list:
        agents.append(load_agent(ps_name, game, seed, AgentClass=AgentClass))
        if not(seed is None):
            seed += 1
    return agents
