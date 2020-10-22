import random
import numpy as np
import matplotlib.pyplot as plt
from geister2 import Geister2
from vsenv import VsEnv
from iagent import IAgent
from random_agent import RandomAgent


def learn():
    file_name = "weights_5/rf_4"
    seed = 120
    game = Geister2()
    agent = REINFORCEAgent(game, seed)
    agent.w = np.random.randn(agent.W_SIZE)*agent.alpha*0.1
    agent.theta = np.random.randn(agent.T_SIZE)*agent.beta*0.1
    opponent = RandomAgent(game, seed+1)
    env = VsEnv(opponent, game, seed)
    agent.learn(env, seed)
    np.save(file_name+"_w", agent.w)
    np.save(file_name+"_theta", agent.theta)


class REINFORCEAgent(IAgent):
    def learn(self, env, seed=1, max_episodes=10000):
        alpha = self.alpha
        beta = self.beta
        w = self.w
        theta = self.theta
        assert(env.S_SIZE == self.S_SIZE)
        assert(alpha > 0)
        assert(beta > 0)
        assert(len(w) > 0)
        assert(len(theta) > 0)

        plt_intvl = 100
        episodes_x = []
        results_y = []
        for episode in range(max_episodes):
            afterstates = env.on_episode_begin(self.init_red())
            xs = self.get_x([env.get_state()])[0]
            x = self.get_x(afterstates)
            a = self.get_act(x, theta)
            xs_list = [xs]
            x_list = [x]
            xa_list = [x[a]]
            self.history = np.zeros(self.H_SIZE)
            for t in range(300):
                r, nafterstates = env.on_action_number_received(a)
                if r != 0:
                    break
                nxs = self.get_x([env.get_state()])[0]
                nx = self.get_x(nafterstates)
                na = self.get_act(nx, theta)
                xs_list.append(nxs)
                x_list.append(nx)
                xa_list.append(nx[na])
                x = nx
                a = na
            for xa, x, xs in zip(xa_list, x_list, xs_list):
                dlt = r - w.dot(xs)  # 報酬予測は事後状態を用いてはならない
                w += beta*dlt*xa
                hs = x.dot(theta)
                hs -= hs.max()  # overflow回避のため
                exps = np.exp(hs)
                pis = exps/exps.sum()
                theta += alpha*r*(xa - pis.dot(x))

        #     results_y.append(r)
        #     if (episode+1) % plt_intvl == 0:
        #         plt.figure(2)
        #         plt.title('Training...')
        #         plt.xlabel('Episode')
        #         plt.ylabel('Mean Results of Interval')
        #         episodes_x.append(episode)
        #         x_list = np.array(episodes_x)
        #         y_list = np.array(results_y)
        #         y_list = y_list.reshape(-1, plt_intvl)
        #         means = y_list.mean(axis=1)
        #         plt.plot(x_list, means)
        #         plt.pause(0.0001)  # pause a bit so that plots are updated
        #         plt.clf()
        #
        # plt.figure(2)
        # plt.title('Training...')
        # plt.xlabel('Episode')
        # plt.ylabel('Mean Results of Interval')
        # x_list = np.array(episodes_x)
        # y_list = np.array(results_y)
        # y_list = y_list.reshape(-1, plt_intvl)
        # means = y_list.mean(axis=1)
        # plt.plot(x_list, means)
        # plt.show()

    def get_act(self, x, theta):
        assert(len(theta) > 0)

        a_size = x.shape[0]
        hs = x.dot(theta)
        hs -= hs.max()  # for prevention of overflow
        exps = np.exp(hs)
        pis = exps/exps.sum()
        act_i = np.random.choice(a_size, p=pis)
        return act_i

    # using learned weights with no learning.
    def init_red(self):
        arr_string = ["A", "B", "C", "D", "E", "F", "G", "H"]
        states = self._game.init_states()
        x = self.get_x(states)
        act_i = self.get_act(x, self.theta)
        state = states[act_i]
        arr = []
        arr[0:4] = state[1][25:29]
        arr[4:8] = state[1][31:35]
        dst = []
        for i in range(len(arr)):
            if arr[i] == 1:
                dst.append(arr_string[i])
        return dst

    def get_a_size(self, afterstates):
        return len(afterstates)

    def get_x(self, afterstates):
        states_1ht = [
            state[0] + state[1] + state[2] + [1]
            for state in afterstates]
        a_size = len(afterstates)
        s1_size = self.S_SIZE + 1  # 通常サイズ+バイアス項
        x = np.array(states_1ht).reshape(a_size, s1_size)
        # 二駒関係v2
        y = np.zeros((a_size, (s1_size*(s1_size+1)//2)))
        for i in range(s1_size):
            y[:, (i*(i+1)//2):((i+1)*(i+2)//2)] = x[:, i:i+1]*x[:, 0:i+1]
        y[:, -1] = 1  # バイアス項
        return y

    def get_act_afterstates(self, states):
        assert(self.theta.shape[0] != 0)
        x = self.get_x(states)
        i_act = self.get_act(x, self.theta)
        return i_act

    def __init__(self, game, seed=None):
        self._game = game
        self._rnd = random.Random(seed)
        np.random.seed(seed)

        self.alpha = 0.005
        self.beta = 0.0003

        self.S_SIZE = (6*6+6)*3
        self.W_SIZE = ((self.S_SIZE+1)*(self.S_SIZE+2))//2
        self.T_SIZE = self.W_SIZE
        self.H_SIZE = 5

        self.w = None
        self.theta = None

        self.wB = None
        self.thetaB = None


if __name__ == "__main__":
    learn()
