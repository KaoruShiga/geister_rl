import numpy as np
from geister2 import Geister2
from battle import battle, battle2
from load_ import load_agent, load_agents

seed = None
game = Geister2()
folder_path = "weights/vsself2"
agents50 = load_agents([folder_path+"/vsself"+str(i) for i in range(45, 56)], game)
agents100 = load_agents([folder_path+"/vsself"+str(i) for i in range(95, 106)], game)
agents150 = load_agents([folder_path+"/vsself"+str(i) for i in range(145, 156)], game)
mat150vs100 = battle2(agents150, agents100, seed=seed, bttl_num=100)
mat150vs50 = battle2(agents150, agents50, seed=seed, bttl_num=100)
mat100vs50 = battle2(agents100, agents50, seed=seed, bttl_num=100)

mat150vs100
mat150vs50
mat100vs50

agent1 = load_agent(folder_path+"/vsself1", game)
agent150 = load_agent(folder_path+"/vsself150", game)
battle(agent150, agent1, seed=seed, bttl_num=1000)  # 0.92(出力結果)
agent150_b = load_agent("weights/weights_17/vsself30", game)
agent50_b = load_agent("weights/weights_17/vsself10", game)
agent100_b = load_agent("weights/weights_17/vsself10", game)
battle(agent150_b, agent1, seed=seed, bttl_num=1000)  # 0.90(出力結果)
battle(agent150_b, agent50_b, seed=seed, bttl_num=1000)  # 0.764(勝率)
battle(agent150_b, agent100_b, seed=seed, bttl_num=1000)  # 0.78(勝率)

agent150 = load_agent(folder_path+"/vsself150", game)
agent50 = load_agent(folder_path+"/vsself50", game)
agent100 = load_agent(folder_path+"/vsself100", game)
battle(agent150, agent100, seed=seed, bttl_num=12100)  #
battle(agent150, agent50, seed=seed, bttl_num=12100)  #
battle(agent100, agent50, seed=seed, bttl_num=12100)  #


agents = load_agents([folder_path+"/vsself"+str(i) for i in range(50, 370, 50)], game)
mat = battle2(agents, agents, seed=seed, bttl_num=10000)
