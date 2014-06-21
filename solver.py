#!/usr/bin/env python

import numpy as np
from scipy import linalg
import sys

_strategies = []
_matchups = []

def parse_input(fName):
  global _strategies, _matchups

  fptr = open(fName, 'r')

  num_strategies = int(fptr.readline().strip())
  _strategies = list(fptr.readline().strip() for x in xrange(num_strategies))

  _matchups = np.identity(num_strategies) * 0.5

  line_index = 0
  for matchup_line in (fptr.readline() for x in xrange(num_strategies - 1)):
    match_index = line_index + 1
    for matchup in (float(x) for x in matchup_line.strip().split(' ')):
      _matchups[line_index][match_index] = matchup
      _matchups[match_index][line_index] = 1.0 - matchup
      match_index += 1
    line_index += 1

def viability_check():
  """
  The idea here is to remove all strategies that are strictly worse than another strategy
  """
  pass

def solve():
  return linalg.solve(_matchups, np.array([[0.5]] * _matchups.shape[0]))

def display(solutions):
  for i in xrange(len(solutions)):
    print "%s: %.2f%%" % (_strategies[i], solutions[i] * 100.0)

def main(fName):
  parse_input(fName)
  viability_check()
  display(solve())

if __name__ == '__main__':
  if len(sys.argv) == 2:
    main(sys.argv[1])
  else:
    print "Usage: %s <filename>" % sys.argv[0]
