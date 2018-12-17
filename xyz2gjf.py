#!/usr/bin/env python

#AUTHOR: Yue Liu
#EMAIL: yueliu96@uw.edu
#Created on 11/28/2018

import os,sys

STRT = ['%mem=32gb\n','%nprocshared=28\n']
ROUTE = '# opt wb97xd/6-31+g(d,p) pop=min scf=(xqc,tight)\n'
CHGMP = '2 1\n'

def checkcommand(n):
    if n==2:
        infl = sys.argv[1]
        if os.path.isfile(infl):
            return infl,infl[:-4]
        else:
            raise SystemExit(':::>_<:::%s Not Found!' % infl)
    else:
        raise SystemExit('\npython xyz2gjf.py xyzfile\n')
def iscoords(xyzlists):
    realcoords = []
    for s in xyzlists:
        try:
            map(float,s.split()[1:])
            realcoords.append(s)
        except:
            pass
    return realcoords

    
def isxyzfile(s1,s2):
    try:
        natoms=int(s1.rstrip().lstrip())
        if s2 != natoms:
            raise SystemExit(':::>_<:::Not Found %d Atoms!' % natoms)
    except:
        print('1st line: '+s1.rstrip().lstrip())
        raise SystemExit(':::>_<:::Not Real xyz File!')

def xyz2gjf(f1,nm):
    with open(f1,'r') as f1o:
        lines = f1o.readlines()
    t_xyz = [x for x in lines if len(x.split())==4]
    coords = iscoords(t_xyz)
    isxyzfile(lines[0],len(coords))
    chk = '%chk='+nm+'.chk\n'
    f2 = nm+'.gjf'
    with open(f2,'w') as f2o:
        f2o.writelines(STRT)
        f2o.write(chk)
        f2o.write(ROUTE)
        f2o.write('\n')
        f2o.write('Complex '+nm+'\n')
        f2o.write('\n')
        f2o.write(CHGMP)
        f2o.writelines(coords)
        f2o.write('\n')
    print('**\(^O^)/**%s --> %s\n Route(default): %s Charge & Multiplicity(default): %s' % (f1,f2,ROUTE,CHGMP))

if __name__=='__main__':
    x,y=checkcommand(len(sys.argv)) 
    xyz2gjf(x,y)       
