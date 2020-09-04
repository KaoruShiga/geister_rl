# Guister environment vs the opponent(reffered in init)
from random_agent import RandomAgent
from geister2 import Geister2


class VsEnv:
    "w’è‚µ‚½ŒÅ’è‘Šè‚Æ‘Îí‚·‚éŠÂ‹«"
    "Œ»İ‚ÍŠwKAgent‚ªæèturn=0‚ÅŒÅ’è"
    def is_ended(self):
        return self._game.is_ended()

    def get_reward(self, result):
        if result > 0:
            return 1
        elif result < 0:
            return -1
        else:
            return 0

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
        return reward, self._game.after_states()

    # Resetting
    def on_episode_begin(self, init_red0):
        init_red1 = self._opponent.init_red()
        self._game.__init__()
        self._game.setRed(init_red0)
        self._game.changeSide()
        self._game.setRed(init_red1)
        self._game.changeSide()
        return self._game.after_states()

    def __init__(self, opponent, game=Geister2(), seed=0):
        self._opponent = opponent
        self._game = game
        self._seed = seed

        self.S_SIZE = (6*6+6)*3
        # self.A_SIZE = 8*4  # —LŒøÅ‘åŒó•âè


# debug for cmd(tmp)
if __name__ == "__main__":
    seed = 9
    game = Geister2()
    agent0 = RandomAgent(game, seed)
    agent1 = RandomAgent(game, seed)
    env = VsEnv(agent1, game, seed)
    arr0 = agent0.init_red()
    s = env.on_episode_begin(arr0)
    while not env.is_ended():
        a = agent0.get_act_afterstates(s)
        r, s = env.on_action_number_received(a)
    print("r = "+str(r))
