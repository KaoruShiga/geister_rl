import random
import csv
import cProfile
import pstats
import numpy as np
from geister2 import Geister2
from iagent import IAgent
from random_agent import RandomAgent
from reinforce_agent import REINFORCEAgent
from load_ import load_agents
from battle import battle
from battle import battle2


agentsnum = 9
seed = None
bttl_num = 3
threshold = 0.2


def add_in_ranking(path_list):
    # ランキングデータの読み込み
    ranking_path = []
    ranking_n = []
    ranking_r = []
    with open('rankings', 'rt') as fin:
        cin = csv.reader(fin)
        datas = [row for row in cin if len(row) > 0]
        ranking_path = [row[2] for row in datas]
        ranking_n = [int(row[3]) for row in datas]
        ranking_r = [float(row[4]) for row in datas]

    # ランキングの人数が足りないときはagentを追加
    while len(ranking_path) < agentsnum:
        ranking_path.append(path_list.pop(0))  # path_listの末尾を移動
        ranking_n.append(0)
        ranking_r.append(0)
    # ランキングの人数が多すぎるときは追加候補に移動
    while len(ranking_path) > agentsnum:
        path_list.append(ranking_path.pop(0))  # rankingの末尾を移動
        del ranking_n[0]
        del ranking_r[0]

    # agentの重みの読み込み
    game = Geister2()
    agents = load_agents(path_list, game, seed)
    rank_agents = load_agents(ranking_path, game, seed)

    # 対戦を行い基準を満たせば追加．
    for i in range(len(agents)):
        agent = agents[i]
        results = []
        # 最新のランキングに更新
        rank_agents = load_agents(ranking_path, game, seed)
        for j in range(len(rank_agents)):
            rank_agent = rank_agents[j]
            # resultはagentの勝率
            result = battle(agent, rank_agent, bttl_num=bttl_num, seed=seed)
            results.append(result)
            # 対戦相手の勝率を更新
            r_opp = -result
            ranking_r[j] = (ranking_r[j]*ranking_n[j]+r_opp)/(ranking_n[j]+1)
            ranking_n[j] += 1
        results = np.array(results)
        # 基準を満たしていない場合
        if (results.mean() <= threshold or
                len(np.where(results > 0)[0]) <= agentsnum/2):
            continue
        # 基準を満たしている場合(rが一定値以上かつ過半数に対し勝利),ランキングに追加
        dl_index = ranking_r.index(min(ranking_r))  # ランキングの削除対象
        ranking_path[dl_index] = path_list[i]
        ranking_n[dl_index] = ranking_r[dl_index] = 0

    # データの書き込み
    datas = [[str(i+1), "REINFORCEAgent", ranking_path[i], n, r]
             for i, n, r
             in zip(range(len(ranking_path)), ranking_n, ranking_r)]
    with open('rankings', 'wt') as fout:
        csvout = csv.writer(fout)
        csvout.writerows(datas)


if __name__ == '__main__':
    # # 計測準備
    # pr = cProfile.Profile()
    # pr.enable()
    # # 計測開始
    n = 9
    all_path_list = ['weights/weights_'+str(j)+'/reinforce_'+str(i)
                     for i in range(1, 10) for j in range(2, 18) if j != 9]
    all_path_list += ['weights/rfvsrnd'+str(i) for i in range(1, 6)]
    # all_path_list += ['weights/blindvsself1']
    all_path_list += ['ranking_learn/weights/rankRF'+str(i) for i in range(1, 300)]
    all_path_list += ['weights/weights_17/vsself'+str(i) for i in range(1, 4)]
    while(True):
        path_list = random.choices(all_path_list, k=n)
        add_in_ranking(path_list)
    # # 計測終了，計測結果出力
    # pr.disable()
    # stats = pstats.Stats(pr)
    # stats.sort_stats('cumtime')
    # stats.print_stats()
    # pr.dump_stats('profile.stats')
    # # 結果出力終了
