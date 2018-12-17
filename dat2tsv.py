#!/usr/bin/env python

'''
AUTHOR: Yue Liu
Created: 12/14/2018
Usage: python dat2tsv.py datafile
change the delimiter to '\t': split every line and join with '\t'
'''

from __future__ import print_function
import sys

try:
  fl = sys.argv[1]
  with open(fl,'r') as fo:
    lines=fo.readlines()
  newfl = fl.split('.')[0]+'.tsv'
  ctts=[]
  with open(newfl,'w') as fo:
    for line in lines:
      tl = line.split()
      tll = '\t'.join(tl)
      fo.write(tll+'\n')
  print('finish...')
except BaseException as err:
  print(' Usage:\npython dat2tsv.py datafile')
  print(' Error:')
  raise SystemExit(err)    
