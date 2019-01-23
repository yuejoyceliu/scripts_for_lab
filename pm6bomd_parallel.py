#!/usr/bin/env python

#AUTHOR: Yue Liu
#EMAIL: yueliu96@uw.edu
#Created: 11/27/2018
#Edited: 12/29/2018

import glob,os,sys
from subprocess import Popen,PIPE

nCORES = 28
YAML = 'anneal.yaml'

if 1/2==0:
    myinput = raw_input
else:
    myinput = input

def checkcommand():
    if len(sys.argv)!=1:
        raise SystemExit('\npython pm6bomd_parallel.py\n')
    if not bool(glob.glob('*.xyz')):
        raise SystemExit(':::>_<:::No xyz Files Found!')

def mypathexist(dirs):
    for d in dirs:
        if os.path.exists(d):
            raise SystemExit(':::>_<:::%s Exists! Remove it and try again!' % d)

def issamecondition(n):
    x1,x2,x3 = 'could','be','anything'
    print('%d xyz files found in the current directory'  % n)
    print('-'*60+'\nPlease Specify their charge,multiplicity and temperature(K)\n'+'-'*60)
    try:
        c1 = myinput('? Do they have the same charge [y/Y--yes],[other--no]: ')
        if c1.lower()=='y':
            x1=int(myinput('? charge: '))
        c2 = myinput('? Do they have the same multiplicity [y/Y--yes],[other--no]: ')
        if c2.lower()=='y':
            x2=int(myinput('? multiplicity: '))
        c3 = myinput('? Do they have the same temperature: [y/Y--yes],[other--no]: ')
        if c3.lower()=='y':
            x3=float(myinput('? temperature(K): '))
        return x1,x2,x3
    except:
        raise SystemExit(':::>_<:::Invalid Input!')

def yaml(fl,outfl,chg,mp,t):
    p1 = ['job: dynamics\n','geometry: '+fl+'\n']
    p2 = ['interface: mopac\n','method: pm6\n','mopac_precise: yes\n','mopac_peptide_bond_fix: yes\n','modifiers: dispersion3, h_bonds4\n']
    p3 = ['modifier_h_bonds:\n','  h_bonds4_scale_charged: no\n','  h_bonds4_extra_scaling: {}\n','maxcycles: 20000\n','timestep: 0.001\n']
    p4 = ['thermostat: berendsen\nthermostat_tc: 0.05\n']
    try:
        if isinstance(chg,str):
            chg = int(myinput(('? charge of %s: ') % fl))
        if isinstance(mp,str):
            mp = int(myinput(('? multiplicity of %s: ') % fl))
        if isinstance(t,str):
            t = float(myinput(('? temperature(K) of %s: ') %fl))
    except:
        raise SystemExit(':::>_<:::Invalid Input!')
    with open(outfl,'w') as fo:
        fo.writelines(p1)
        fo.write('charge: '+str(chg)+'\n')                                   
        fo.write('multiplicity: '+str(mp)+'\n')
        fo.write('spin_restricted: auto_uhf\n')
        if mp!=1:
            fo.write('scf_cycles: 1000\n')             
        fo.writelines(p2)
        fo.writelines(p3)
        fo.write('init_temp: '+str(t)+'\n')
        fo.write('temperature: '+str(t)+'\n')
        fo.writelines(p4)                                   

def tasklists_sh(alldirs,mydir):
    lines = []
    for dd in alldirs:
        line = 'cd '+mydir+'/'+dd+'; cuby4 '+YAML+' &>LOG\n'
        lines.append(line)
    with open('tasklists.sh','w') as fo:
        fo.writelines(lines)

def parallelrun_sh(n,user,mydir):
    p1 = '#!/bin/bash\n#SBATCH --job-name=dynamics\n#SBATCH --nodes=1\n#SBATCH --time=20:00:00\n#SBATCH --mem=100G\n'
    p2 = '#SBATCH --workdir='+mydir+'\n'
    p3 = '#SBATCH --partition=stf\n#SBATCH --account=stf\n\n'
    p4 = 'module load parallel-20170722\nmodule load contrib/mopac16\n'
    p5 = 'source /usr/lusers/'+user+'/.rvm/scripts/rvm\n'
    p6 = 'ldd /sw/contrib/cuby4/cuby4/classes/algebra/algebra_c.so > ldd.log\n'
    p7 = 'cat tasklists.sh | parallel -j '+str(min(nCORES,n))+'\n'
    with open('parallel_run.sh','w') as fo:
        fo.write(p1)
        fo.write(p2)
        fo.write(p3)
        fo.write(p4)
        fo.write(p5)
        fo.write(p6)
        fo.write(p7)

def dynamics():
    xyzfiles = glob.glob('*.xyz')
    xyzfiles.sort()
    xyzdirs = ['d'+d[:-4] for d in xyzfiles]
    mypathexist(xyzdirs)
    nxyz = len(xyzfiles)
    charge,mtplct,temp = issamecondition(nxyz) 
    for i in range(nxyz):
        fxyz = xyzfiles[i]
        dxyz = xyzdirs[i]
        os.mkdir(dxyz)
        yamlname = dxyz+'/'+YAML
        yaml(fxyz,yamlname,charge,mtplct,temp)
        os.rename(fxyz,dxyz+'/'+fxyz)
    pwd = Popen('pwd',stdout=PIPE,shell=True).stdout.read().strip().decode()
    who = Popen('whoami',stdout=PIPE,shell=True).stdout.read().strip().decode()
    tasklists_sh(xyzdirs,pwd)
    parallelrun_sh(nxyz,who,pwd)
    print('**\(^O^)/**You are ready to run mopac dynamics! Check and Run:\n sbatch parallel_run.sh')

if __name__=='__main__':
    checkcommand()
    dynamics()
                

        
