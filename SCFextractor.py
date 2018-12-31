#!/usr/bin/env python

#Author: Yue Liu
#Usage: python SCFextractor
#extract 'Step number','Predicted change' & 'SCF Done' from all log files in the working directory

import os,glob,time

def read2writelog(f,out):
    wrout = open(out,'a')
    wrout.write(f.center(80,'-')+'\n')
    with open(f,'r') as fo:
        lines = fo.readlines()
    for line in lines:
        line=line.lstrip()#keep \n at right
        if line.startswith('Step number'):
            wrout.write(line)
        if line.startswith('Predicted change'):
            wrout.write('\t'+line)
        if line.startswith('SCF Done'):
            wrout.write('\t\t'+line)
    wrout.write('\n')
    wrout.close()


def extractor():
    x = time.strftime('%Y%m%d%H%M%S',time.localtime())
    x = 'opt'+x+'.txt'
    alllog = glob.glob('*.log')
    alllog.sort(key=lambda x: (len(x),x),reverse=False)
    for log in alllog:
        with open(x,'a') as fout:
            read2writelog(log,x)
    print('**\(^O^)/**Please check %s file' % x)

if __name__=='__main__':
    extractor() 
