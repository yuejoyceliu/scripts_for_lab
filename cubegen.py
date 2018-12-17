#!/usr/bin/env python

'''
 AUTHOR: Yue Liu
 EMAIL: yueliu96@uw.edu
 Created: 12/09/2018
Need tddft log and chk file in the same folder and generate cube files
From tddft log file find number of alpha electrons and virtual alpha electrons to calculate where to find beta electron orbital: mo(beta)+=mo(NAE)+mo(NVA)
From log to find the name of chk file to create fchk if fchk not found. fchk file shoud have the same name with chk file.
Read all orbitals in one excited state and turn them to cube files
Write a bash script to run parallelly(tN_logname.sh) and submit it to hyak-ckpt
'''

from __future__ import print_function
import sys,os,subprocess

def checkcommand():
    if len(sys.argv)!=3:
        raise SystemExit('Usage: python logchk2cube.py tddftlog Nstate')
    else:
        fa = sys.argv[1]
        if fa.split('.')[-1]!='log':
            raise SystemExit('Error: %s Must End with \'log\'' % fa)
        if os.path.isfile(fa):
            return fa,sys.argv[2]
        else:
            raise SystemExit('Error: %s Not Found!' % fa)

def readlog(fl,n):
    with open(fl,'r') as fo:
        lines = fo.readlines()
    i=-1
    es = 'Excited State%4s' % n
    proc = []
    for line in lines:
        i += 1
        if '%chk=' in line:
            chk = line.strip().split('=')[-1]
            if not os.path.isfile(chk):
                raise SystemExit(':::>_<:::%s Not Found!' % chk)
        elif 'alpha electrons' in line:
            nae = int(line.split()[0])
        elif 'NVA=' in line:
            nva = int(line.split('NVA=')[1].split()[0])
        elif es in line:
             keyi = i
             try:
                 while True:
                     keyi += 1
                     x = lines[keyi] 
                     int(x.lstrip()[0])
                     proc.append(x)
             except:
                 return chk,nae+nva,proc
    raise SystemExit(':::>_<::: Number of state out of range!')
        
def writecube(m,n,proc,nm,cnm):
    fchk = cnm+'.fchk'
    orbit = []
    for p in proc:
        g = p.split()[0]
        e = p.split()[2]
        if g not in orbit:
            orbit.append(g)
        if e not in orbit:
            orbit.append(e)
    cubes = []
    for x in orbit:
        fc = nm+'_'+x+'.cube'
        if os.path.isfile(fc):
            continue
        else:
            if 'A' in x:
                cubes.append('cubegen 0 mo='+x.strip('A')+' '+fchk+' '+fc+' 0 h\n')
            if 'B' in x:
                cubes.append('cubegen 0 mo='+str(int(x.strip('B'))+n)+' '+fchk+' '+fc+' 0 h\n')
    cubes.sort(key=lambda x: (len(x),x))
    task = 't'+str(m)+'_'+nm+'.txt'
    with open(task,'w') as fo:
        fo.writelines(cubes)
    return task,len(cubes)
                 
def writebash(chk,task,nt):
    fchk = chk.split('.')[0]+'.fchk'
    mybash = task.split('.')[0]+'.sh'   
    with open(mybash,'w') as fsh:
        fsh.write('#!/bin/bash\n#SBATCH --job-name=fchk_cube\n#SBATCH --nodes=1\n#SBATCH --time=10:00\n#SBATCH --mem=100G\n')
        pwd = subprocess.Popen('pwd',stdout=subprocess.PIPE,shell=True).stdout.read()
        fsh.write('#SBATCH --workdir='+pwd.decode())
        fsh.write('#SBATCH --partition=ckpt\n#SBATCH --account=stf-ckpt\n\n')
        #fsh.write('#SBATCH --partition=ilahie\n#SBATCH --account=ilahie\n\n')
        fsh.write('echo \'This job will run on\' $SLURM_JOB_NODELIST\n')
        fsh.write('#set up time\nstart=$(date +%s)\n\n')
        fsh.write('#load Gaussian environment\nmodule load contrib/g16.b01\n\n')
        if not os.path.isfile(fchk):
            fsh.write('#use checkpoint file to generte formatted one\nformchk '+chk+' '+fchk+'\n\n')
        fsh.write('#load parallel environment\nmodule load parallel-20170722\n')
        fsh.write('cat '+task+' | parallel -j 28\n\n')
        fsh.write('end=$(date +%s)\necho \'Elapsed Time: \'$(($end-$start))\'s\'')
    subprocess.call('sbatch '+mybash,shell=True)
    print('**\(^O^)/**%s submitted to ckpt, please wait a little bit!' % mybash)

def logchk2cube(flog,nstt):
    chk,nava,process = readlog(flog,nstt)
    flnm = flog.split('.')[0]
    tasklist,ntask = writecube(nstt,nava,process,flog.split('.')[0],chk.split('.')[0])
    writebash(chk,tasklist,ntask)

if __name__=='__main__':
    log,N = checkcommand()
    logchk2cube(log,N)

   
'''
def myinput(fchk):
    nae,nbe,nava = cubegen(fchk)
    print('-'*50,'\nSpecify orbital numbers to visualize respectively','\n[number to add orbital],[<enter> to continue]','\n'+'-'*50)
    A=[]
    B=[]
    try:
        print('  Alpha Electronic orbital: [alpha valence electrons: 1-%d]' % nae)
        while True:
            A.append(int(input('alpha mo = ')))
    except (SyntaxError,NameError,ValueError):
        mo = ['cubegen 0 mo='+str(a)+' '+fchk+' '+fchk.split('.')[0]+str(a)+'A.cube 0 h &\n' for a in A]
        try:
            print('  Beta Electronic orbital: [beta valence electrons:1-%d]' % nbe)
            while True:
                B.append(int(input('beta mo = ')))
        except (SyntaxError,NameError,ValueError):
            mo.extend(['cubegen 0 mo='+str(b+nava)+' '+fchk+' '+fchk.split('.')[0]+str(b)+'B.cube 0 h &\n' for b in B])
    return mo

def cubegen(fchk):
    with open(fchk,'r') as fo:
        lines=fo.readlines()
    for line in lines[:50]:
        if 'Number of alpha electrons' in line:
            NAE = int(line.split()[-1])
        elif 'Number of beta electrons' in line:
            NBE = int(line.split()[-1])
        elif 'Number of independent functions' in line:
            NApVA = int(line.split()[-1])
    try:
        return NAE,NBE,NApVA
    except NameError as err:
        raise SystemExit(err) 
'''
