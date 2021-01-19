import random
import numpy as np
import matplotlib.pyplot as plt
from geister2 import Geister2
from vsenvs import VsEnvs
from reinforce_agent import REINFORCEAgent
from random_agent import RandomAgent


def cluster_learn2():
    """発表のグラフ作成用"""
    seed = 122
    file_name = "weights/weights_16/reinforce_"
    agents_len = 18
    max_episodes = 500*(agents_len)
    plt_intvl = 50*(agents_len)
    plt_bttl = 200
    linestyles = [':', '--', '-.']  # alphaに相当 # linestyle=(0, (1, 0))
    plt_colors = ['m', 'r', 'g', 'c', 'b', 'y']  # betaに相当,mマゼンタ(紫),cシアン(青緑)
    linestyle_avg = '-'
    plt_color_avg = 'k'
    alphas = [0.003, 0.005, 0.01]
    betas = [0.0005, 0.0001, 0.0003, 0.0005, 0.001, 0.0015]
    assert(len(linestyles) == len(alphas))
    assert(len(plt_colors) == len(betas))
    assert(len(alphas)*len(betas) == agents_len)

    game = Geister2()
    np.random.seed(seed)
    rnd = random.Random(seed)
    agents = [REINFORCEAgent(game, seed+i) for i in range(agents_len)]
    for i in range(len(alphas)):
        for j in range(len(betas)):
            agents[i+j*len(alphas)].alpha = alphas[i]
            agents[i+j*len(alphas)].beta = betas[j]
    # 重みを小さな正規乱数で初期化
    for agent in agents:
        if agent.w is None:
            agent.w = np.zeros(agent.W_SIZE)
        if agent.theta is None:
            agent.theta = np.zeros(agent.T_SIZE)

    episodes_x = []
    results_y = [[] for _ in range(agents_len)]
    avg_y = []
    rnd_agent = RandomAgent(game, seed*2+1)
    env = VsEnvs(agents, game, seed)
    for episode in range(max_episodes):
        # 学習個体を一度ずつ選ぶ(順番はランダム)
        for i in rnd.sample(range(agents_len), agents_len):  # -> [2, 0, 1]など
            # i = rnd.randrange(agents_len)  # 学習個体はランダム
            # # 対戦相手は，全ての候補を一度ずつ選ぶ(順番はランダム)
            # for j in rnd.sample(range(agents_len), agents_len):
            agent = agents[i]
            agent.learn(env, max_episodes=1, dtaw_mode=True, draw_opp=rnd_agent)
    plt.savefig(file_name+str(".png"))
    plt.show()
    for i in range(agents_len):
        np.save(file_name+str(i+1)+"_w", agents[i].w)
        np.save(file_name+str(i+1)+"_theta", agents[i].theta)


if __name__ == "__main__":
    cluster_learn2()
