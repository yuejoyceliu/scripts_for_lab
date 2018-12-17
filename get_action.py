#!/usr/bin/env python

import sys,time

def checkcommand(n):
    if n!=5:
        raise SystemExit('python script.py name_prefix name_sufix num_start num_end\ngenerate a list of name=prefix+num+suffix')
    return sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4])+1

def generator(a,b,m,n):
    name=[]
    for i in range(m,n):
        name.append(a+str(i)+b+'\n')
    x = time.strftime('%Y%m%d%H%M%S',time.localtime())
    x = 'log'+x+'.txt'
    with open('name.txt','w') as fo:
        fo.writelines(name)
    print('**\(^O^)/** check name.txt & run mergeOPTlog.py!')

if __name__=='__main__':
    prefix,suffix,strt,end=checkcommand(len(sys.argv))
    generator(prefix,suffix,strt,end)
