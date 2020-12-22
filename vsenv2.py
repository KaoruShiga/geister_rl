# Guister environment vs the opponent(reffered in init)
import random
from geister2 import Geister2
from random_agent import RandomAgent
from vsenv import VsEnv


class VsEnv2(VsEnv):
    """指定した相手と対戦し，対戦相手も学習する環境"""

    def on_action_number_received(self, act_i):
        assert(not self._game.is_ended())
        _ = "NILLdayo in vsenv"
        self._game.on_action_number_received(act_i)
        reward = self.get_reward(self._game.checkResult())
        self._game.changeSide()
        if reward != 0:  # ゲーム終了時
            self._opponent.fit(self.xa_list, self.x_list, self.xs_list,
                               -reward)
            return reward, _
        states_opp = self._game.after_states()
        x_opp = self._opponent.get_x(states_opp)
        i_act_opp = self._opponent.get_act(x_opp, self._opponent.theta)
        self.x_list.append(x_opp)
        self.xa_list.append(x_opp[i_act_opp])
        self.xs_list.append(self._opponent.get_x([self._game.crr_state()])[0])
        self._game.on_action_number_received(i_act_opp)
        self._game.changeSide()
        reward = self.get_reward(self._game.checkResult())
        if reward != 0:  # ゲーム終了時
            self._opponent.fit(self.xa_list, self.x_list, self.xs_list,
                               -reward)
            return reward, _
        self._state = self._game.crr_state()
        return reward, self._game.after_states()

    # Resetting
    def on_episode_begin(self, init_red0):
        self.xa_list = []
        self.x_list = []
        self.xs_list = []
        return super().on_episode_begin(init_red0)
