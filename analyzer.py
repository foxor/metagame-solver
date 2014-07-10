#!/usr/bin/env python

import sys

import calculator

_LIST_ENTRIES = 5

_stable_meta = list()
_observed_meta = list()

def printTop(headline, data):
  print "\n"
  print headline
  for datum in sorted(data, key=lambda x: -x[1])[:_LIST_ENTRIES]:
    print "%s: %.2f%%" % datum

def record():
  def normalized_record(strategy):
    wins,losses = calculator.record(strategy)
    return float(wins * 100) / (wins + losses)
  return ((x, normalized_record(x)) for x in calculator._strategies)

def stable_metagame(metagameFilename):
  global _stable_meta
  fptr = open(metagameFilename, 'r')
  _stable_meta = [(split_line[0], float(split_line[1][1:-1])) for split_line in 
    (line.strip().split(':') for line in fptr)
  ]
  return _stable_meta

def observed_metagame(logFilename):
  global _observed_meta
  total_encounters = 0
  encounters = dict()
  for line in open(logFilename, 'r'):
    opponent = None
    if '>' in line:
      opponent = line.strip().split('>')[1]
    elif '<' in line:
      opponent = line.strip().split('<')[1]
    else:
      continue

    total_encounters += 1
    if opponent in encounters:
      encounters[opponent] = encounters[opponent] + 1
    else:
      encounters[opponent] = 1

  for opponent in encounters:
    _observed_meta.append((opponent, float(encounters[opponent] * 100) / total_encounters))
  return _observed_meta

def antiObserved():
  for strategy in calculator._strategies:
    win_rate = 0.0
    for density in _observed_meta:
      win_rate += calculator.matchup(strategy, density[0]) * density[1]
    yield (strategy, win_rate)

def underplayed():
  for density in _observed_meta:
    stable_density = [x for x in _stable_meta if x[0] == density[0]]
    stable_density = stable_density[0] if stable_density else ('', 0.0)
    yield (density[0], stable_density[1] - density[1])

def overplayed():
  for density in _observed_meta:
    stable_density = [x for x in _stable_meta if x[0] == density[0]]
    stable_density = stable_density[0] if stable_density else ('', 0.0)
    yield (density[0], density[1] - stable_density[1])

def main(logFilename, metagameFilename):
  calculator.parse(logFilename, 0)
  printTop("Observed most popular:", observed_metagame(logFilename))
  printTop("Most popular in a stable metagame:", stable_metagame(metagameFilename))
  printTop("Most underplayed in observed meta:", underplayed())
  printTop("Most overplayed in observed meta:", overplayed())
  printTop("Top win percentages:", record())
  printTop("Best against observed metagame:", antiObserved())

if __name__ == '__main__':
  if len(sys.argv) == 3:
    main(sys.argv[1], sys.argv[2])
  else:
    print "Usage: %s <stats filename> <metagame filename>" % sys.argv[0]
