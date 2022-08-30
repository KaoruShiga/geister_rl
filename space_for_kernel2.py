import numpy as np
from geister2 import Geister2
from battle import battle, battle2, battle2_get_results
from load_ import load_agent, load_agents
from greedy_agent import GreedyAgent
seed = None
game = Geister2()
folder_path = "weights/vsself4"

agents = load_agents([folder_path+"/vsself"+str(i) for i in range(0, 351, 50)], game)
pastagent = load_agent("weights/vsself2/vsself500", game)

mat = battle2(agents, [pastagent], seed=seed, bttl_num=100)
mat
