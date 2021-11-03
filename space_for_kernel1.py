import numpy as np
from geister2 import Geister2
from battle import battle, battle2, battle2_get_results
from load_ import load_agent, load_agents
from greedy_agent import GreedyAgent
seed = None
game = Geister2()
folder_path = "weights/vsself2"

agents = load_agents([folder_path+"/vsself"+str(i) for i in range(50, 450, 50)], game)
mat = battle(agents[-1], agents[-3], seed=seed, bttl_num=10000)
mat/2+0.5

agents = load_agents([folder_path+"/vsself"+str(i) for i in range(100, 510, 100)], game)
mat = battle2_get_results(agents, agents, seed=seed, bttl_num=10000, isGreedy=True)
mat[:,:,:]

agent100 = load_agent(folder_path+"/vsself100", game, AgentClass=GreedyAgent)
agent300 = load_agent(folder_path+"/vsself300", game, AgentClass=GreedyAgent)
agent500 = load_agent(folder_path+"/vsself500", game, AgentClass=GreedyAgent)
agent600 = load_agent(folder_path+"/vsself600", game, AgentClass=GreedyAgent)
agent700 = load_agent(folder_path+"/vsself700", game, AgentClass=GreedyAgent)
agent800 = load_agent(folder_path+"/vsself800", game, AgentClass=GreedyAgent)
agent900 = load_agent(folder_path+"/vsself900", game, AgentClass=GreedyAgent)

mat = battle2_get_results([agent600], [agent600], seed=seed, bttl_num=10000)
mat
mat2 = battle2_get_results([agent800], [agent800], seed=seed, bttl_num=10000)
mat2
agent200 = load_agent(folder_path+"/vsself200", game, AgentClass=GreedyAgent)
mat3 = battle2_get_results([agent200], [agent200], seed=seed, bttl_num=10000)
mat3

win_rates = [1-(mat[0]+mat[1]/2)/10000 for mat in mat3]
win_rates += [0.5, 0.641525, 0.53625, 0.66755, 0.625075]
y_list = win_rates
x_list = list(range(0, 100, 20)) + list(range(100, 1000, 200))
x_list
y_list
