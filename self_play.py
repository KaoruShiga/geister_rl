import numpy as np
from geister2 import Geister2
from vsenv import VsEnv
from reinforce_agent import REINFORCEAgent


def self_play(file_name, agent=None, max_train=10000):
    seed = 0
    max_episodes = max_train
    alpha = 0.001
    beta = 0.0001

    game = Geister2()
    np.random.seed(seed)
    if agent is None:
        agent = REINFORCEAgent(game, seed)
        agent.w = np.zeros(agent.W_SIZE)
        agent.theta = np.zeros(agent.T_SIZE)
    agent.alpha = alpha
    agent.beta = beta

    env = VsEnv(agent, game, seed)
    for episode in range(max_episodes):
        agent.alpha = alpha  # * (1 - episode/max_episodes)
        agent.beta = beta   # * (1 - episode/max_episodes)
        agent.learn(env, max_episodes=1)
    # self play向けに変更
    np.save(file_name+"_w", agent.w)
    np.save(file_name+"_theta", agent.theta)


if __name__ == "__main__":
    import argparse
    import load_
    seed = None
    max_train = 10000

    # パーサを作る
    parser = argparse.ArgumentParser(description='self-play')
    # parser.add_argumentで受け取る引数を追加していく
    parser.add_argument('-i', type=int)
    # 引数を解析
    args = parser.parse_args()

    i = args.i
    assert(i > 0)
    while(True):
        past_path = "weights/vsself2/vsself"+str(i)
        file_name = "weights/vsself2/vsself"+str(i+1)
        game = Geister2()
        agent = load_.load_agent(past_path, game, seed=seed)
        self_play(file_name, agent, max_train)
        i += 1
