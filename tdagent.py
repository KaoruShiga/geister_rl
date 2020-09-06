import random
import numpy as np
import matplotlib.pyplot as plt
from iagent import IAgent
from random_agent import RandomAgent
from geister2 import Geister2
from vsenv import VsEnv


def learn():
    seed = 560
    game = Geister2()
    tdagent = TDAgent(game, seed)
    rndagent = RandomAgent(game, seed)
    env = VsEnv(rndagent, game, seed)
    tdagent.learn(env, seed)
    for k in range(6*7*3):
        for i in range(3):
            for j in range(7):
                print((tdagent.w[j+i*(6*7)+k*(6*7*3):6+j+i*(6*7)+k*(6*7*3)]
                      * 1000).round()*(1/1000))
            print("-----------")
        print("-------------------")
    np.save('td_4', tdagent.w)
    w_td = np.load('td_4.npy')
    print(w_td)


class TDAgent(IAgent):
    def learn(self, env, seed=1):
        alpha = self.alpha
        epsilon = self.epsilon
        rnd = self._rnd
        S_SIZE = env.S_SIZE
        self.S_SIZE = S_SIZE

        plt_intvl = 100
        episodes_x = []
        results_y = []
        # wを小さな正規乱数で初期化
        np.random.seed(seed)
        self.w = w = np.random.randn(S_SIZE**2)*alpha*2 + alpha*2

        for episode in range(10000):
            afterstates = env.on_episode_begin(self.init_red())
            x = self.get_x(afterstates)
            a = self.get_act(w, x)
            for t in range(300):
                r, nafterstates = env.on_action_number_received(a)
                if r != 0:
                    break
                nx = self.get_x(nafterstates)
                na = self.get_act(w, nx)
                q = 2/(1 + np.exp(-np.dot(x[a], w))) - 1
                nq = 2/(1+np.exp(-np.dot(nx[na], w))) - 1
                w = w + alpha*(nq - q)*x[a]
                x = nx
                a = na
            q = 2/(1 + np.exp(-np.dot(x[a], w))) - 1
            w = w + alpha*(r - q)*x[a]

            episodes_x.append(episode)
            results_y.append(r)
            if (episode+1) % plt_intvl == 0:
                x_list = plt_intvl*np.arange((episode+1)/plt_intvl)
                y_list = np.array(results_y)
                y_list = y_list.reshape(-1, plt_intvl)
                means = y_list.mean(axis=1)
                plt.figure(2)
                plt.title('Training...')
                plt.xlabel('Episode')
                plt.ylabel('Mean Results of Interval')
                plt.plot(x_list, means)
                plt.pause(0.0001)  # pause a bit so that plots are updated
                plt.clf()
        self.w = w

    def get_act(self, w, x):
        assert(len(w) != 0)
        act_i = 0
        a_size = x.shape[0]
        if self.epsilon < self._rnd.random():  # P(1-epsilon): greedy
            act_i = self.get_greedy_a(w, x)
        else:  # P(epsilon): explore
            act_i = self._rnd.randrange(a_size)
        return act_i

    # constant
    def init_red(self):
        arr = ["E", "F", "G", "H"]
        return arr

    def get_greedy_a(self, w, x):
        Q_list = np.dot(x, w)
        amax = np.argmax(Q_list)
        return amax

    def get_a_size(self, afterstates):
        return len(afterstates)

    def get_x(self, afterstates):
        states_1ht = [
            state[0] + state[1] + state[2]
            for state in afterstates]
        x = np.array(states_1ht)
        a_size = len(afterstates)
        # 二駒関係
        y = np.array([np.dot(s.reshape(-1, 1), s.reshape(1, -1)) for s in x]) \
            .reshape(a_size, -1)
        return y

    def get_act_afterstates(self, states):
        assert(self.w.shape[0] != 0)
        x = self.get_x(states)
        i_act = self.get_act(self.w, x)
        return i_act

    def __init__(self, game, seed=0):
        self._game = game
        self._rnd = random.Random(seed)

        self.epsilon = 0.3
        self.alpha = 0.001
        self.S_SIZE = (6*6+6)*3

        self.w = "midainyuu"


def test():
    seed = 2
    game = Geister2()

    tdagent = TDAgent(game, seed)
    tdagent.w = np.array([
        0.9, 0, 0, 0, 0, 0,
        0.8, 0, 0, 0, 0, 0,
        0.7, 0, 0, 0, 0, 0,
        0.6, 0, 0, 0, 0, 0,
        0.5, 0, 0, 0, 0, 0,
        0.1, 0, 0, 0, 0, 0,
        0,   0, 0, 0, 0, 1,

        0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0,

        0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0
    ])

    rndagent = RandomAgent(game, seed)
    agents = (tdagent, rndagent)
    arr0, arr1 = (agent.init_red() for agent in agents)
    game.setRed(arr0)
    game.changeSide()
    game.setRed(arr1)
    game.changeSide()
    game.printBoard()
    player = 0
    while not game.is_ended():
        agent = agents[player]
        states = game.after_states()
        i_act = agent.get_act_afterstates(states)
        game.on_action_number_received(i_act)
        if player == 0:
            game.printBoard()
        game.changeSide()

        player = (player+1) % 2


if __name__ == "__main__":
    # test()
    learn()
