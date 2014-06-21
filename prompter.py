#!/usr/bin/env python

import sys

def prompt(fName):
  fptr = open(fName, 'w')

  lines = list()

  strategies = list()
  while True:
    newStrat = raw_input("Enter the name of a strategy (empty if done): ")
    if newStrat:
      strategies.append(newStrat)
    else:
      break

  lines.append("%s" % len(strategies))
  lines.extend(strategies)

  for winner in xrange(len(strategies)):
    line = list()
    for loser in xrange(winner + 1, len(strategies)):
      line.append(str(float(raw_input("How often does %s beat %s: " % (strategies[winner], strategies[loser])))))
    lines.append(" ".join(line))

  fptr.write("\n".join(lines))

if __name__ == '__main__':
  if len(sys.argv) == 2:
    prompt(sys.argv[1])
  else:
    print "Usage: %s <filename>" % sys.argv[0]
