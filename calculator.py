#!/usr/bin/env python

import sys

_RECORD_SOFTENING = 5
_MATCHUP_SOFTENING = 0

_wins = dict()
_strategies = list()
_strategy_names = list()
_seen_strategies = set()

def soften(real_wins, softening):
  softening_win_indexes = [(x + 1) % 2 for x in xrange(softening * 2 - (real_wins[0] + real_wins[1]))]
  return (
    real_wins[0] + len([x for x in softening_win_indexes if x == 0]),
    real_wins[1] + len([x for x in softening_win_indexes if x == 1])
  )

def record(strategy):
  real_wins = (
    sum(x for x in _wins[strategy].values()) if strategy in _wins else 0,
    sum(_wins[x][strategy] for x in _wins if strategy in _wins[x])
  )
  return soften(real_wins, _RECORD_SOFTENING)

def matchup(strategy1, strategy2):
  real_wins = (
    _wins[strategy1][strategy2] if strategy1 in _wins and strategy2 in _wins[strategy1] else 0,
    _wins[strategy2][strategy1] if strategy2 in _wins and strategy1 in _wins[strategy2] else 0
  )
  
  total_matches = real_wins[0] + real_wins[1]
  if total_matches > 0:
    softened_matchup = soften(real_wins, _MATCHUP_SOFTENING)
    return float(softened_matchup[0]) / (softened_matchup[0] + softened_matchup[1])

  records = (record(strategy1), record(strategy2))
  return float(records[0][0] + records[1][1]) / (records[0][0] + records[0][1] + records[1][0] + records[1][1])

def parse(fName, depth):
  global _wins, _strategy_names, _seen_strategies, _strategies
  if depth == 0:
    depth = sys.maxint
  for line in open(fName, 'r'):
    if '>' in line:
      strategy_names = line.strip().split('>')
    elif '<' in line:
      strategy_names = line.strip().split('<')[::-1]
    else:
      sys.stderr.write("This line doesn't make sense: %s" % line)
      continue

    strategy_names = list('.'.join(x.split('.')[:depth]) for x in strategy_names)

    if strategy_names[0] == strategy_names[1]:
      continue

    _seen_strategies = _seen_strategies.union(strategy_names)

    previous_wins = 0
    if strategy_names[0] in _wins:
      if strategy_names[1] in _wins[strategy_names[0]]:
        previous_wins = _wins[strategy_names[0]][strategy_names[1]]
    else:
      _wins[strategy_names[0]] = dict()
    _wins[strategy_names[0]][strategy_names[1]] = previous_wins + 1

  _strategies = sorted(list(_seen_strategies), key= lambda x: sum(y for y in _wins[x].values()) if x in _wins else 0)

def calculate():
  for primary in xrange(len(_strategies)):
    primary_name = _strategies[primary]
    percentages = list()
    for opponent in xrange(primary + 1, len(_strategies)):
      opponent_name = _strategies[opponent]
      percentages.append(matchup(primary_name, opponent_name))
    yield percentages

def serialize(percentage_lists):
  print "%d" % len(_strategies)
  print "%s" % "\n".join(_strategies)
  for percentages in percentage_lists:
    print " ".join(str(x) for x in percentages)

def main(fName, depth):
  parse(fName, depth)
  serialize(calculate())

if __name__ == '__main__':
  if len(sys.argv) == 3:
    main(sys.argv[1], int(sys.argv[2]))
  elif len(sys.argv) == 2:
    main(sys.argv[1], 0)
  else:
    print "Usage: %s <filename> [depth]" % sys.argv[0]
    print "If depth is specified and nonzero, calculator ignores"
    print "strategy names after the specified dot."
    print "Example: with depth 2, Mage.Freeze.Pyro becomes Mage.Freeze"
    print "this is useful for matching sample size to inference specificity"
