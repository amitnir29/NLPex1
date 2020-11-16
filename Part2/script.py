import sys

print(open(sys.argv[1], 'r').read().count(" ") + open(sys.argv[1], 'r').read().count("\n"))
