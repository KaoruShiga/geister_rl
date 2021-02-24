# rollout algorithm とか，(ボードゲームaiでの)モンテカルロ法と呼ばれている手法
# (強化学習の)モンテカルロ法とは別物(=> こっちはmcagent.py)
import random
import numpy as np
from geister2 import Geister2
from iagent import IAgent
from battle import battle_from


class RolloutAgent(IAgent):
    def get_act_afterstates(self, states):
        tmp_game = Geister2()
        max_num = self.bttl_num
        mat = np.zeros((len(states), max_num))
        for num in range(max_num):
            for act_i in range(len(states)):
                # tmp_gameに位置情報と自分の駒の色を設定
                num_red = 0  # 敵の赤駒の数
                is_vld = []  # 敵の盤上にある駒のi
                for i in range(16):
                    tmp_game.units[i].x = self._game.units[i].x
                    tmp_game.units[i].y = self._game.units[i].y
                    tmp_game.units[i].taken = self._game.units[i].taken
                    tmp_game.units[i].color = self._game.units[i].color
                    if(i >= 8):
                        tmp_game.units[i].color = 1  # 敵の青駒として設定
                        if(tmp_game.units[i].taken is False):
                            is_vld.append(i)
                        # 敵の赤駒ならばnum_redを1追加
                        num_red += 1 if tmp_game.units[i].color == 3 else 0
                # 敵の駒の色は推定せず，ランダムに
                self._rnd.shuffle(is_vld)
                for i in is_vld[:num_red]:
                    tmp_game.units[i].color = 3  # 敵の赤駒として設定
                tmp_game.on_action_number_received(act_i)
                mat[act_i, num] = battle_from(self.policy, self.policy, tmp_game=tmp_game)
        means = mat.mean(axis=1)
        return np.argmax(means)

    def get_greedy_a(self, states):
        return self.get_act_afterstates(states)

    def init_red(self):
        arr = ["A", "B", "C", "D", "E", "F", "G", "H"]
        self._rnd.shuffle(arr)
        return arr[0:4]

    def __init__(self, game, seed=1, policy=None):
        if policy is None:
            raise Exception
        self._game = game
        self._rnd = random.Random(seed)
        self.policy = policy
        self.bttl_num = 100


if __name__ == "__main__":
    import cProfile
    import pstats
    from random_agent import RandomAgent
    from battle import battle
    seed = 0
    game = Geister2()
    rndagent = RandomAgent(game, seed)
    rlagent = RolloutAgent(game, seed, policy=rndagent)
    # 計測準備
    pr = cProfile.Profile()
    pr.enable()
    # 計測開始
    r = battle(rlagent, rndagent, seed=seed, bttl_num=10)
    # 計測終了，計測結果出力
    pr.disable()
    stats = pstats.Stats(pr)
    stats.sort_stats('cumtime')
    stats.print_stats()
    pr.dump_stats('profile.stats')
    # 事後処理

    print(r)
