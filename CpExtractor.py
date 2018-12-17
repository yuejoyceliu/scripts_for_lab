#!/usr/bin/env python

#Created: 11/29/2018
#Extract Cp from all *_freq.csv files in the working direcotry
#Usage: python CpExtractor.py

import glob

def findCp(fl):
    key='key'
    with open(fl,'r') as fo:
        lines=fo.readlines()
    for i in range(len(lines)):
        line = lines[i]
        if 'Cp' in line:
            key=i+1
            break
    if isinstance(key,int):
        keyline = lines[key].strip()
        keylist = keyline.split(',')
        return keylist[-1]
    else:
        raise SystemExit(':::>_<:::Cp Not Found! in '+fl)
        
def CpExtractor():
    xx=glob.glob('*_freq.csv')
    xx.sort()
    if not bool(xx):
        raise SystemExit(':::>_<:::No *_freq.csv Files!')
    fo=open('Cp.csv','w')
    fo.write('struct,Cp(J/mol/K)\n')
    for x in xx:
        tmpt = findCp(x)
        fo.write(x+','+tmpt+'\n')
    fo.close()
    print('**\(^O^)/**please check Cp.csv!')

if __name__=='__main__':
    CpExtractor()
        

