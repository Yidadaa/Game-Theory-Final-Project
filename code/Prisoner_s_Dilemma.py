"""
Paper link: https://plato.stanford.edu/entries/game-evolutionary/#SenFai

This code implements section 2.2 of the paper.

Ref: https://www.researchgate.net/profile/Martin_Nowak2/publication/216634494_Evolutionary_Games_and_Spatial_Chaos/links/54217b730cf274a67fea8e60/Evolutionary-Games-and-Spatial-Chaos.pdf
"""
import numpy as np
import json
from matplotlib import pyplot as plt

N = 100

def simulate(payoffs, rounds=10, skip=1):
  """
  Simulate the generation with payoff matrix T/R/P/S.

  In Nowak and May's model, each individual on the lattice plays the prisoner's dilemma with their eight nearest neighbors.
  At the end of each game round, an individual compares her score with that of her neighbors.
  If one of her neighbors earned a higher score, that player will adopt the strategy used by her most successful neighbor (presumably using some kind of randomization process to break ties).
  If no neighbor earned a higher score, that player will continue using the same strategy for the next round of play.
  All individuals switch strategies at the same time, and all have the same payoff structure.

  Link: https://plato.stanford.edu/entries/game-evolutionary/notes.html#2?tdsourcetag=s_pctim_aiomsg

  Arguments:
    payoffs: payoff matrix with struture [T, R, P, S]
  """
  # The simulation is performed on a N * N square lattice and starts with
  # the same initial configuation with 90% cooperators and 10% defectors.
  # 0 denotes cooperator, 1 denotes defector
  agent_matrix = np.random.choice(2, size=(N, N), p=(0.9, 0.1))

  [T, R, P, S] = payoffs
  payoff_matrix = [[R, S], [T, P]]

  for i in range(rounds):
    score_matrix = np.zeros((N, N))
    # In each round, each player plays with its eight neighbors.
    for r in range(N):
      for c in range(N):
        strategy_r_c = agent_matrix[r, c]
        for n_r in [r - 1, r, r + 1]:
          for n_c in [c - 1, c, c + 1]:
            if (n_r == r and n_c == c) or (n_r < 0 or n_r >= N) or (n_c < 0 or n_c >= N):
              continue
            else:
              neighbor_strategy = agent_matrix[n_r, n_c]
              score_matrix[r, c] += payoff_matrix[strategy_r_c][neighbor_strategy]
              score_matrix[n_r, n_c] += payoff_matrix[neighbor_strategy][strategy_r_c]
    # At the end of round, player_r_c changes its strategy.
    for r in range(N):
      for c in range(N):
        strategy_r_c = agent_matrix[r, c]
        max_neighbor_score = score_matrix[r, c]
        max_neighbor_strategy = strategy_r_c
        for n_r in [r - 1, r, r + 1]:
          for n_c in [c - 1, c, c + 1]:
            if (n_r == r and n_c == c) or (n_r < 0 or n_r >= N) or (n_c < 0 or n_c >= N):
              continue
            else:
              neighbor_strategy = agent_matrix[n_r, n_c]
              if score_matrix[n_r, n_c] > max_neighbor_score:
                max_neighbor_score = score_matrix[n_r, n_c]
                max_neighbor_strategy = neighbor_strategy
        agent_matrix[r, c] = max_neighbor_strategy
    if i % skip == 0:
      filename = '_'.join(['T=%0.2f' % T, 'P=%0.2f' % P, 'R=%0.2f' % R, 'S=%0.2f' % S, 'round=%d' % i])
      plt.imshow(agent_matrix, cmap=plt.cm.gray, vmin=0, vmax=1)
      plt.savefig('./img/%s.jpg' % filename)

if __name__ == "__main__":
    simulate([2.8, 1.1, 0.1, 0], 6, 1)
    simulate([1.2, 1.1, 0.1, 0], 10, 2)
    simulate([1.61, 1.01, 0.1, 0], 20, 5)