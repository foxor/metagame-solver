#!/usr/bin/env python

import numpy as np
from scipy import linalg
import sys

_strategies = []
_matchups = []
_undefined = []

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

def _remove_strategy(to_remove):
  global _strategies, _matchups
  _strategies.pop(to_remove)
  _matchups = np.delete(_matchups, to_remove, 0)
  _matchups = np.delete(_matchups, np.s_[to_remove], 1)

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
    _remove_strategy(to_remove)

  if non_viable:
    viability_check()

def solve(_desingularizing = False):
  try:
    return linalg.solve(_matchups, np.array([[0.5]] * _matchups.shape[0]))
  except:
    if _desingularizing:
      return None
    return _desingularize()

def _combinations(num, low, high):
  """
  Combinations are guaranted to be highest-to-lowest
  """
  for i in xrange(low, high):
    if num <= 1:
      yield [i]
    else:
      for subcombination in _combinations(num - 1, i + 1, high):
        if i in subcombination:
          continue
        subcombination.append(i)
        yield subcombination

def _desingularize():
  """
  The de-singularization method is to remove as few strategies as possible to result in a unique solution.  Once a unique solution is achieved to the subset matrix, we impose the sum(densities) = 1 requirement (that the matrix inversion is unaware of) and impose the average.  Therefore, if there is a singular matrix with 3 elements, and it becomes desingularized at 50-50 when one element has been removed, the solution is 33-33-33.
  """
  global _strategies, _matchups, _undefined
  backup_strat = _strategies[:]
  backup_match = np.copy(_matchups)
  for remove_size in xrange(1, len(_strategies)):
    for combination in _combinations(remove_size, 0, len(_strategies)):
      _strategies = backup_strat[:]
      _matchups = np.copy(backup_match)
      for test in combination:
        _remove_strategy(test)
      partial_solution = solve(True)
      if partial_solution != None:
        _undefined = list(backup_strat[x] for x in combination)
        return partial_solution

def display(solutions):
  for undefined in _undefined:
    print "%s occupies an undefined percentage of the meta-game" % undefined
  if _undefined:
    print "Assuming all variable decks are unplayed:"
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
