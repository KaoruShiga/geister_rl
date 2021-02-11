import numpy as np
import matplotlib.pyplot as plt

path_cl_xs = 'reinforce_x_list.npy'
path_cl_ys = 'reinforce_avg_y.npy'
path_self_xs = 'vsself2x_list.npy'
path_self_ys = 'vsself2avg_y.npy'


plt.xlabel('各個体の学習回数', fontname="IPAexGothic")
plt.ylabel('平均勝率(対戦相手はランダムな手を指す)', fontname="IPAexGothic")
episodes_x = np.load(path_cl_xs)
avg_y = np.load(path_cl_ys)
avg_y = avg_y/2 + 0.5
x_list = np.array(episodes_x)
y_list = np.array(avg_y)
plt.plot(x_list, y_list, linestyle='-', c='r', label="9 players against each other")
plt.legend()

episodes_x = np.load(path_self_xs)
avg_y = np.load(path_self_ys)
avg_y = avg_y/2 + 0.5
x_list = np.array(episodes_x)
y_list = np.array(avg_y)
plt.plot(x_list, y_list, linestyle='-', c='b', label="self-play")
plt.legend()
plt.show()
