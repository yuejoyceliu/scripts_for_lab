#!/usr/bin/env python

import sys,os,math

Cores = 28
GauEnv = 'contrib/g16.b01'
PttAccMem = {'stf' : ['stf','stf','110G'], 'chem': ['chem','chem','200G'], 'ilahie' : ['ilahie','ilahie','200G'], 'ckpt' : ['ckpt','stf-ckpt','110G']}

def checkcommand():
    if len(sys.argv)!=5:
        raise SystemExit("Usage: python gaussian-mox.py input-file partition node-num time-float-in-hour")
    else:
        fl = sys.argv[1]
        if fl.split('.')[-1] != 'gjf' and fl.split('.')[-1] != 'com':
            print('Warning: This Script Only Can Be Used To Submit Gaussian Input Jobs!')
        try:
            pam = PttAccMem[sys.argv[2]]
            node = int(sys.argv[3])
            t = float(sys.argv[4])
            if (t-int(t))*60>=10:
                time = str(int(t))+':'+str(int((t-int(t))*60))+':00'
            else:
                time = str(int(t))+':0'+str(int((t-int(t))*60))+':00'
            with open(fl,'r') as fo:
                lines = fo.read()
                if '%lindaworker' in lines.lower():
                    if node==1:
                        raise SystemExit("Error: Please Remove %LINDAWORKER from %s for ONE Node!" % fl)
                else:
                    if node>1:
                        raise SystemExit("Error: Please Add %LINDAWORKER into %s for Multi-Nodes!" % fl)
                return fl,pam,node,time
        except IOError:
            raise SystemExit('Error: %s Not Found!' % sys.argv[1])
        except ValueError:
            raise SystemExit('Error: Time is a Float (in Hour)! Node is an Integer!')
        except KeyError:
            tmp = ''
            for p in PttAccMem.keys():
                tmp += p
                tmp += ' '
            raise SystemExit('Error: Available Partitions: [ %s]' % tmp)
        
def gaussian(fl,pam,n,t):
    nm = fl.split('.')[0]
    with open(nm+'.sh','w') as fo:
        fo.write('#!/bin/bash\n')
        fo.write('#SBATCH --job-name='+nm+'\n')
        fo.write('#SBATCH --nodes='+str(n)+'\n')
        fo.write('#SBATCH --ntasks-per-node='+str(Cores)+'\n')
        fo.write('#SBATCH --time='+t+'\n')
        fo.write('#SBATCH --mem='+pam[2]+'\n')
        fo.write('#SBATCH --workdir='+os.path.abspath('.')+'\n')
        fo.write('#SBATCH --partition='+pam[0]+'\n#SBATCH --account='+pam[1]+'\n\n')
        fo.write('# load Gaussian environment\nmodule load '+GauEnv+'\n\n')
        fo.write('#debugging information\necho \"**** Job Debugging Information ****\"\necho \"This job will run on $SLURM_JOB_NODELIST\"\necho \"\"\necho \"ENVIRONMENT VARIABLES\"\nset\necho \"**********************************************\"\n\n')
        if n>1:
            fo.write('# add linda nodes\nnodes=()\nnodes+=(`scontrol show hostnames $SLURM_JOB_NODELIST `)\nfor ((i=0; i<${#nodes[*]}-1; i++));\ndo\n\tstring+=${nodes[$i]}\n\tstring+=\",\"\ndone\nstring+=${nodes[$SLURM_NNODES-1]}\nsed -i -e \"s/%LindaWorker.*/%LindaWorker=$string/Ig\" '+fl+' \n\n')
            fo.write('# check that the Linda nodes are correct\nlindaline=(`grep -i \'lindaworker\' '+fl+'`)\nif [[ $lindaline == *$string ]]\nthen\n\techo \"Using the correct nodes for Linda\"\nelse\n\techo \"Using the wrong nodes for Linda\"\n\techo \"Nodes assigned by scheduler = $string\"\n\techo \"Line in Gaussian input file = $lindaline\"\n\texit 1\nfi\n\n')
        fo.write('#run Gaussian\ng16 '+fl+'\n\nexit 0\n')
    print('Please Check and Submit File '+nm+'.sh!')

if __name__=="__main__":
    fl,pam,n,t = checkcommand()
    gaussian(fl,pam,n,t)

