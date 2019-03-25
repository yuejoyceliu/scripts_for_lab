#!/usr/bin/env python

'''
 AUTHOR: Yue Liu
 EMAIL: yueliu96@uw.edu
 Created on 11/26/2018
 Edited on 12/17/2018
Usage:
 python SCFextractor.py N (N=1: 1st standard orientation, N=-1: the last standard orientation)
Description:
 - extract the Nth SCF energy from all log files in the working directory.
 - N is an integer in -1,1,2,3,..., and N should not larger than the number of standard orientations in the input file!
'''

import sys,glob

def checkcommand():
    if len(sys.argv)!=2:
        raise SystemExit('\n\tpython SCFextractor.py number\n (1:1st SCF energy; -1:the last SCF energy)\n')
    try:
        n = int(sys.argv[1])
        out = 'SCFenergy_'+sys.argv[1]+'.csv'
        if n==0:
            raise SystemExit(':::>_<::: Input couldn\'t be zero!')
        return n,out
    except ValueError:
        raise SystemExit(':::>_<:::\"%s\" is supposed to be an integer!' % n)

def getvalues(s,n):
#split a string s by space and return the first n numbers, return float or a list of float
    i = 0
    values = []
    ls = s.split()
    for x in ls:
        if i>=n:
            break
        try:
            values.append(float(x))
            i += 1
        except:
            continue
    if not bool(values):
        raise SystemExit(':::>_<:::No Values Found in %s\n Warning: Delimiter Must be space or spaces' % ls)
    if n==1:
        return values[0]
    else:
        return values

def write_out(n,fl):
    alllog = glob.glob('*.log')
    alllog.sort(key=lambda x: (len(x),x),reverse=False)
    with open(fl,'w') as fo:
        fo.write('isomers,E_HF(hartrees)\n')
        for log in alllog:
           fo.write(SCFextract(log,n)+'\n')
    print('**\\(^O^)/**Please check '+fl+'!')

def SCFextract(fl,N):
    with open(fl,'r') as fo:
        lines = fo.readlines()
    eng = ['NA']
    for line in lines:
        if 'SCF Done' in line:
           eng.append(getvalues(line,1))
    try:
        float(eng[N])
        return fl.split('.')[0]+','+str(eng[N])
    except:
        raise SystemExit(':::>_<::: %s SCF Done Found in %s, but %s is specified!' % (len(eng)-1,fl,N))
 
if __name__=='__main__':
    n,out = checkcommand()
    write_out(n,out)
