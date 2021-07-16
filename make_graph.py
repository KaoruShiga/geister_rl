import numpy as np
import matplotlib.pyplot as plt



x_list = [0, 30, 100, 400, 900]
y_list = [0.12, 0.58, 0.56, 0.645, 0.79]


plt.xlabel('学習回数/万回', fontname="IPAexGothic")
plt.ylabel('勝率', fontname="IPAexGothic")
episodes_x = np.array(x_list)
results_y = np.array(y_list)
plt.plot(episodes_x, results_y, linestyle='-', marker="o", c='b')
plt.legend()
plt.show()
