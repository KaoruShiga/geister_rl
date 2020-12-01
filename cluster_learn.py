import random
import numpy as np
import matplotlib.pyplot as plt
from geister2 import Geister2
from vsenv import VsEnv
from reinforce_agent import REINFORCEAgent
from random_agent import RandomAgent


def cluster_learn():
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
    env = VsEnv(agents[0], game, seed)
    for episode in range(max_episodes):
        # 学習個体を一度ずつ選ぶ(順番はランダム)
        for i in rnd.sample(range(agents_len), agents_len):  # -> [2, 0, 1]など
            # i = rnd.randrange(agents_len)  # 学習個体はランダム
            # # 対戦相手は，全ての候補を一度ずつ選ぶ(順番はランダム)
            # for j in rnd.sample(range(agents_len), agents_len):
            j = rnd.randrange(agents_len)  # 対戦相手はランダムに一度だけ
            agent = agents[i]
            env._opponent = agents[j]
            agent.learn(env, max_episodes=1)
        # 定期的にランダムとの対戦結果を描画
        if (episode+1) % plt_intvl == 0:
            episodes_x.append(episode)
            plt.clf()
            opponent = rnd_agent
            env._opponent = opponent
            avgs = []
            for i in range(agents_len):
                agent = agents[i]
                theta = agent.theta
                r_list = np.zeros(plt_bttl)
                for bttl_i in range(plt_bttl):
                    afterstates = env.on_episode_begin(agent.init_red())
                    x = agent.get_x(afterstates)
                    a = agent.get_act(x, theta)
                    for t in range(300):
                        r, nafterstates = env.on_action_number_received(a)
                        if r != 0:
                            break
                        nx = agent.get_x(nafterstates)
                        na = agent.get_act(nx, theta)
                        x = nx
                        a = na
                    r_list[bttl_i] = r
                mean = r_list.mean()
                avgs.append(mean)
                results_y[i].append(mean)
                plt.figure(1)
                plt.title('Training...')
                plt.xlabel('Episode')
                plt.ylabel('Mean Results')
                x_list = np.array(episodes_x)
                y_list = np.array(results_y[i])
                plt.plot(x_list, y_list,
                         linestyle=linestyles[i % len(alphas)],
                         c=plt_colors[i // len(alphas)],
                         label=str(i))
            avg_y.append(np.array(avgs).mean())
            plt.figure(1)
            plt.title('Training...')
            plt.xlabel('Episode')
            plt.ylabel('Mean Results')
            x_list = np.array(episodes_x)
            y_list = np.array(avg_y)
            plt.plot(x_list, y_list,
                     linestyle=linestyle_avg,
                     c=plt_color_avg,
                     label=agents_len)
            plt.pause(0.01)  # pause a bit so that plots are updated
    plt.savefig(file_name+str(".png"))
    plt.show()
    for i in range(agents_len):
        np.save(file_name+str(i+1)+"_w", agents[i].w)
        np.save(file_name+str(i+1)+"_theta", agents[i].theta)


if __name__ == "__main__":
    cluster_learn()
