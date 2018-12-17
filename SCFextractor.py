#!/usr/bin/env python

#extract 'Step number' & 'SCF Done' from all log files in the working directory

import os,glob,time

def read2writelog(f,out):
    wrout = open(out,'a')
    wrout.write('######'+f+'######'+'\n')
    with open(f,'r') as fo:
        lines = fo.readlines()
    for line in lines:
        if line.lstrip()[:11]=='Step number':
            wrout.write(line)
        if line.lstrip()[:8]=='SCF Done':
            wrout.write(line)
    wrout.write('\n')
    wrout.close()


def extractor():
    x = time.strftime('%Y%m%d%H%M%S',time.localtime())
    x = 'opt'+x+'.txt'
    alllog = glob.glob('*.log')
    alllog.sort()
    for log in alllog:
        with open(x,'a') as fout:
            read2writelog(log,x)
    print('**\(^O^)/**Please check %s file' % x)

if __name__=='__main__':
    extractor() 
