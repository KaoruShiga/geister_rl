import numpy as np
from geister2 import Geister2
from vsenv import VsEnv
from vsenvs import VsEnvs
from reinforce_agent import REINFORCEAgent
import load_

def self_play2(file_name, game, i, past_agents, max_train=10000, seed=None):
    max_episodes = max_train
    alpha = 0.001
    beta = 0.0001
    r = 0.5
    rs = [(1-r)/(len(past_agents)-1) for _ in past_agents]
    rs[-1] = r
    np.random.seed(seed)

    past_path = file_name+str(i)
    new_path = file_name+str(i+1)
    agent = load_.load_agent(past_path, game, seed=seed)
    agent.alpha = alpha
    agent.beta = beta

    env = VsEnvs(past_agents, game, seed, rs=rs)
    for episode in range(max_episodes):
        agent.alpha = alpha  # * (1 - episode/max_episodes)
        agent.beta = beta   # * (1 - episode/max_episodes)
        agent.learn(env, max_episodes=1)

    # save
    np.save(new_path+"_w", agent.w)
    np.save(new_path+"_theta", agent.theta)
    return agent


if __name__ == "__main__":
    import argparse
    import pstats
    import cProfile
    seed = None
    max_train = 10000

    # パーサを作る
    parser = argparse.ArgumentParser(description='self-play')
    # parser.add_argumentで受け取る引数を追加していく
    parser.add_argument('-i', type=int)
    # 引数を解析
    args = parser.parse_args()
    file_name = "weights/vsself3/vsself"
    i = args.i
    assert(i > 0)

    game = Geister2()
    paths = [file_name+str(i) for i in range(0, i+1)]
    past_agents = load_.load_agents(paths, game, seed=seed)

    # 1回だけ計測ありで実行
    # 計測準備
    pr = cProfile.Profile()
    pr.enable()
    # 計測開始
    added_agent = self_play2(file_name, game, i, past_agents, max_train, seed=seed)
    past_agents.append(added_agent)
    i += 1
    # 計測結果出力
    stats = pstats.Stats(pr)
    stats.sort_stats('cumtime')
    stats.print_stats()

    pr.dump_stats('profile.stats')
    # 計測あり終了

    # 計測なしで中断されるまで学習継続
    while(True):
        added_agent = self_play2(file_name, game, i, past_agents, max_train, seed=seed)
        past_agents.append(added_agent)
        i += 1
