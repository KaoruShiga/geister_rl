from geister2 import Geister2
from vsenv import VsEnv
from tdagent import TDAgent
from random_agent import RandomAgent

seed = 3
game = Geister2()
tdagent = TDAgent(game, seed)
rndagent = RandomAgent(game, seed)
env = VsEnv(rndagent, game, seed)
tdagent.learn(env, seed)
for j in range(3):
    for i in range(7):
        print((tdagent.w[i*6+j*(6*6+6):i*6+6+j*(6*6+6)]*1000).round()*(1/1000))
    print("-------------------")
