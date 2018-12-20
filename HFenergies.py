#!/usr/bin/env python
'''
 AUTHOR: Yue Liu
 EMAIL: yueliu96@uw.edu
 Created: 12/03/2018
 Edited: 12/08/2018
 Usage: python HFenergies.py
 Description:
used to extract HF Energy(the last SCF Done) from every log file in the current directory.
if not optimized(not found 'Stationary point found'), return NA.
you will get HFenergies.csv with energy in the ascending order.
'''
import sys,glob,csv

def checkcommand():
    if len(sys.argv)==1:
        if bool(glob.glob('*log')):
            return glob.glob('*log')
        else:
            raise SystemExit(':::>_<::: No LOG Founded!')
    else:
        raise SystemExit('\n python HFenergies.py\n')

def scfdone(fl):
    with open(fl,'r') as fo:
        lines = fo.readlines()
    optend = []
    scf = []
    for l in lines:
        if 'Stationary point found' in l:
            optend.append(l)
        elif l.lstrip().startswith('SCF Done'):
            scf.append(l)
    if bool(optend):
        energy = getvalue(scf[-1])
        return energy
    else:
        print('\'<_\' Warning: %s Not Optimized!' % fl)
        return 'NA'

def getvalue(s):
#return the first number in the string s
    nums = list(map(str,range(10)))
    nums.append('-')
    ls = s.split()
    for x in ls:
        if x[0] in nums:
            return x
    return 'none' 
        
def HFenergies(logs):
    result=[]
    for log in logs:
        e = scfdone(log)
        result.append([log.split('.')[0],e])
    result.sort(key=lambda x: x[1],reverse=True)
    out = 'HFenergies.csv'
    with open(out,'w') as fo:
        wrfo = csv.writer(fo)
        wrfo.writerow(['struct','energy(Hartrees)'])
        wrfo.writerows(result)
    print('**\(^O^)/**Please check your output file: %s!' % out)


if __name__=='__main__':
    optlogs = checkcommand()
    HFenergies(optlogs)
 
