import csv
import numpy as np
from geister2 import Geister2
from iagent import IAgent
from random_agent import RandomAgent
from reinforce_agent import REINFORCEAgent
from load_ import load_agents
from battle import battle
from battle import battle2


agentsnum = 5
seed = None
bttl_num = 3
threshold = 0.2


def add_in_ranking(path_list):
    # ランキングデータの読み込み
    ranking_path = []
    with open('rankings', 'rt') as fin:
        cin = csv.reader(fin)
        datas = [row for row in cin if len(row) != 0]
        ranking_path = [row[2] for row in datas]
        # print(datas)

    # ランキングの人数が足りないときはagentを追加
    while len(ranking_path) < agentsnum:
        ranking_path.append(path_list.pop())  # path_listの末尾を移動
    # ランキングの人数が多すぎるときは追加候補に移動
    while len(ranking_path) > agentsnum:
        path_list.append(ranking_path.pop())  # rankingの末尾を移動

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
        for rank_agent in rank_agents:
            results.append(battle(agent, rank_agent,
                           bttl_num=bttl_num, seed=seed))
        results = np.array(results)
        # 基準を満たしていない場合
        if (results.mean() <= threshold or
                len(np.where(results > 0)[0]) <= agentsnum/2):
            continue
        # 基準を満たしている場合(ただし，総当たりではじかれることもある)
        newagents = rank_agents + [agent]
        means = battle2(newagents, newagents, bttl_num=bttl_num, seed=seed)
        rs = means.mean(0)
        dl_index = rs.argmin()
        if dl_index != len(newagents)-1:  # 総当たりで追加エージェントがビリ以外
            del ranking_path[dl_index]
            ranking_path.append(path_list[i])

    # ランキングをソート
    rank_agents = load_agents(ranking_path, game, seed)
    means = battle2(rank_agents, rank_agents, bttl_num=bttl_num, seed=seed)
    rs = means.mean(0)
    sorted_path = sorted(list(zip(ranking_path, rs)), key=lambda a: a[1],
                         reverse=True)
    ranking_path = [a[0] for a in sorted_path]

    # データの書き込み
    datas = [[str(i+1), "REINFORCEAgent", ranking_path[i], n, r]
             for i in range(len(ranking_path))]
    with open('rankings', 'wt') as fout:
        csvout = csv.writer(fout)
        csvout.writerows(datas)


if __name__ == '__main__':
    add_in_ranking(['weights/weights_13/reinforce_'+str(i) for i in range(1, 10)])
