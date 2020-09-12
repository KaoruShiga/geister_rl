import random
import numpy as np
import matplotlib.pyplot as plt
from geister2 import Geister2
from vsenv import VsEnv
from mcagent import MCAgent
from random_agent import RandomAgent


def cluster_learn():
    seed = 30
    file_name = "mc2_learned3_"
    max_episodes = 1000
    plt_intvl = 100
    plt_bttl = 50
    agents_len = 3
    plt_colors = ['r', 'g', 'b']  # r g b c m y k w
    assert(len(plt_colors) == agents_len)

    game = Geister2()
    np.random.seed(seed)
    rnd = random.Random(seed)
    agents = [MCAgent(game, seed+i) for i in range(agents_len)]
    episodes_x = []
    results_y = [[] for i in range(agents_len)]
    for agent in agents:
        agent.w = np.random.randn(agent.W_SIZE)*agent.alpha*2 + agent.alpha*2
    rnd_agent = RandomAgent(game, seed-1)
    env = VsEnv(agents[0], game, seed)
    for episode in range(max_episodes):
        # 各episodeで一度ずつ学習し，その相手も候補すべてに対して行うが，順番はランダム
        for i in rnd.sample(range(agents_len), agents_len):  # -> [2, 1, 0]など
            for j in rnd.sample(range(agents_len), agents_len):
                # i = rnd.randrange(agents_len)
                # j = rnd.randrange(agents_len)
                # j = rnd.randrange(agents_len-1)
                # j += (1 if (i == j) else 0)
                agent = agents[i]
                w = agent.w
                alpha = agent.alpha
                env._opponent = agents[j]
                afterstates = env.on_episode_begin(agent.init_red())
                x = agent.get_x(afterstates)
                a = agent.get_act(w, x)
                xa_list = [x[a]]
                for t in range(300):
                    r, nafterstates = env.on_action_number_received(a)
                    if r != 0:
                        break
                    nx = agent.get_x(nafterstates)
                    na = agent.get_act(w, nx)
                    xa_list.append(nx[na])
                    x = nx
                    a = na
                for xa in xa_list[::-1]:
                    q = 2/(1 + np.exp(-np.dot(xa, w))) - 1
                    w = w + alpha*(r - q)*xa
        # 定期的にランダムとの対戦結果を描画
        if (episode+1) % plt_intvl == 0:
            episodes_x.append(episode)
            plt.clf()
            opponent = rnd_agent
            env = VsEnv(opponent, game, seed)
            for i in range(agents_len):
                r_list = np.zeros(plt_bttl)
                for bttl_i in range(plt_bttl):
                    afterstates = env.on_episode_begin(agent.init_red())
                    x = agent.get_x(afterstates)
                    a = agent.get_act(w, x)
                    for t in range(300):
                        r, nafterstates = env.on_action_number_received(a)
                        if r != 0:
                            break
                        nx = agent.get_x(nafterstates)
                        na = agent.get_act(w, nx)
                        x = nx
                        a = na
                    r_list[bttl_i] = r
                results_y[i].append(r_list.mean())
                plt.figure(1)
                plt.title('Training...')
                plt.xlabel('Episode')
                plt.ylabel('Mean Results')
                x_list = np.array(episodes_x)
                y_list = np.array(results_y[i])
                plt.plot(x_list, y_list, c=plt_colors[i], label=str(i))
            plt.pause(0.01)  # pause a bit so that plots are updated
    plt.show()
    for i in range(agents_len):
        np.save(file_name+str(i+1), agents[i].w)


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
    bttl_num = 100
    game = Geister2()
    agents_str = ["weights/td_"+str(i)+".npy" for i in range(1, 9)]
    agents = [MCAgent(game, seed+i) for i in range(8)]
    for agent, string in zip(agents, agents_str):
        agent.w = load(string)
    means = np.zeros(8*8).reshape(8, 8)
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
    bttl_num = 50
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


if __name__ == "__main__":
    cluster_learn()
