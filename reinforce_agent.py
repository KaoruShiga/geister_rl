# reinforce と書いてあるがREINFORCE with baselineを実装している
import random
import cProfile
import pstats
import numpy as np
import matplotlib.pyplot as plt
from geister2 import Geister2
from vsenv import VsEnv
from iagent import IAgent
from random_agent import RandomAgent


def learn():
    file_name = "weights/rfvsrnd6"
    seed = 103
    game = Geister2()
    agent = REINFORCEAgent(game, seed)
    agent.w = np.random.randn(agent.W_SIZE)*agent.alpha*0.0001
    agent.theta = np.random.randn(agent.T_SIZE)*agent.beta*0.0001
    opponent = RandomAgent(game, seed+1)
    env = VsEnv(opponent, game, seed)
    # 計測準備
    pr = cProfile.Profile()
    pr.enable()
    # 計測開始
    agent.learn(env, seed)
    # 計測終了，計測結果出力
    pr.disable()
    stats = pstats.Stats(pr)
    stats.sort_stats('cumtime')
    stats.print_stats()
    pr.dump_stats('profile.stats')
    # 事後処理

    np.save(file_name+"_w", agent.w)
    np.save(file_name+"_theta", agent.theta)


class REINFORCEAgent(IAgent):
    def learn(self, env, seed=1, max_episodes=100000,
              draw_mode=False, draw_opp=None):
        alpha = self.alpha
        beta = self.beta
        # epsilon = self.epsilon
        # rnd = self._rnd
        assert(env.S_SIZE == self.S_SIZE)

        plt_intvl = 500
        plt_bttl = 50
        episodes_x = []
        results_y = []
        dlts_y = []
        dlts = []
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
        if draw_mode:
            denv = VsEnv(draw_opp, game=Geister2(), seed=seed)
        for episode in range(max_episodes):
            afterstates = env.on_episode_begin(self.init_red())
            xs = self.get_x([env.get_state()])[0]
            x = self.get_x(afterstates)
            a = self.get_act(x, theta)

            xs_list = [xs]
            x_list = [x]
            xa_list = [x[a]]

            for t in range(self.MAX_T):
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
            # reinforce と書いてあるがREINFORCE with baselineを実装している
            for xa, x, xs in zip(xa_list, x_list, xs_list):
                q = 2/(1 + np.exp(-np.dot(w, xs))) - 1
                dlt = r - q  # 報酬予測は事後状態を用いてはならない
                dlts.append(dlt**2)
                w += beta*dlt*xs
                hs = x.dot(theta)
                hs -= hs.max()  # overflow回避のため
                exps = np.exp(hs)
                pis = exps/exps.sum()
                theta += alpha*r*(xa - pis.dot(x))
                # 焼きなまし法
                # theta += alpha*(episode/max_episodes)*r*(xa - pis.dot(x))

            if draw_opp is None and draw_mode:
                print("not implemented")
                raise Exception
            if draw_mode and ((episode+1) % plt_intvl == 0):
                dlts_y.append(np.array(dlts).mean())
                dlts = []
                if draw_opp is not None:
                    denv._opponent = draw_opp
                    r_sum = 0.0
                    for bttl_i in range(plt_bttl):
                        afterstates = denv.on_episode_begin(self.init_red())
                        x = self.get_x(afterstates)
                        a = self.get_act(x, theta)
                        for t in range(300):
                            r, nafterstates = denv.on_action_number_received(a)
                            if r != 0:
                                break
                            nx = self.get_x(nafterstates)
                            na = self.get_act(nx, theta)
                            x = nx
                            a = na
                        r_sum += r
                    results_y.append(r_sum/plt_bttl)
                episodes_x.append(episode)
                # 一つ目 results
                plt.figure(2)
                plt.title('Training...')
                plt.xlabel('Episode')
                plt.ylabel('Mean Results of Interval')
                plt.text(50, 0.5, "alpha="+str(self.alpha))
                plt.text(50, 0.4, "beta="+str(self.beta))
                x_list = np.array(episodes_x)
                y_list = np.array(results_y)
                plt.plot(x_list, y_list)
                plt.pause(0.0001)  # pause a bit so that plots are updated
                plt.clf()
                # 二つ目 予測誤差 Δv(s)^2
                plt.figure(1)
                plt.title('Training...')
                plt.xlabel('Episode')
                plt.ylabel('Mean Dlt v(s)^2')
                plt.text(50, 0.5, "alpha="+str(self.alpha))
                plt.text(50, 0.4, "beta="+str(self.beta))
                x_list = np.array(episodes_x)
                y_list = np.array(dlts_y)
                plt.plot(x_list, y_list)
                plt.pause(0.0001)  # pause a bit so that plots are updated
                plt.clf()

        # 学習終了後
        if (draw_mode):
            # 一つ目 results
            plt.figure(2)
            plt.title('Training...')
            plt.xlabel('Episode')
            plt.ylabel('Mean Results of Interval')
            plt.text(50, 0.5, "alpha="+str(self.alpha))
            plt.text(50, 0.4, "beta="+str(self.beta))
            x_list = np.array(episodes_x)
            y_list = np.array(results_y)
            plt.plot(x_list, y_list)
            plt.show()
            # 二つ目 予測誤差 Δv(s)^2
            plt.figure(1)
            plt.title('Training...')
            plt.xlabel('Episode')
            plt.ylabel('Mean Dlt v(s)^2')
            plt.text(50, 0.5, "alpha="+str(self.alpha))
            plt.text(50, 0.4, "beta="+str(self.beta))
            x_list = np.array(episodes_x)
            y_list = np.array(dlts_y)
            plt.plot(x_list, y_list)
            plt.show()

    def get_act(self, x, theta):
        assert(len(theta) > 0)

        a_size = x.shape[0]
        hs = x.dot(theta)
        hs -= hs.max()  # for prevention of overflow
        exps = np.exp(hs)
        pis = exps/exps.sum()
        act_i = np.random.choice(a_size, p=pis)
        return act_i

    # random
    def init_red(self):
        arr = ["A", "B", "C", "D", "E", "F", "G", "H"]
        self._rnd.shuffle(arr)
        return arr[0:4]
    # # using learned weights with no learning.
    # def init_red(self):
    #     arr_string = ["A", "B", "C", "D", "E", "F", "G", "H"]
    #     states = self._game.init_states()
    #     x = self.get_x(states)
    #     act_i = self.get_act(x, self.theta)
    #     state = states[act_i]
    #     arr = []
    #     arr[0:4] = state[1][25:29]
    #     arr[4:8] = state[1][31:35]
    #     dst = []
    #     for i in range(len(arr)):
    #         if arr[i] == 1:
    #             dst.append(arr_string[i])
    #     return dst

    def get_a_size(self, afterstates):
        return len(afterstates)

    def get_x(self, afterstates):
        states_1ht = [
            state[0] + state[1] + state[2] + [1]
            for state in afterstates]
        a_size = len(afterstates)
        s1_size = self.S_SIZE + 1  # 通常サイズ+バイアス項
        x = np.array(states_1ht)
        # # 二駒関係v1
        # y = np.array([np.dot(s.reshape(-1, 1), s.reshape(1, -1)) for s in x])
        #     .reshape(a_size, -1)
        # 二駒関係v2
        # y = np.zeros((a_size, (s1_size*(s1_size+1)//2)))
        # for i in range(s1_size):
        #     y[:, (i*(i+1)//2):((i+1)*(i+2)//2)] = x[:, i:i+1]*x[:, 0:i+1]
        # 二駒関係v3
        x = (x[:, self.ROW_IDS]*x[:, self.COL_IDS]).reshape(a_size, -1)
        x[:, -1] = 1  # バイアス項
        return x

    def get_act_afterstates(self, states):
        assert(self.theta.shape[0] != 0)
        x = self.get_x(states)
        i_act = self.get_act(x, self.theta)
        return i_act

    # 優先度が最も高い手を返す(after_states -> act_i)
    def get_greedy_a(self, states):
        assert(len(self.theta) > 0)
        x = self.get_x(states)
        hs = x.dot(self.theta)
        amax = np.argmax(hs)
        return amax

    def __init__(self, game, seed=None):
        self._game = game
        self._rnd = random.Random(seed)
        np.random.seed(seed)

        self.alpha = 0.002
        self.beta = 0.00005

        self.S_SIZE = (6*6+6)*3
        self.W_SIZE = ((self.S_SIZE+1)*(self.S_SIZE+2))//2
        self.T_SIZE = self.X_SIZE = self.W_SIZE
        self.A_MAX = 32  # 最大有効候補手
        self.MAX_T = 100  # 最大行動回数(=最大ターン数/2)

        self.w = None
        self.theta = None

        self.ROW_IDS = []
        self.COL_IDS = []
        for i in range(self.S_SIZE+1):
            self.ROW_IDS += [i]*(i+1)
            for j in range(i+1):
                self.COL_IDS += [j]


if __name__ == "__main__":
    # test()
    learn()
    # test2()
