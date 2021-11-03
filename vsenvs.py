import random as rnd
import numpy as np
from random_agent import RandomAgent
from geister2 import Geister2
from vsenv import VsEnv

EPS = 0.001


class VsEnvs(VsEnv):
    """複数のエージェントからランダムに一つ使うやつ"""
    # Resetting
    def on_episode_begin(self, init_red0):
        self._opponent = rnd.choices(self._opponents, weights=self._rs)[0]
        return super().on_episode_begin(init_red0=init_red0)

    def __init__(self, opponents, game=Geister2(), seed=0, rs=None):
        if rs is None:
            rs = [1/len(opponents) for _ in opponents]
        assert(abs(sum(rs))-1 < EPS)  # 合計1である必要はないが，バグ防止のため
        assert(len(opponents) == len(rs))

        self._opponents = opponents
        self._rs = rs
        opp = rnd.choices(opponents, weights=rs)[0]
        return super().__init__(opponent=opp, game=game, seed=seed)
