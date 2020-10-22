import random
import numpy as np
import matplotlib.pyplot as plt
from geister2 import Geister2
from vsenv import VsEnv
from iagent import IAgent
from random_agent import RandomAgent


def learn():
    file_name = "weights_5/rf_4"
    seed = 121
    game = Geister2()
    agent = REINFORCEAgent(game, seed)
    agent.w = np.random.randn(agent.W_SIZE)*agent.alpha*0.1
    agent.theta = np.random.randn(agent.T_SIZE)*agent.beta*0.1
    opponent = RandomAgent(game, seed+1)
    env = VsEnv(opponent, game, seed)
    agent.learn(env, seed)
    # np.save(file_name+"_w", agent.w)
    # np.save(file_name+"_theta", agent.theta)


class REINFORCEAgent(IAgent):
    def learn(self, env, seed=1, max_episodes=10000):
        alpha = self.alpha
        beta = self.beta
        # epsilon = self.epsilon
        # rnd = self._rnd
        assert(env.S_SIZE == self.S_SIZE)

        plt_intvl = 100
        episodes_x = []
        results_y = []
        # 読み込み
        # mcagent.w = np.load("td_4.npy")
        # wを小さな正規乱数で初期化
        # np.random.seed(seed)
        # if self.w is None:
        #     self.w = np.random.randn(self.W_SIZE)*alpha*0.1
        # if self.theta is None:
        #     self.theta = np.random.randn(self.T_SIZE)*beta*0.1
        w = self.w
        theta = self.theta

        for episode in range(max_episodes):
            afterstates = env.on_episode_begin(self.init_red())
            xs = self.get_x([env.get_state()])[0]
            x = self.get_x(afterstates)
            a = self.get_act(x, theta)
            xs_list = [xs]
            x_list = [x]
            xa_list = [x[a]]
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
            xa_arr, x_arr, xs_arr = np.array(xa_list), np.array(x_list), np.array(xs_list)
            print(x_arr[0:1])
            dlt = r - xs_arr.dot(w)
            dlt_w1 = beta*(xa_arr.T.dot(dlt))
            hs = x_arr.dot(theta)
            hs -= hs.max().reshape(-1, 1)
            exps = np.exp(hs)
            pis = exps/exps.sum(1).reshape(-1, 1)
            dlt_theta1 = alpha*r*(
                xa_arr.sum(0) -
                np.matmul(pis.reshape(len(pis), 1, -1), x_arr)
                .reshape(len(pis), -1).sum(0))
            dlt_w2 = dlt_theta2 = 0
            for xa, x, xs in zip(xa_list, x_list, xs_list):
                dlt = r - w.dot(xs)  # 報酬予測は事後状態を用いてはならない
                dlt_w2 += beta*dlt*xa
                hs = x.dot(theta)
                hs -= hs.max()  # overflow回避のため
                exps = np.exp(hs)
                pis = exps/exps.sum()
                dlt_theta2 += alpha*r*(xa - pis.dot(x))
            print(dlt_w1 - dlt_w2)
            print(dlt_theta1 - dlt_theta2)
            w += dlt_w2
            theta += dlt_theta2

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
        # # 二駒関係
        # y = np.array([np.dot(s.reshape(-1, 1), s.reshape(1, -1)) for s in x])
        #     .reshape(a_size, -1)
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

        self.w = None
        self.theta = None


if __name__ == "__main__":
    # test()
    learn()
    # test2()
