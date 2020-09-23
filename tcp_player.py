import numpy as np
import client
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
        act_i = self.agent.get_act_afterstates(self._game.after_states())
        i, dir = self._game.legalMoves()[act_i]
        unit_names = ["A", "B", "C", "D", "E", "F", "G", "H"]
        unit_name = unit_names[i]
        move_dirs = ["E", "S", "W", "N"]
        move_dir = move_dirs[dir]
        return [unit_name, move_dir]

    def init_red(self):
        return "".join(self.agent.init_red())


def tcp_connect(agent, game, port):
    player = TCPPlayer(agent=agent, game=game)
    client.run(player, port)


if __name__ == "__main__":
    file_name = "weights/weights_11/reinforce_2_theta.npy"
    game = Geister2()
    agent = REINFORCEAgent(game)
    agent.theta = np.load(file_name)
    tcp_connect(agent=agent, game=game, port=10000)
