#!/usr/bin/env python
import random
import sys

def pick_strategy(fptr):
  strategies = [(split_line[0], float(split_line[1][1:-1])) for split_line in 
    (line.strip().split(':') for line in fptr)
  ]
  strategies.sort(key=lambda x: random.random())
  remainder = random.random() * sum(x[1] for x in strategies)
  index = 0
  while True:
    remainder -= strategies[index][1]
    if remainder >= 0:
      index += 1
    else:
      print "Play a game with %s" % strategies[index][0]
      break

if __name__ == '__main__':
  if len(sys.argv) == 2:
    pick_strategy(open(sys.argv[1], 'r'))
  else:
    print "Usage: %s <filename>, where the file is a metagame evaluation" % sys.argv[0]
