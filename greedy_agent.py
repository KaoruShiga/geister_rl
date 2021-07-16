from reinforce_agent import REINFORCEAgent
from geister2 import Geister2


class GreedyAgent(REINFORCEAgent):
    def get_act_afterstates(self, states):
        return self.get_greedy_a(states)


if __name__ == "__main__":
    from load_ import load_agent
    from battle import battle
    from battle import battle2_get_results

    bttl_num = 10000
    MAX_T = 100

    seed = None
    path_vsself = "weights/vsself2/vsself"
    game = Geister2()
    path1 = path_vsself + str(300)
    path2 = path_vsself + str(300)
    agent1 = load_agent(path1, game=game, seed=seed, AgentClass=GreedyAgent)
    agent2 = load_agent(path2, game=game, seed=seed)
    mat1 = battle2_get_results([agent1], [agent2], bttl_num=bttl_num//2, seed=seed)
    mat2 = battle2_get_results([agent2], [agent1], bttl_num=bttl_num//2, seed=seed)
    mat1 = mat1[0][0]
    mat2 = mat2[0][0]
    mat1
    mat2[::-1]

    path1 = path_vsself + str(500)
    path2 = path_vsself + str(500)
    agent1 = load_agent(path1, game=game, seed=seed, AgentClass=GreedyAgent)
    agent2 = load_agent(path2, game=game, seed=seed)
    mat1 = battle2_get_results([agent1], [agent2], bttl_num=bttl_num//2, seed=seed)[0][0]
    mat2 = battle2_get_results([agent2], [agent1], bttl_num=bttl_num//2, seed=seed)[0][0]
    mat1
    mat2[::-1]

    path1 = path_vsself + str(700)
    path2 = path_vsself + str(700)
    agent1 = load_agent(path1, game=game, seed=seed, AgentClass=GreedyAgent)
    agent2 = load_agent(path2, game=game, seed=seed)
    mat1 = battle2_get_results([agent1], [agent2], bttl_num=bttl_num//2, seed=seed)[0][0]
    mat2 = battle2_get_results([agent2], [agent1], bttl_num=bttl_num//2, seed=seed)[0][0]
    mat1
    mat2[::-1]
