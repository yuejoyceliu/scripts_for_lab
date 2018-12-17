#!/usr/bin/env python

'''
 AUTHOR: Yue Liu
 EMAIL: yueliu96@uw.edu
 Created: 12/03/2018
used to restart gaussian opt job if it's not finished because of timelimited 
or add more states for tddft to continue calculation, but the previous one must be done.
'''
import sys,os,re

def checkcommand():
    if len(sys.argv)!=2:
        raise SystemExit('\npython restart_gaussian.py oldgjf\n')
    if sys.argv[1][-4:]!='.gjf':
        raise SystemExit('\'<_\'%s suffix must be \'gjf\'!' % sys.argv[1])
    if not os.path.isfile(sys.argv[1]):
        raise SystemExit('\'<_\'%s Not Found!' % sys.argv[1])
    return sys.argv[1]

def restart(fl):
    with open(fl,'r') as fo:
        lines=fo.readlines()
    lk = [l for l in lines if l.startswith('%') and not l.lower().startswith('%lindaworker') and not l.lower().startswith('%oldchk')]
    rt = [l for l in lines if l.startswith('#')]
    if not bool(lk) or not bool(rt):
        raise SystemExit('\'<_\'No link section or/and route section found!')
    rtstr = rt[0].lower()
    if 'opt' in rtstr:
        link = writelink(lk,'rstrt')
        route = writeopt(rt[0])
        newgjf = fl.split('.')[0]+'_rstrt.gjf'
    elif 'td' in rtstr:
        link = writelink(lk,'add')
        route = writetd(rt[0])
        newgjf = fl.split('.')[0]+'_add.gjf'
    else:
        raise SystemExit('\'<_\' This job cannot be restarted!\n     Only OPT can be restart and TDDFT can be added more states if previous one finished!')
    with open(newgjf,'w') as fo:
        fo.writelines(link)
        fo.write(route)
    print('**\(^O^)/** Please check new gjf file: %s and do:\n~/Hyak-Gaussian/gaussian-sub.py %s; sbatch %s.sh' % (newgjf,newgjf,newgjf[:-4]))

def writelink(oldlk,s):
    newlk=[]
    for l in oldlk:
        if l.lower().startswith('%chk'):
            tl = re.split(r'=|\.',l)
            newlk.append('%oldchk'+l[4:])
            newlk.append('%chk='+tl[1]+'_'+s+'.chk\n')
        else:
            newlk.append(l)
    return newlk

def writeopt(optrt):
    newrt = []
    for r in optrt.split():
        if r.lower()=='opt':
            newrt.append('Opt=Restart')
        else:
            newrt.append(r)
    return ' '.join(newrt)+'\n\n'

def writetd(tdrt):
    newrt = []
    for r in tdrt.split():
        if r.lower().startswith('td'):
            try:
                n = int(input('? How many states do you want to add: '))
            except:
                raise SystemExit('\'<_\'Invalid Input!')
            newrt.append('td(add='+str(n)+')')
            newrt.append('Geom=AllCheck')
        elif r.lower().startswith('geom'):
            continue
        else:
            newrt.append(r)
    return ' '.join(newrt)+'\n\n'

if __name__=='__main__':
    gjf = checkcommand()
    restart(gjf) 
