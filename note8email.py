#!/usr/bin/env python

#this script is to turn on the email notification for the bash job. Already considering if email was on
#AUTHOR: Yue Liu 
#EMAIL: yueliu96@uw.edu

import sys,os
EMAIL = 'yueliu96@uw.edu'
NameKey = '#SBATCH --job-name='
MAILT = '#SBATCH --mail-type=ALL'
MAILU = '#SBATCH --mail-user='

def checkcommand(n):
    if n==3:
        jobfile = sys.argv[1]
        jobname = sys.argv[2]
    elif n==2:
        jobfile = sys.argv[1]
        jobname = True
    else:
        raise SystemExit('python note8email.py slurmfile.sh jobname\nor\npython note8email.py slurmfile')
    if os.path.isfile(jobfile):
        return jobfile,jobname
    else:
        raise SystemExit('%s File Not Found' % jobfile)

def note8email(x,jobname):
    with open(x,'r') as rdfo:
        lines = rdfo.readlines() 
    fo = open(x,'w')
    count = 1
    for line in lines:
        if line[:len(NameKey)]==NameKey:
            if jobname==True:
                pass
            else:
                line = NameKey+jobname+'\n'
        if line.lstrip()[:len(MAILU)]==MAILU:
            line = MAILU+EMAIL+'\n'
            count=2
        elif len(line)==1 and count==1:
            fo.write('#SBATCH --mail-type=ALL'+'\n')
            fo.write('#SBATCH --mail-user='+EMAIL+'\n')
            count=2
        fo.write(line)
    fo.close()
    print('**\(^O^)/** Job information will be sent to %s\nPlease run \'sbatch %s\'' % (EMAIL,x))

if __name__=='__main__':
    x,jobname = checkcommand(len(sys.argv))
    note8email(x,jobname)
