#!/usr/bin/env python

import numpy as np
from scipy import linalg

matchup_input = {
  'R': {'R': 0.5, 'P': 0.2, 'S': 0.6},
  'P': {'R': 0.8, 'P': 0.5, 'S': 0.3},
  'S': {'R': 0.4, 'P': 0.7, 'S': 0.5}
}

_name_indexes = []

def parse_input():
  pass

_name_indexes = [
  'R',
  'P',
  'S'
]

_matchups = np.array([
  [0.5, 0.2, 0.6],
  [0.8, 0.5, 0.3],
  [0.4, 0.7, 0.5]
])

constraints = np.array([
  [0.5],
  [0.5],
  [0.5]
])

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
