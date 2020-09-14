import random
import numpy as np
from env_short_corridor import EnvShortCorridor


class agent_eps_grdy:
    def get_action(self):
        if self.epsilon < random.random():
            xs = np.array([[1, 0], [0, 1]])
            qs = np.dot(self.w, xs)
            a = np.argmax(qs)
            return a
        else:
            a = random.randrange(2)
            return a

    def __init__(self, alpha=0.1, epsilon=0.1):
        self.alpha = alpha
        self.epsilon = epsilon
        self.w = np.array([0., 0.])


if __name__ == "__main__":
    max_episode = 1000
    agent = agent_eps_grdy()
    env = EnvShortCorridor()
    j_list = []
    for episode in range(max_episode):
        x_list = []
        g_list = []
        g = 0.0
        env.on_episode_begin()
        while(not env.is_ended):
            a = agent.get_action()
            x = ([1, 0] if (a == 0) else [0, 1])
            x_list.append(x)
            r = env.on_action_received(a)
            g += r
            g_list.append(g)
        j_list.append(g)
        for x, g in zip(x_list, g_list):
            x = np.array(x)
            agent.w += agent.alpha*(g - np.dot(agent.w, x))*x
    print(np.array(j_list[:100]).mean())
    print(np.array(j_list[-100:]).mean())
    print(agent.w)
