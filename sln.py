#!/usr/bin/env python

import numpy as np
from scipy import linalg

matchup_input = {
  'R': {'R': 0.5, 'P': 0.2, 'S': 0.6},
  'P': {'R': 0.8, 'P': 0.5, 'S': 0.3},
  'S': {'R': 0.4, 'P': 0.7, 'S': 0.5}
}

_name_indexes = []
_matchups = []

def parse_input():
  global _name_indexes, _matchups

  _name_indexes = list(matchup_input.keys())
  name_lookup = dict((_name_indexes[i], i) for i in xrange(len(_name_indexes)))

  _matchups = np.array(
    list(
      list(matchup_pair[1] for matchup_pair in 
        sorted(
          list((matchup, matchup_input[strategy][matchup]) for matchup in matchup_input[strategy]),
          key= lambda matchup_pair: name_lookup[matchup_pair[0]]
        )
      ) for strategy in _name_indexes
    )
  )
  import pdb;pdb.set_trace()

  
  #_matchups = np.array([
  #  [0.5, 0.2, 0.6],
  #  [0.8, 0.5, 0.3],
  #  [0.4, 0.7, 0.5]
  #])

def viability_check():
  """
  The idea here is to remove all strategies that are strictly worse than another strategy are removed
  """
  pass

def solve():
  return linalg.solve(_matchups, np.array([[0.5]] * _matchups.shape[0]))

def display(solutions):
  for i in xrange(len(solutions)):
    print "%s: %.2f%%" % (_name_indexes[i], solutions[i] * 100.0)

if __name__ == '__main__':
  parse_input()
  viability_check()
  display(solve())
