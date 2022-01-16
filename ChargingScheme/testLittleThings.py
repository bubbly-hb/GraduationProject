import Constants
import os
import sys


def testClearList(ls):
    del ls[:]
    ls.append(1)
    Constants.NUM_OF_NODES = 0


ls = [1, 2]
print(ls)
testClearList(ls)
print(ls)
print('current path:', os.getcwd())
print('sys path:', sys.path)

for i in ls:
    print(i)
