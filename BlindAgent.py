import random
import cProfile
import pstats
import numpy as np
import matplotlib.pyplot as plt
from geister2 import Geister2
from vsenv import VsEnv
from iagent import IAgent
from random_agent import RandomAgent
from reinforce_agent import REINFORCEAgent
from load_ import load_agent
from tcp_player import tcp_connect


def learn():
    file_name = "weights/blindvsrnd3"
    seed = 111
    game = Geister2()
    agent = BlindAgent(game, seed)
    agent.w = np.random.randn(agent.W_SIZE)*agent.alpha*0.00001
    agent.theta = np.random.randn(agent.T_SIZE)*agent.beta*0.00001
    opponent = RandomAgent(game, seed+1)
    env = VsEnv(opponent, game, seed)
    # 計測準備
    pr = cProfile.Profile()
    pr.enable()
    # 計測開始
    agent.learn(env, seed=seed, max_episodes=100000, draw_mode=True)
    # 計測終了，計測結果出力
    pr.disable()
    stats = pstats.Stats(pr)
    stats.sort_stats('cumtime')
    stats.print_stats()
    pr.dump_stats('profile.stats')
    # 事後処理

    np.save(file_name+"_w", agent.w)
    np.save(file_name+"_theta", agent.theta)


def learnVsBlind(file_name_blind):
    file_name = "weights/rfvscnstblind"
    seed = 114
    game = Geister2()
    agent = REINFORCEAgent(game, seed)
    agent.w = np.random.randn(agent.W_SIZE)*agent.alpha*0.00001
    agent.theta = np.random.randn(agent.T_SIZE)*agent.beta*0.00001
    opponent = load_agent(file_name_blind, game, seed)
    env = VsEnv(opponent, game, seed)
    # 計測準備
    pr = cProfile.Profile()
    pr.enable()
    # 計測開始
    agent.learn(env, seed=seed, max_episodes=100000, draw_mode=True)
    # 計測終了，計測結果出力
    pr.disable()
    stats = pstats.Stats(pr)
    stats.sort_stats('cumtime')
    stats.print_stats()
    pr.dump_stats('profile.stats')
    # 事後処理

    np.save(file_name+"_w", agent.w)
    np.save(file_name+"_theta", agent.theta)


# 自分の駒の色が見えないREINFORCEAgent(取られた駒は相手のも自分のも見える)
# 自分と対戦相手の双方が得られる情報しか使えない
class BlindAgent(REINFORCEAgent):
    # xは0-1の実数になりうる．自分の駒が赤(青)である確率を示す(取られた駒から計算)
    # 小数でも「きっと」うまくいく => デバッグ完了
    def get_x(self, afterstates):
        left_b = 4  # 取られた青ゴマの数
        left_r = 4  # 取られた赤ゴマの数
        for i in range(3):
            if(afterstates[0][i][38] == 1):
                left_b = 4 - (i+1)
            if(afterstates[0][i][39] == 1):
                left_r = 4 - (i+1)
        states_1ht = [
            state[0] + state[1] + state[2] + [1.0]  # 小数にするため
            for state in afterstates]
        a_size = len(afterstates)
        s1_size = self.S_SIZE + 1  # 通常サイズ+バイアス項
        x = np.array(states_1ht)
        x[:, 0:36] = x[:, 42:36+42] = x[:, 0:36] + x[:, 42:36+42]
        x[:, 0:36] *= left_b/(left_b+left_r)
        x[:, 42:36+42] *= left_r/(left_b+left_r)
        x = (x[:, self.ROW_IDS]*x[:, self.COL_IDS]).reshape(a_size, -1)
        x[:, -1] = 1  # バイアス項
        return x

    def __init__(self, game, seed=None):
        super().__init__(game, seed)
        self.alpha = 0.001
        self.beta = 0.00002


if __name__ == "__main__":
    # learn()

    learnVsBlind("weights/blindvsrnd1")

    # seed = 1
    # game = Geister2()
    # # rndAgent = RandomAgent(game, seed=seed)
    # blindAgent = BlindAgent(game, seed=seed)
    # blindAgent.w = np.zeros(blindAgent.W_SIZE)
    # blindAgent.theta = np.zeros(blindAgent.T_SIZE)
    # env = VsEnv(opponent=rndAgent, game=game, seed=seed)
    # env.on_episode_begin(rndAgent.init_red())
    # blindAgent.get_x(game.after_states())

    # tcp_connect(blindAgent, game, port=10000)
