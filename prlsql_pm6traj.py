#!/usr/bin/env python

#AUTHOR: Yue Liu
#EMAIL: yueliu96@uw.edu
#Created: 11/27/2018
#Edited: 12/01/2018

import glob,os,sys
from subprocess import Popen,PIPE

def checkcommand():
    if len(sys.argv)!=1:
        raise SystemExit('\npython dynamics4mopac_parallel.py\n')
    if not bool(glob.glob('*.xyz')):
        raise SystemExit(':::>_<:::No xyz Files Found!')

def mypathexist(dirs):
    for d in dirs:
        if os.path.exists(d):
            raise SystemExit(':::>_<:::%s Exists! Remove it and try again!' % d)

def issamecondition(n):
    x1,x2,x3 = 'could','be','anything'
    print('%d xyz files found in the current directory'  % n)
    print('-'*60+'\nPlease Specify their charge,multiplicity and temperature(K)\nInputs Must Be ###INTERGERS###\n'+'-'*60)
    try:
        c1=int(input('? Do they have the same charge [1--yes],[other--no]: '))
        if c1==1:
            x1=int(input('? charge: '))
        c2=int(input('? Do they have the same multiplicity [1--yes],[other--no]: '))
        if c2==1:
            x2=int(input('? multiplicity: '))
        c3=int(input('? Do they have the same temperature: [1--yes],[other--no]: '))
        if c3==1:
            x3=int(input('? temperature(K): '))
        return x1,x2,x3
    except:
        raise SystemExit(':::>_<:::Invalid Input!')

def anneal_yaml(fl,outfl,chg,mp,t):
    p1 = ['job: dynamics\n','geometry: '+fl+'\n','maxcycles: 20000\n','timestep: 0.001\n','interface: mopac\n',
'mopac_precise: yes\n','mopac_peptide_bond_fix: yes\n','method: pm6\n','modifiers: dispersion3, h_bonds4\n']
    p2 = ['modifier_h_bonds:\n','  h_bonds4_scale_charged: no\n','  h_bonds4_extra_scaling: {}\n','\n']
    p3 = ['thermostat: berendsen\nthermostat_tc: 0.05\n']
    try:
        if isinstance(chg,str):
            chg = int(input(('? charge of %s: ') % fl))
        pchg='charge: '+str(chg)+'\n'
        if isinstance(mp,str):
            mp = int(input(('? multiplicity of %s: ') % fl))
        if isinstance(t,str):
            t = int(input(('? temperature(K) of %s: ') %fl))
    except:
        raise SystemExit(':::>_<:::Invalid Input!')
    with open(outfl,'w') as fo:
        fo.writelines(p1)
        fo.write(pchg)
        if mp!=1:                                          
            fo.write('multiplicity: '+str(mp)+'\n')    
            fo.write('scf_cycles: 1000\n')             
        fo.writelines(p2)
        if mp!=1:
            fo.write('spin_restricted: uhf\n')
        fo.write('init_temp: '+str(t)+'\n')
        fo.writelines(p3)                                   
        fo.write('temperature: '+str(t)+'\n')

def tasklists_sh(alldirs,mydir):
    lines = []
    for dd in alldirs:
        line = 'cd '+mydir+'/'+dd+'; cuby4 anneal.yaml &>LOG\n'
        lines.append(line)
    with open('tasklists.sh','w') as fo:
        fo.writelines(lines)

def parallelrun_sh(n,user,mydir):
    p1 = '#!/bin/bash\n#SBATCH --job-name=dynamics\n#SBATCH --nodes=1\n#SBATCH --time=20:00:00\n#SBATCH --mem=100Gb\n'
    p2 = '#SBATCH --workdir='+mydir+'\n'
    p3 = '#SBATCH --partition=stf\n#SBATCH --account=stf\n\n'
    p4 = 'module load parallel_sql\nmodule load contrib/mopac16\n'
    p5 = 'source /usr/lusers/'+user+'/.rvm/scripts/rvm\n\n'
    p6 = 'ldd /sw/contrib/cuby4/cuby4/classes/algebra/algebra_c.so > ldd.log\n\n'
    p7 = 'parallel_sql --sql -a parallel --exit-on-term -j '+str(n)+'\n\n'
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
        yamlname = dxyz+'/anneal.yaml'
        anneal_yaml(fxyz,yamlname,charge,mtplct,temp)
        os.rename(fxyz,dxyz+'/'+fxyz)
    pwd = Popen('pwd',stdout=PIPE,shell=True).stdout.read().strip()
    who = Popen('whoami',stdout=PIPE,shell=True).stdout.read().strip()
    if isinstance(pwd,bytes):
        pwd = pwd.decode()
    if isinstance(who,bytes):
        who = who.decode()
    tasklists_sh(xyzdirs,pwd)
    parallelrun_sh(nxyz,who,pwd)
    print('**\(^O^)/**You are ready to run mopac dynamics! Check your files and do:\nmodule load parallel_sql; cat tasklists.sh | psu --load; sbatch parallel_run.sh')

if __name__=='__main__':
    checkcommand()
    dynamics()
                

        
