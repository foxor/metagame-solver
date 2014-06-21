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
  global _strategies, _matchups

  non_viable = list()
  for check in xrange(len(_strategies)):
    for test in xrange(len(_strategies)):
      if check == test:
        continue
      foundBetter = False
      for matchup in xrange(len(_strategies)):
        if _matchups[check][matchup] > _matchups[test][matchup]:
          foundBetter = True
          break
      if not foundBetter:
        non_viable.append(check)
        break

  # Iterating through this backwards keeps us from stepping on our indexes
  for to_remove in non_viable[::-1]:
    _strategies.pop(to_remove)
    _matchups = np.delete(_matchups, to_remove, 0)
    _matchups = np.delete(_matchups, np.s_[to_remove], 1)

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
