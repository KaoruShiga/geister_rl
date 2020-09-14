import random
import numpy as np
from env_short_corridor import EnvShortCorridor


class REINFORCEBL:
    def get_action(self):
        xs = np.array([[1, 0], [0, 1]])
        hs = np.dot(self.theta, xs)
        hs -= hs.max()  # for prevention of overflow
        exps = np.exp(hs)
        sum = exps.sum()
        pis = exps/sum
        a = np.random.choice(2, 1, p=pis)
        return a

    def __init__(self, alpha_t=0.001953125, alpha_w=0.015625):
        self.alpha_t = alpha_t
        self.alpha_w = alpha_w
        self.theta = np.log([19, 1])
        self.w = np.array([0.])


def main():
    max_episode = 1000
    max_t = 1000
    agents = [REINFORCEBL() for _ in range(100)]
    env = EnvShortCorridor()
    xs = np.array([[1, 0], [0, 1]])
    for episode in range(max_episode):
        j_list = []
        for i in range(100):
            agent = agents[i]
            g_list = []
            x_list = []
            g = 0.0
            env.on_episode_begin()
            t = 0
            while (not env.is_ended) and (t < max_t):
                a = agent.get_action()
                x = (np.array([1, 0]) if (a == 0) else np.array([0, 1]))
                x_list.append(x)
                r = env.on_action_received(a)
                g += r
                g_list.append(g)
                t += 1
            j_list.append(g)
            for x, g in zip(x_list, g_list):
                dlt = g - agent.w*1
                agent.w += agent.alpha_w*dlt*1
                hs = np.dot(agent.theta, xs)
                hs -= hs.max()  # for prevention of overflow
                exps = np.exp(hs)
                sum = exps.sum()
                pis = exps/sum
                agent.theta += agent.alpha_t*dlt*(x - np.dot(xs, pis))
        print(np.array(j_list).mean())
    print(agent.theta)
    hs = np.dot(agent.theta, xs)
    exps = np.exp(hs)
    sum = exps.sum()
    pis = exps/sum
    print(pis)
    print(agent.w)


if __name__ == "__main__":
    main()
