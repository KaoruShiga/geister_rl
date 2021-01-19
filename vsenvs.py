import random as rnd
import numpy as np
from random_agent import RandomAgent
from geister2 import Geister2
from vsenv import VsEnv


class VsEnvs(VsEnv):
    """複数のエージェントからランダムに一つ使うやつ"""
    # Resetting
    def on_episode_begin(self, init_red0):
        self._opponent = rnd.choice(self._opponents)
        return super().on_episode_begin(init_red0=init_red0)

    def __init__(self, opponents, game=Geister2(), seed=0):
        self._opponents = opponents
        opp = rnd.choice(opponents)
        return super().__init__(opponent=opp, game=game, seed=seed)
