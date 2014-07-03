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

    if strategy_names[0] == strategy_names[1]:
      continue

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
    primary_name = strategies[primary]
    percentages = list()
    for opponent in xrange(primary + 1, len(strategies)):
      opponent_name = strategies[opponent]
      primary_wins = wins[primary_name][opponent_name] if primary_name in wins and opponent_name in wins[primary_name] else 0
      opponent_wins = wins[opponent_name][primary_name] if opponent_name in wins and primary_name in wins[opponent_name] else 0
      if primary_wins + opponent_wins == 0:
        primary_losses_total = sum(wins[x][primary_name] for x in wins if primary_name in wins[x])
        primary_wins_total = sum(x for x in wins[primary_name].values()) if primary_name in wins else 0
        primary_record = float(primary_wins_total) / (primary_wins_total + primary_losses_total)

        opponent_losses_total = sum(wins[x][opponent_name] for x in wins if opponent_name in wins[x])
        opponent_wins_total = sum(x for x in wins[opponent_name].values()) if opponent_name in wins else 0
        opponent_record = float(opponent_wins_total) / (opponent_wins_total + opponent_losses_total)

        percentages.append(str(float(primary_record + (1 - opponent_record)) / 2.0))
      else:
        percentages.append(str(float(primary_wins)/(primary_wins + opponent_wins)))
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
