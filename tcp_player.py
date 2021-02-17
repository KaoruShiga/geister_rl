import numpy as np
import client
import argparse
from geister import Geister
from geister2 import Geister2
from random_agent import RandomAgent
from reinforce_agent import REINFORCEAgent


class TCPPlayer():
    def __init__(self, agent, game):
        self._game = game
        self.agent = agent

    def get_hand(self, state):
        self._game.setState(state=state)

        # # 脱出可能か検討
        # ext_lvl = np.array([
        #     8, 7, 6, 6, 7, 8,
        #     7, 6, 5, 5, 6, 7,
        #     6, 5, 4, 4, 5, 6,
        #     5, 4, 3, 3, 4, 5,
        #     4, 3, 2, 2, 3, 4,
        #     3, 2, 1, 1, 2, 3
        # ])
        # ext_opp_lvl = np.array([
        #     3, 2, 1, 1, 2, 3,
        #     4, 3, 2, 2, 3, 4,
        #     5, 4, 3, 3, 4, 5,
        #     6, 5, 4, 4, 5, 6,
        #     7, 6, 5, 5, 6, 7,
        #     8, 7, 6, 6, 7, 8
        # ])
        # states = self._game.crr_state()
        # max_lvl = (np.array(states[0][0:6 * 6]) * ext_lvl).max()
        # if (max_lvl > (np.array(states[2][0:6 * 6]) * ext_lvl).max()):
        #     max_lvl_opp = (np.array(states[2][0:6 * 6]) * ext_opp_lvl).max()
        #     if (max_lvl >= max_lvl_opp):
        #         # 以下確実に脱出可能な場合

        # 脱出可能だと判定できなかった場合
        act_i = self.agent.get_greedy_a(self._game.after_states())
        i, dir = self._game.legalMoves()[act_i]
        unit_names = ["A", "B", "C", "D", "E", "F", "G", "H"]
        unit_name = unit_names[i]
        move_dirs = ["E", "S", "W", "N"]
        move_dir = move_dirs[dir]
        return [unit_name, move_dir]

    def init_red(self):
        return "".join(self.agent.init_red())


def tcp_connect(agent, game, port, host="localhost"):
    player = TCPPlayer(agent=agent, game=game)
    client.run(player, port, host)


if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description='TCP接続するクライエント')  # 2. パーサを作る
    # # 3. parser.add_argumentで受け取る引数を追加していく
    # parser.add_argument('-p', '--port', type=int, default=10000)
    # # 4. 引数を解析
    # args = parser.parse_args()

    # file_name = "weights/weights_10/reinforce_6_theta.npy"  # 今までより少し強い
    # file_name = "ranking_learn/weights/rankRF91_theta.npy"
    file_name = "weights/weights_17/vsself11_theta.npy"  # なぜかめっちゃ強い
    game = Geister2()
    agent = REINFORCEAgent(game)
    agent.theta = np.load(file_name)
    # "itolab.asuscomm.com", "localhost"
    # first_player: port=10000, second_player: port=10001
    tcp_connect(agent=agent, game=game, port=10000, host="itolab.asuscomm.com")
