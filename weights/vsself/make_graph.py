import numpy as np
import matplotlib.pyplot as plt
path_here = 'weights/weights_17/'
path_self_xs = path_here + 'vsselfx_list.npy'
path_self_ys = path_here + 'vsselfresults_y.npy'
path_self3_xs = path_here + 'vsself3x_list.npy'
path_self3_ys = path_here + 'vsself3results_y.npy'


plt.xlabel('対戦回数', fontname="IPAexGothic")
plt.ylabel('平均勝率(対戦相手はランダムな手を指す)', fontname="IPAexGothic")
episodes_x = np.load(path_self_xs)
results_y = np.load(path_self_ys)[0]
results_y = results_y/2 + 0.5
episodes3_x = np.load(path_self3_xs) + 50000
results3_y = np.load(path_self3_ys)[0]
results3_y = results3_y/2 + 0.5
episodes_x = np.concatenate((episodes_x, episodes3_x), axis=None)
results_y = np.concatenate((results_y, results3_y), axis=None)
plt.plot(episodes_x, results_y, linestyle='-', c='b', label="self-play")
plt.legend()
plt.show()
