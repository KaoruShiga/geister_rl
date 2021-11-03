import numpy as np
from geister2 import Geister2
from load_ import load_agent

MAX_T = 200  # don't forget it.


def battle_get_kifu(agent1, agent2, bttl_num, seed=None):
    kifus = []
    results = []  # results, 0=>win, 1=>draw, 2=>lost for i
    game = agent1._game
    for t in range(bttl_num):
        kifu = []
        agent_s = (agent1, agent2)
        arr0, arr1 = (agent.init_red() for agent in agent_s)
        game.__init__()
        game.setRed(arr0)
        game.changeSide()
        game.setRed(arr1)
        game.changeSide()
        player = 0
        for _ in range(MAX_T):
            if player == 0:
                kifu.append(game.real_state())
            agent = agent_s[player]
            states = game.after_states()
            i_act = agent.get_act_afterstates(states)
            game.on_action_number_received(i_act)
            game.changeSide()
            player = (player+1) % 2
            if game.is_ended():
                break
        if player == 1:
            game.changeSide()
        result = game.checkResult()
        r = (0 if (result > 0) else (1 if (result == 0) else 2))
        results.append(r)
        kifus.append(kifu)
    return (kifus, results)

def battle2_get_results(agents1, agents2, bttl_num=1, seed=None):
    game = agents1[0]._game
    results = np.zeros(len(agents1)*len(agents2)*3).reshape(len(agents1), len(agents2), 3)
    # results[i][j], 0=>win, 1=>draw, 2=>lost for agents1
    for i in range(len(agents1)):
        for j in range(len(agents2)):
            for t in range(bttl_num):
                agent_s = (agents1[i], agents2[j])
                arr0, arr1 = (agent.init_red() for agent in agent_s)
                game.__init__()
                game.setRed(arr0)
                game.changeSide()
                game.setRed(arr1)
                game.changeSide()
                player = 0
                for _ in range(MAX_T):
                    agent = agent_s[player]
                    states = game.after_states()
                    i_act = agent.get_act_afterstates(states)
                    game.on_action_number_received(i_act)
                    game.changeSide()
                    player = (player+1) % 2
                    if game.is_ended():
                        break
                if player == 1:
                    game.changeSide()
                result = game.checkResult()
                r = (0 if (result > 0) else (1 if (result == 0) else 2))
                results[i][j][r] += 1
    return results


# 次の手番はagent1, tmp_gameに関して破壊的
def battle_from(agent1, agent2, tmp_game=None, seed=None):
    agent1._game = agent2._game = tmp_game
    agents = [agent1, agent2]
    player = 0
    for _ in range(MAX_T):
        agent = agents[player]
        states = tmp_game.after_states()
        i_act = agent.get_act_afterstates(states)
        tmp_game.on_action_number_received(i_act)
        tmp_game.changeSide()
        player = (player+1) % 2
        if tmp_game.is_ended():
            break
    if player == 1:
        tmp_game.changeSide()
    result = tmp_game.checkResult()
    dst = (1 if (result > 0) else (-1 if (result < 0) else 0))
    return dst


# agents1 とagents2の全ての対戦カードの平均報酬を出力
def battle2(agents1, agents2, bttl_num=1, seed=None):
    game = agents1[0]._game
    means = np.zeros(len(agents1)*len(agents2)).reshape(len(agents1), len(agents2))
    for i in range(len(agents1)):
        for j in range(len(agents2)):
            r_list = np.zeros(bttl_num)
            for t in range(bttl_num):
                agent_s = (agents1[i], agents2[j])
                arr0, arr1 = (agent.init_red() for agent in agent_s)
                game.__init__()
                game.setRed(arr0)
                game.changeSide()
                game.setRed(arr1)
                game.changeSide()
                player = 0
                for _ in range(MAX_T):
                    agent = agent_s[player]
                    states = game.after_states()
                    i_act = agent.get_act_afterstates(states)
                    game.on_action_number_received(i_act)
                    game.changeSide()
                    player = (player+1) % 2
                    if game.is_ended():
                        break
                if player == 1:
                    game.changeSide()
                result = game.checkResult()
                r = (1 if (result > 0) else (-1 if (result < 0) else 0))
                r_list[t] = r
            means[i][j] = r_list.mean()
    return means


# agent1の平均報酬を出力
def battle(agent1, agent2, bttl_num=1, seed=None):
    game = agent1._game
    results = np.zeros(bttl_num)
    agents = [agent1, agent2]
    for t in range(bttl_num):
        arr0, arr1 = (agent.init_red() for agent in agents)
        game.__init__()
        game.setRed(arr0)
        game.changeSide()
        game.setRed(arr1)
        game.changeSide()
        player = 0
        for _ in range(MAX_T):
            agent = agents[player]
            states = game.after_states()
            i_act = agent.get_act_afterstates(states)
            game.on_action_number_received(i_act)
            game.changeSide()
            player = (player+1) % 2
            if game.is_ended():
                break
        if player == 1:
            game.changeSide()
        result = game.checkResult()
        r = (1 if (result > 0) else (-1 if (result < 0) else 0))
        results[t] = r
    return results.mean()


if __name__ == "__main__":
    seed = 100
    geister = Geister2()
    agents1 = [load_agent("weights/rfvsrnd5", geister, seed)]
    agents2 = [load_agent(("weights/weights_13/reinforce_"+str(i)),
               geister, seed) for i in range(1, 10)]
    results = battle2(agents1, agents2, 100)
    print(results)
