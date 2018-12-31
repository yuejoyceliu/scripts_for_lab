#!/usr/bin/env python

'''
 AUTHOR: Yue Liu
 EMAIL: yueliu96@uw.edu
 Created: 12/01/2018
 Edited: 12/05/2018
Usage: python pm6opt_parallel.py
find all xyz files in the working directory and make directories and inp.yaml for every one.
generate tasklists.sh file and parallel_run.sh file
after finishing, run 'sbatch parallel_run.sh'
after finishing, still in this directory, run 'python extract_pm6opt.py'
'''

import glob,os,sys
from subprocess import Popen,PIPE

nCORES = 28
YAML = 'inp.yaml'

if 1/2==0:
    myinput = raw_input
else:
    myinput = input 

def checkcommand():
    if len(sys.argv)!=1:
        raise SystemExit('\npython pm6opt_parallel.py\n')
    if not bool(glob.glob('*.xyz')):
        raise SystemExit(':::>_<:::No xyz Files Found!')

def mypathexist(dirs):
    for d in dirs:
        if os.path.exists(d):
            raise SystemExit(':::>_<:::%s Exists! Remove it and try again!' % d)

def issamecondition(n):
    x1,x2 = 'x1','x2'
    print('%d xyz files found in the current directory'  % n)
    print('-'*60+'\nPlease Specify their charge,multiplicity\n'+'-'*60)
    try:
        c1 = myinput('? Do they have the same charge [y/Y--yes],[other--no]: ')
        if c1.lower()=='y':
            x1 = int(myinput('? charge: '))
        c2 = myinput('? Do they have the same multiplicity [y/Y--yes],[other--no]: ')
        if c2.lower()=='y':
            x2 = int(myinput('? multiplicity: '))
        return x1,x2
    except:
        raise SystemExit(':::>_<:::Invalid Input!')

def yaml(fl,outfl,chg,mp):
    p1 = ['job: optimize\n','geometry: '+fl+'\n']
    p2 = ['interface: mopac\n','method: pm6\n','spin_restricted: auto_uhf\n','maxcycles: 2000\n','print: timing\n','mopac_precise: yes\n','mopac_peptide_bond_fix: yes\n','modifiers: dispersion3, h_bonds4\n','modifier_h_bonds:\n','  h_bonds4_scale_charged: no\n','  h_bonds4_extra_scaling: {}\n']
    try:
        if isinstance(chg,str):
            chg = int(myinput(('? charge of %s: ') % fl))
        if isinstance(mp,str):
            mp = int(myinput(('? multiplicity of %s: ') % fl))
    except:
        raise SystemExit(':::>_<:::Invalid Input!')
    with open(outfl,'w') as fo:
        fo.writelines(p1)
        fo.write('charge: '+str(chg)+'\n')                                          
        fo.write('multiplicity: '+str(mp)+'\n')    
        fo.writelines(p2)

def tasklists_sh(alldirs,mydir):
    lines = []
    for dd in alldirs:
        line = 'cd '+mydir+'/'+dd+'; cuby4 '+YAML+' &>LOG\n'
        lines.append(line)
    with open('tasklists.sh','w') as fo:
        fo.writelines(lines)

def parallelrun_sh(ntasks,user,mydir):
    p1 = '#!/bin/bash\n#SBATCH --job-name=pm6opt\n#SBATCH --nodes=1\n#SBATCH --time=10:00:00\n#SBATCH --mem=100G\n'
    p2 = '#SBATCH --workdir='+mydir+'\n'
    p3 = '#SBATCH --partition=stf\n#SBATCH --account=stf\n\n'
    p4 = 'module load parallel-20170722\nmodule load contrib/mopac16\n'
    p5 = 'source /usr/lusers/'+user+'/.rvm/scripts/rvm\n'
    p6 = 'ldd /sw/contrib/cuby4/cuby4/classes/algebra/algebra_c.so > ldd.log\n'
    p7 = 'cat tasklists.sh | parallel -j '+str(min(ntasks,nCORES))+'\n'
    with open('parallel_run.sh','w') as fo:
        fo.write(p1)
        fo.write(p2)
        fo.write(p3)
        fo.write(p4)
        fo.write(p5)
        fo.write(p6)
        fo.write(p7)

def opt():
    xyzfiles = glob.glob('*.xyz')
    xyzfiles.sort()
    xyzdirs = ['d'+d[:-4] for d in xyzfiles]
    mypathexist(xyzdirs)
    nxyz = len(xyzfiles)
    charge,mtplct = issamecondition(nxyz) 
    for i in range(nxyz):
        fxyz = xyzfiles[i]
        dxyz = xyzdirs[i]
        os.mkdir(dxyz)
        yamlname = dxyz+'/'+YAML
        yaml(fxyz,yamlname,charge,mtplct)
        os.rename(fxyz,dxyz+'/'+fxyz)
    pwd = Popen('pwd',stdout=PIPE,shell=True).stdout.read().strip().decode()
    who = Popen('whoami',stdout=PIPE,shell=True).stdout.read().strip().decode()
    tasklists_sh(xyzdirs,pwd)
    parallelrun_sh(nxyz,who,pwd)
    print('**\(^O^)/**%s tasks found! check and run:\n sbatch parallel_run.sh' % nxyz) 

if __name__=='__main__':
    checkcommand()
    opt()
                

        
