import numpy as np
import client
import argparse
from geister2 import Geister2
from random_agent import RandomAgent
from reinforce_agent import REINFORCEAgent
from greedy_agent import GreedyAgent


class TCPPlayer():
    def __init__(self, agent, game):
        self._game = game
        self.agent = agent

    def get_hand(self, state):
        self._game.setState(state=state)

        # # 脱出可能か検討...してない

        act_i = self.agent.get_act_afterstates(self._game.after_states())
        i, dir = self._game.legalMoves()[act_i]
        unit_names = ["A", "B", "C", "D", "E", "F", "G", "H"]
        unit_name = unit_names[i]
        move_dirs = ["E", "S", "W", "N"]
        move_dir = move_dirs[dir]
        return [unit_name, move_dir]

    def init_red(self):
        return "".join(self.agent.init_red())
        # return "".join(["A", "B", "C", "D"])


def tcp_connect(agent, game, port, host="localhost", games=1):
    rs = [0, 0, 0]  # rs = [win, draw, lost]
    player = TCPPlayer(agent=agent, game=game)
    for _ in range(args.games):
        result = client.run(player, port, host)
        rs[result] += 1
        sleep(0.1)
    return rs


if __name__ == "__main__":
    from time import sleep
    parser = argparse.ArgumentParser(description='TCP接続するクライエント')  # 2. パーサを作る
    # # 3. parser.add_argumentで受け取る引数を追加していく
    parser.add_argument('-p', '--port', type=int, default=10000)
    parser.add_argument('--host', type=str, default="localhost")
    parser.add_argument('--games', type=int, default=1)
    parser.add_argument('--isGreedy', type=bool, default=True)
    parser.add_argument('--path', type=str)
    # 例:
    # python tcp_player.py --port 10000 --games 5000 --path C:\Users\maoru\Documents\geister_v2\weights\vsself2\vsself500
    # file name: vsself500_theta.npy
    # first_player: port=10000, second_player: port=10001

    # # 4. 引数を解析
    args = parser.parse_args()
    game = Geister2()
    agent = GreedyAgent(game) if args.isGreedy else REINFORCEAgent(game)
    path_theta = args.path + "_theta.npy"
    agent.theta = np.load(path_theta)

    # rs = [win, draw, lost]
    rs = tcp_connect(agent=agent, game=game, port=args.port, host=args.host, games=args.games)
    print("win, draw, lost = ")
    print(rs)
