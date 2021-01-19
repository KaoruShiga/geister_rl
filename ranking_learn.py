import random as rnd
import csv
import cProfile
import pstats
import numpy as np
from geister2 import Geister2
from vsenv import VsEnv
from vsenvs import VsEnvs
from reinforce_agent import REINFORCEAgent
from load_ import load_agent
from load_ import load_agents
from battle import battle

# エージェントの学習中のパラメータ
max_episodes = 5000

# rankingに関するパラメタ
num_rankingagents = 18
bttl_num = 20
threshold = 0.2
# rankingに関するパス
weights_path = "ranking_learn/weights"
ranking_data_path = 'ranking_learn/ranking_data'
rankings_path = 'ranking_learn/rankings'


def get_path_radom(game):
    file_name = weights_path + "/random_reinforce"
    agent = REINFORCEAgent(game, None)
    agent.alpha = 0.005
    agent.beta = 0.0003
    agent.w = np.random.randn(agent.W_SIZE)*agent.alpha*0.0001
    agent.theta = np.random.randn(agent.T_SIZE)*agent.beta*0.0001
    np.save(file_name+"_w", agent.w)
    np.save(file_name+"_theta", agent.theta)
    return file_name


def pick_agent(game):
    with open(rankings_path, 'rt') as fin:
        cin = csv.reader(fin)
        datas = [row for row in cin if len(row) > 0]
        ranking_path = [row[2] for row in datas]
    agent1 = load_agent(rnd.choice(ranking_path), game, seed=None)
    agent2 = load_agent(rnd.choice(ranking_path), game, seed=None)
    agent = REINFORCEAgent(game, None)
    agent.alpha = 0.005
    agent.beta = 0.0003
    agent.w = np.random.normal(
        loc=(agent1.w+agent2.w)/2,
        scale=(2**0.5)*abs(agent1.w-agent2.w)/2
        )
    agent.theta = np.random.normal(
        loc=(agent1.theta+agent2.theta)/2,
        scale=(2**0.5)*abs(agent1.theta-agent2.theta)/2
        )
    return agent


def ranking_learn(game):
    # ranking_leanのデータ読み込み
    with open(ranking_data_path, 'rt') as fin:
        cin = csv.reader(fin)
        datas = [row for row in cin if len(row) > 0]
        num_weights = int(datas[0][0])

    # ランキングデータの読み込み
    ranking_path = []
    ranking_n = []
    ranking_r = []
    with open(rankings_path, 'rt') as fin:
        cin = csv.reader(fin)
        datas = [row for row in cin if len(row) > 0]
        ranking_path = [row[2] for row in datas]
        ranking_n = [int(row[3]) for row in datas]
        ranking_r = [float(row[4]) for row in datas]

    # ランキングの人数が足りないときはランダムな重みのREINFORCEagentを追加
    while len(ranking_path) < num_rankingagents:
        ranking_path.append(get_path_radom(game))  # path_listの末尾を移動
        ranking_n.append(0)
        ranking_r.append(0)
    # ランキングの人数が多すぎるときはエラー
    if len(ranking_path) > num_rankingagents:
        print("error. ranking_num is over num_rankingagents")
        # path_list.append(ranking_path.pop(0))  # rankingの末尾を移動
        # del ranking_n[0]
        # del ranking_r[0]

    # rank agentsの重みの読み込み
    game = Geister2()
    train_is = rnd.sample(range(num_rankingagents), num_rankingagents//2)
    test_is = [i for i in range(num_rankingagents) if i not in train_is]
    rank_agents = load_agents(ranking_path, game, None)
    train_agents = [rank_agents[i] for i in train_is]
    test_agents = [rank_agents[i] for i in test_is]

    # 新しいagentの作成
    agent = pick_agent(game)
    agent_path = weights_path + "/rankRF" + str(num_weights)
    # agnetの学習
    env = VsEnvs(train_agents, game, None)  # 対戦相手はランダムに一度だけ
    agent.learn(env, max_episodes=max_episodes)

    # 最新のランキングに対して改めて対戦を行い，(test_agentsのみ更新)
    # 基準を満たしていれば，agentのランキングへの追加
    results = []
    for i in test_is:
        test_agent = rank_agents[i]
        # resultはagentの勝率
        result = battle(agent, test_agent, bttl_num=bttl_num, seed=None)
        results.append(result)
        # 対戦相手の勝率を更新
        r_opp = -result
        ranking_r[i] = (ranking_r[i]*ranking_n[i]+r_opp)/(ranking_n[i]+1)
        ranking_n[i] += 1
    results = np.array(results)
    # 基準を満たしている場合(rが一定値以上かつ過半数に対し勝利),ランキングに追加
    if (results.mean() > threshold and
            len(np.where(results > 0)[0]) > num_rankingagents/2):
        # ランキングの削除対象(test_agentsのうち勝率が最低のもの)
        dl_index = ranking_r.index(min([ranking_r[i] for i in test_is]))
        ranking_path[dl_index] = agent_path
        ranking_n[dl_index] = ranking_r[dl_index] = 0

    # agentのデータの書き込み
    np.save(agent_path + "_w", agent.w)
    np.save(agent_path + "_theta", agent.theta)
    num_weights += 1

    # ranking_learnのデータ書き込み
    with open(ranking_data_path, 'wt') as fout:
        csvout = csv.writer(fout)
        datas = [[str(num_weights)]]
        csvout.writerows(datas)

    # ランキングデータの書き込み
    datas = [[str(i+1), "REINFORCEAgent", ranking_path[i], n, r]
             for i, n, r
             in zip(range(len(ranking_path)), ranking_n, ranking_r)]
    with open(rankings_path, 'wt') as fout:
        csvout = csv.writer(fout)
        csvout.writerows(datas)


if __name__ == "__main__":
    game = Geister2()
    # 計測準備
    pr = cProfile.Profile()
    pr.enable()
    # 計測開始
    while(True):
        ranking_learn(game)
    # 計測終了，計測結果出力
    pr.disable()
    stats = pstats.Stats(pr)
    stats.sort_stats('cumtime')
    stats.print_stats()
    pr.dump_stats('profile.stats')
    # 結果出力終了
