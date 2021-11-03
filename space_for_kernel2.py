import numpy as np
from geister2 import Geister2
from battle import battle, battle2, battle2_get_results
from load_ import load_agent, load_agents
from greedy_agent import GreedyAgent
seed = None
game = Geister2()
folder_path = "weights/vsself3"

agents = load_agents([folder_path+"/vsself"+str(i) for i in range(0, 949, 79)], game)
random_agent = load_agent(folder_path+"/vsself0", game)
mat = battle2_get_results(agents, [agents[2]], seed=seed, bttl_num=10)
mat[:,:,:]
x_list = list(range(0, 949, 79))
x_list
