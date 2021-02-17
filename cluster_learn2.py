import random
import numpy as np
import matplotlib.pyplot as plt
from geister2 import Geister2
from vsenv import VsEnv
from vsenvs import VsEnvs
from reinforce_agent import REINFORCEAgent
from random_agent import RandomAgent


def cluster_learn2():
    """発表のグラフ作成用"""
    seed = 122
    file_name = "weights/weights_17/reinforce_"
    agents_len = 9
    max_episodes = 5000
    plt_intvl = max_episodes/10
    plt_bttl = 200
    linestyles = [':', '--', '-.']  # alphaに相当 # linestyle=(0, (1, 0))
    plt_colors = ['r', 'g', 'b']  # betaに相当,mマゼンタ(紫),cシアン(青緑)
    linestyle_avg = '-'
    plt_color_avg = 'k'
    alphas = [0.003, 0.005, 0.01]
    betas = [0.0003, 0.0005, 0.001]
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
    denv = VsEnv(rnd_agent, game, seed)
    for episode in range(max_episodes):
        # 学習個体を一度ずつ選ぶ(順番はランダム)
        for i in rnd.sample(range(agents_len), agents_len):  # -> [2, 0, 1]など
            # i = rnd.randrange(agents_len)  # 学習個体はランダム
            # # 対戦相手は，全ての候補を一度ずつ選ぶ(順番はランダム)
            # for j in rnd.sample(range(agents_len), agents_len):
            agent = agents[i]
            agent.learn(env, max_episodes=1)
        # 定期的にランダムとの対戦結果を描画
        if (episode) % plt_intvl == 0:
            episodes_x.append(episode)
            plt.clf()
            opponent = rnd_agent
            denv._opponent = opponent
            avgs = []
            for i in range(agents_len):
                agent = agents[i]
                theta = agent.theta
                r_list = np.zeros(plt_bttl)
                for bttl_i in range(plt_bttl):
                    afterstates = denv.on_episode_begin(agent.init_red())
                    x = agent.get_x(afterstates)
                    a = agent.get_act(x, theta)
                    for t in range(300):
                        r, nafterstates = denv.on_action_number_received(a)
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

    # numpyに変換し，グラフの情報を保存
    np.save(file_name+"x_list", np.array(x_list))
    np.save(file_name+"avg_y", np.array(avg_y))
    np.save(file_name+"results_y", np.array(results_y))


def selfplay(file_name, agent=None):
    """発表のグラフ作成用"""
    seed = 0
    max_episodes = 50000
    plt_intvl = max_episodes/10
    plt_bttl = 200
    linestyle = '-'  # alphaに相当 # linestyle=(0, (1, 0))
    plt_color = 'k'  # betaに相当,mマゼンタ(紫),cシアン(青緑)
    alpha = 0.001
    beta = 0.0001

    game = Geister2()
    np.random.seed(seed)
    if agent is None:
        agent = REINFORCEAgent(game, seed)
        agent.w = np.zeros(agent.W_SIZE)
        agent.theta = np.zeros(agent.T_SIZE)
    agent.alpha = alpha
    agent.beta = beta

    episodes_x = []
    results_y = []
    rnd_agent = RandomAgent(game, seed*2+1)
    env = VsEnv(agent, game, seed)
    denv = VsEnv(rnd_agent, game, seed)
    for episode in range(max_episodes):
        agent.alpha = alpha * (1 - episode/max_episodes)
        agent.beta = beta * (1 - episode/max_episodes)
        agent.learn(env, max_episodes=1)
        # 定期的にランダムとの対戦結果を描画
        if (episode) % plt_intvl == 0:
            episodes_x.append(episode)
            plt.clf()
            opponent = rnd_agent
            denv._opponent = opponent
            theta = agent.theta
            r_list = np.zeros(plt_bttl)
            for bttl_i in range(plt_bttl):
                afterstates = denv.on_episode_begin(agent.init_red())
                x = agent.get_x(afterstates)
                a = agent.get_act(x, theta)
                for t in range(300):
                    r, nafterstates = denv.on_action_number_received(a)
                    if r != 0:
                        break
                    nx = agent.get_x(nafterstates)
                    na = agent.get_act(nx, theta)
                    x = nx
                    a = na
                r_list[bttl_i] = r
            mean = r_list.mean()
            results_y.append(mean)
            plt.figure(1)
            plt.title('Training...')
            plt.xlabel('Episode')
            plt.ylabel('Mean Results')
            x_list = np.array(episodes_x)
            y_list = np.array(results_y)
            plt.plot(x_list, y_list,
                     linestyle=linestyle,
                     c=plt_color)
            plt.pause(0.01)  # pause a bit so that plots are updated
    plt.savefig(file_name+str(".png"))
    # selfplay向けに変更
    np.save(file_name+"_w", agent.w)
    np.save(file_name+"_theta", agent.theta)

    # numpyに変換し，グラフの情報を保存
    np.save(file_name+"x_list", np.array(x_list))
    np.save(file_name+"results_y", np.array(results_y))


if __name__ == "__main__":
    import load_
    i = 14
    while(True):
        past_path = "weights/weights_17/vsself"+str(i)
        file_name = "weights/weights_17/vsself"+str(i+1)
        game = Geister2()
        agent = load_.load_agent(past_path, game, seed=0)
        selfplay(file_name, agent)
        i += 1
