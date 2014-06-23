#!/usr/bin/env python

import sys

def main(fName, depth):
  if depth == 0:
    depth = sys.maxint
  wins = dict()
  strategy_names = list()
  seen_strategies = set()
  for line in open(fName, 'r'):
    if '>' in line:
      strategy_names = line.strip().split('>')
    elif '<' in line:
      strategy_names = line.strip().split('<')[::-1]
    else:
      sys.stderr.write("This line doesn't make sense: %s" % line)
      continue

    strategy_names = list('.'.join(x.split('.')[:depth]) for x in strategy_names)
    seen_strategies = seen_strategies.union(strategy_names)

    previous_wins = 0
    if strategy_names[0] in wins:
      if strategy_names[1] in wins[strategy_names[0]]:
        previous_wins = wins[strategy_names[0]][strategy_names[1]]
    else:
      wins[strategy_names[0]] = dict()
    wins[strategy_names[0]][strategy_names[1]] = previous_wins + 1

  strategies = sorted(list(seen_strategies), key= lambda x: sum(y for y in wins[x].values()) if x in wins else 0)
  print "%d" % len(strategies)
  print "%s" % "\n".join(strategies)

  for primary in xrange(len(strategies)):
    percentages = list()
    for opponent in xrange(primary + 1, len(strategies)):
      primary_wins = wins[strategies[primary]][strategies[opponent]] if strategies[primary] in wins and strategies[opponent] in wins[strategies[primary]] else 0
      losses = wins[strategies[opponent]][strategies[primary]] if strategies[opponent] in wins and strategies[primary] in wins[strategies[opponent]] else 0
      percentages.append(str(float(primary_wins)/(primary_wins + losses) if (primary_wins + losses > 0) else 0.5))
    print " ".join(percentages)

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
