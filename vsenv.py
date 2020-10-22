# Guister environment vs the opponent(reffered in init)
import numpy as np
from random_agent import RandomAgent
from geister2 import Geister2


class VsEnv:
    """指定した固定相手と対戦する環境"""
    """現在は学習Agentが先手turn=0で固定"""

    # 勝敗が判明したか否か(青脱出可でもfalse)
    def is_ended(self):
        return self.get_reward(self._game.checkResult()) != 0

    # 確定された勝敗(青脱出可なら必ず 1)
    def get_reward(self, result):
        if result > 0:
            return 1
        elif result < 0:
            return -1
        else:
            return 0
            # ext_lvl_r = np.array([
            #     4, 5, 6, 7, 8, 9,
            #     3, 4, 5, 6, 7, 8,
            #     2, 3, 4, 5, 6, 7,
            #     1, 2, 3, 4, 5, 6,
            #     0, 1, 2, 3, 4, 5,
            #     0, 0, 1, 2, 3, 4,
            # ])
            # ext_lvl_l = np.array([
            #     9, 8, 7, 6, 5, 4,
            #     8, 7, 6, 5, 4, 3,
            #     7, 6, 5, 4, 3, 2,
            #     6, 5, 4, 3, 2, 1,
            #     5, 4, 3, 2, 1, 0,
            #     4, 3, 2, 1, 0, 0,
            # ])
            # ext_opp_lvl = np.array([
            #     3, 2, 1, 1, 2, 3,
            #     4, 3, 2, 2, 3, 4,
            #     5, 4, 3, 3, 4, 5,
            #     6, 5, 4, 4, 5, 6,
            #     7, 6, 5, 5, 6, 7,
            #     8, 7, 6, 6, 7, 8
            # ])
            # states = self._state
            # max_lvl = (np.array(states[0][0:6*6])*ext_lvl_r).max()
            # if(max_lvl > (np.array(states[2][0:6*6])*ext_lvl_r).max()):
            #     max_lvl_opp = (np.array(states[2][0:6*6])*ext_opp_lvl).max()
            #     if(max_lvl >= max_lvl_opp):
            #         return 1
            # max_lvl = (np.array(states[0][0:6*6])*ext_lvl_l).max()
            # if(max_lvl > (np.array(states[2][0:6*6])*ext_lvl_l).max()):
            #     max_lvl_opp = (np.array(states[2][0:6*6])*ext_opp_lvl).max()
            #     if(max_lvl >= max_lvl_opp):
            #         return 1
            # return 0

    def on_action_number_received(self, act_i):
        assert(not self._game.is_ended())
        _ = "NILLdayo in vsenv"
        self._game.on_action_number_received(act_i)
        reward = self.get_reward(self._game.checkResult())
        self._game.changeSide()
        if reward != 0:
            return reward, _
        states_opp = self._game.after_states()
        i_act_opp = self._opponent.get_act_afterstates(states_opp)
        self._game.on_action_number_received(i_act_opp)
        self._game.changeSide()
        reward = self.get_reward(self._game.checkResult())
        if reward != 0:
            return reward, _
        self._state = self._game.crr_state()
        return reward, self._game.after_states()

    def get_state(self):
        return self._state

    # Resetting
    def on_episode_begin(self, init_red0):
        init_red1 = self._opponent.init_red()
        self._game.__init__()
        self._game.setRed(init_red0)
        self._game.changeSide()
        self._game.setRed(init_red1)
        self._game.changeSide()
        self._state = self._game.crr_state()
        return self._game.after_states()

    def __init__(self, opponent, game=Geister2(), seed=0):
        self._opponent = opponent
        self._game = game
        self._seed = seed

        self.S_SIZE = (6*6+6)*3
        # self.A_SIZE = 8*4  # 有効最大候補手


# debug for cmd(tmp)
if __name__ == "__main__":
    seed = 59
    game = Geister2()
    agent0 = RandomAgent(game, seed)
    agent1 = RandomAgent(game, seed)
    env = VsEnv(agent1, game, seed)
    arr0 = agent0.init_red()
    s = env.on_episode_begin(arr0)
    a = agent0.get_act_afterstates(s)
    while not env.is_ended():
        r, s = env.on_action_number_received(a)
        env._game.printBoard()
        if r != 0:
            break
        a = agent0.get_act_afterstates(s)
