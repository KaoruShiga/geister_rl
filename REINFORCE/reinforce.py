import random
import numpy as np
from env_short_corridor import EnvShortCorridor


class REINFORCE:
    def get_action(self):
        xs = np.array([[1, 0], [0, 1]])
        hs = np.dot(self.theta, xs)
        exps = np.exp(hs)
        sum = exps.sum()
        pis = exps/sum
        a = np.random.choice(2, 1, p=pis)
        return a

    def __init__(self, alpha=0.00012):
        self.alpha = alpha
        self.theta = np.log([19, 1])


if __name__ == "__main__":
    max_episode = 1000
    max_t = 90
    agents = [REINFORCE() for _ in range(100)]
    env = EnvShortCorridor()
    xs = np.array([[1, 0], [0, 1]])
    for episode in range(max_episode):
        j_list = np.zeros(100)
        for i in range(100):
            agent = agents[i]
            x_list = []
            r_list = []
            g = 0.0
            env.on_episode_begin()
            t = 0
            while (not env.is_ended) and (t < max_t):
                a = agent.get_action()
                x = ([1, 0] if (a == 0) else [0, 1])
                x_list.append(x)
                r = env.on_action_received(a)
                g += r
                r_list.append(r)
                t += 1
            j_list[i] = g
            for x, r in zip(x_list, r_list):
                x = np.array(x)
                hs = np.dot(agent.theta, xs)
                exps = np.exp(hs)
                sum = exps.sum()
                pis = exps/sum
                agent.theta += agent.alpha*g*(x - np.dot(xs, pis))
                g -= r
        if episode == 100:
            print(np.array(j_list).mean())
    print(agent.theta)
    hs = np.dot(agent.theta, xs)
    exps = np.exp(hs)
    sum = exps.sum()
    pis = exps/sum
    print(pis)
