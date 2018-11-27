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

def simulate(frequency_of_demands, rounds=10, skip=1):
  """
  A strategy for a player, in this game, consists of an amount of cake that he would like.
  The set of possible strategies for a player is thus any amount between 0 and C.
  - If the sum of strategies for each player is less than or equal to C, each player receives the amount he asked for.
  - However, if the sum of strategies exceeds C, no player receives anything.

  Arguments:
    frequency_of_demands: A vector with length 11.
  """
  frequency_of_demands = np.array(frequency_of_demands) / np.sum(frequency_of_demands)
  agent_matrix = np.random.choice(C + 1, size=(N, N), p=frequency_of_demands)

  dist = {}

  for i in range(C + 1):
    dist[i] = list(np.zeros(rounds))

  for i in range(rounds):
    score_matrix = np.zeros((N, N))
    # In each round, each player plays with its eight neighbors.
    for r in range(N):
      for c in range(N):
        demand_r_c = agent_matrix[r, c]
        for n_r in [r - 1, r, r + 1]:
          for n_c in [c - 1, c, c + 1]:
            if (n_r == r and n_c == c) or (n_r < 0 or n_r >= N) or (n_c < 0 or n_c >= N):
              continue
            else:
              demand_n_r_n_c = agent_matrix[n_r, n_c]
              if demand_r_c + demand_n_r_n_c <= C:
                score_matrix[r, c] += demand_r_c
                score_matrix[n_r, n_c] += demand_n_r_n_c
    # At the end of round, player_r_c changes its demand.
    for r in range(N):
      for c in range(N):
        demand_r_c = agent_matrix[r, c]
        max_neighbor_score = score_matrix[r, c]
        max_neighbor_demand = demand_r_c
        for n_r in [r - 1, r, r + 1]:
          for n_c in [c - 1, c, c + 1]:
            if (n_r == r and n_c == c) or (n_r < 0 or n_r >= N) or (n_c < 0 or n_c >= N):
              continue
            else:
              if score_matrix[n_r, n_c] >= max_neighbor_score:
                max_neighbor_demand = agent_matrix[n_r, n_c]
                max_neighbor_score = score_matrix[n_r, n_c]
        agent_matrix[r, c] = max_neighbor_demand

    e, counts = np.unique(agent_matrix, return_counts=True)
    for index in range(len(e)):
      dist[e[index]][i] = counts[index] / N / N
    # plt.imshow(agent_matrix)
    # plt.show()
  legends = []
  for (demand, line) in dist.items():
    legends.append('demand %d' % demand)
    line.insert(0, frequency_of_demands[demand])
    line_smoothed = gaussian_filter1d(line, sigma=1)
    plt.plot(line_smoothed)
  plt.legend(legends)
  plt.show()

def simulate_2(frequency_of_demands, rounds=50, label='dist'):
  frequency_of_demands = np.array(frequency_of_demands) / np.sum(frequency_of_demands)
  freq_sum = [frequency_of_demands.copy()]
  for i in range(rounds):
    w_c = np.zeros(C + 1)
    for demand_i in range(C + 1):
      for demand_k in range(C + 1):
        w_c[demand_i] += demand_i * frequency_of_demands[demand_k] if demand_i + demand_k <= C else 0
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
  plt.savefig('./img/%s.jpg' % label)

if __name__ == "__main__":
  dist_1 = [0.0544685, 0.236312, 0.0560727, 0.0469244, 0.0562243, 0.0703294, 0.151136, 0.162231, 0.0098273, 0.111366, 0.0451093]
  dist_2 = [0.410376, 0.107375, 0.0253916, 0.116684, 0.0813494, 0.00573677, 0.0277155, 0.0112791, 0.0163166, 0.191699, 0.00607705]
  simulate_2(dist_1, 50, label='dist_1')
  simulate_2(dist_2, 50, label='dist_2')