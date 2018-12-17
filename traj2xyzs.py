#!/usr/bin/env python
'''
 AUTHOR: Yue Liu
 EMAIL: yueliu96@uw.edu
 Created: 12/04/2018
 Usage: python traj2xyz.py N
For all child directories in the working directory, it will find trajectory_anneal.xyz file to extract the 1st struct for every N structures.
If N=100 and it has 20,000 cycles in the trajectory_anneal.xyz, you will get 20,000/100=200 structures
'''

TRAJ = 'trajectory_anneal.xyz'

import sys,os
 
def checkcommand():
    if len(sys.argv)==2:
        return sys.argv[1]
    else:
        raise SystemExit(' python traj2xyz.py N\nif N=200, it will generate 200 snapshots from trajectory.')

def readtraj(d,stride):
    fl = d+'/'+TRAJ
    if os.path.isfile(fl):
        with open(fl,'r') as fo:
            lines = fo.readlines()
        natom = int(lines[0].strip())
        ncycle = len(lines)/(natom+2)
        n = ncycle/stride
        newd = d+'_traj'
        os.mkdir(newd)
        for i in range(n):
            snap = lines[i*stride*(natom+2):(i*stride+1)*(natom+2)]
            convert2xyz(snap,newd+'/'+d[1:],i)
        print(' (@\'.\'@) %s cycles in %s -->  %s *snap*xyz files in %s folder!' % (ncycle,fl,n,newd))
    else:
        print('\'<_\' %s Not Found!' % fl)

def convert2xyz(lss,f,j):
    flname = f+'_snap'+str(j+1)+'.xyz'
    lxyz = [lss[0].strip()+'\n','\n']
    for ss in lss[2:]:
        ssp = ss.split()
        xyz = '%2s%16s%16s%16s' % (ssp[0],ssp[1],ssp[2],ssp[3])
        lxyz.append(xyz+'\n')
    with open(flname,'w') as fo:
        fo.writelines(lxyz)

def traj2xyz(n):
    allfd = os.listdir('.')
    alldirs = [x for x in allfd if os.path.isdir(x)]
    for everydir in alldirs:
        readtraj(everydir,n)
    print('**\(^O^)/** Please check all snap files in the above folders!')

if __name__=='__main__':
    stride = int(checkcommand())
    traj2xyz(stride)
    
