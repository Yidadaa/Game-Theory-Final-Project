"""
Paper link: https://plato.stanford.edu/entries/game-evolutionary/#SenFai

This code implements section 4.1 of the paper.
"""
import numpy as np
import json
from matplotlib import pyplot as plt
from scipy.ndimage.filters import gaussian_filter1d

C = 10 # amount of cake
N = 500

def simulate_2(frequency_of_demands, rounds=50, label='dist'):
  """
  A strategy for a player, in this game, consists of an amount of cake that he
  would like.The set of possible strategies for a player is thus any amount
  between 0 and C.
  - If the sum of strategies for each player is less than or equal to C,
    each player receives the amount he asked for.
  - However, if the sum of strategies exceeds C, no player receives anything.

  Arguments:
    frequency_of_demands: A vector with length 11.
  """
  frequency_of_demands = np.array(frequency_of_demands)\
    / np.sum(frequency_of_demands)
  freq_sum = [frequency_of_demands.copy()]
  for i in range(rounds):
    w_c = np.zeros(C + 1)
    for demand_i in range(C + 1):
      for demand_k in range(C + 1):
        w_c[demand_i] += demand_i * frequency_of_demands[demand_k]\
          if demand_i + demand_k <= C else 0
    w_c *= np.array(frequency_of_demands)
    w_c = w_c / np.sum(w_c)
    frequency_of_demands = w_c
    freq_sum.append(frequency_of_demands.copy())
  legends = []
  freq_sum = np.array(freq_sum)
  plt.clf()
  for i in range(C + 1):
    legends.append('demand %d' % i)
    plt.plot(freq_sum[:, i])
  plt.legend(legends)
  # plt.show()
  plt.savefig('./img/%s.eps' % label)

if __name__ == "__main__":
  dist_1 = [0.0544685, 0.236312, 0.0560727, 0.0469244, 0.0562243, 0.0703294,
    0.151136, 0.162231, 0.0098273, 0.111366, 0.0451093]
  dist_2 = [0.410376, 0.107375, 0.0253916, 0.116684, 0.0813494, 0.00573677,
    0.0277155, 0.0112791, 0.0163166, 0.191699, 0.00607705]
  simulate_2(dist_1, 50, label='dist_1')
  simulate_2(dist_2, 50, label='dist_2')