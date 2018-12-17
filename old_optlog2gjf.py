#!/usr/bin/env python

#AUTHOR: Yue Liu
#EMAIL: yueliu96@uw.edu
#Created on 11/26/2018
#Edited on 12/03/2018

import sys,os

MEM='%mem=32GB'
NProc='%nprocshared=28'
CHK='%chk='
ROUTE='pop=min scf=(xqc,tight)'
KEY1='    -- Stationary point found.'
KEY2='Standard orientation:'
KEY3=' --------------'
CHARGE=' Charge'
KEY4='\\@'
SPIN2='S2='
HF='HF='
PTCE = {1 : 'H', 2 : 'He', 3 : 'Li', 4 : 'Be', 5 : 'B', \
6  : 'C', 7  : 'N', 8  : 'O',  9 : 'F', 10 : 'Ne', \
11 : 'Na' , 12 : 'Mg' , 13 : 'Al' , 14 : 'Si' , 15 : 'P', \
16 : 'S'  , 17 : 'Cl' , 18 : 'Ar' , 19 : 'K'  , 20 : 'Ca', \
21 : 'Sc' , 22 : 'Ti' , 23 : 'V'  , 24 : 'Cr' , 25 : 'Mn', \
26 : 'Fe' , 27 : 'Co' , 28 : 'Ni' , 29 : 'Cu' , 30 : 'Zn', \
31 : 'Ga' , 32 : 'Ge' , 33 : 'As' , 34 : 'Se' , 35 : 'Br', \
36 : 'Kr' , 37 : 'Rb' , 38 : 'Sr' , 39 : 'Y'  , 40 : 'Zr', \
41 : 'Nb' , 42 : 'Mo' , 43 : 'Tc' , 44 : 'Ru' , 45 : 'Rh', \
46 : 'Pd' , 47 : 'Ag' , 48 : 'Cd' , 49 : 'In' , 50 : 'Sn', \
51 : 'Sb' , 52 : 'Te' , 53 : 'I'  , 54 : 'Xe' , 55 : 'Cs', \
56 : 'Ba' , 57 : 'La' , 58 : 'Ce' , 59 : 'Pr' , 60 : 'Nd', \
61 : 'Pm' , 62 : 'Sm' , 63 : 'Eu' , 64 : 'Gd' , 65 : 'Tb', \
66 : 'Dy' , 67 : 'Ho' , 68 : 'Er' , 69 : 'Tm' , 70 : 'Yb', \
71 : 'Lu' , 72 : 'Hf' , 73 : 'Ta' , 74 : 'W'  , 75 : 'Re', \
76 : 'Os' , 77 : 'Ir' , 78 : 'Pt' , 79 : 'Au' , 80 : 'Hg', \
81 : 'Tl' , 82 : 'Pb' , 83 : 'Bi' , 84 : 'Po' , 85 : 'At', \
86 : 'Rn' , 87 : 'Fr' , 88 : 'Ra' , 89 : 'Ac' , 90 : 'Th', \
91 : 'Pa' , 92 : 'U'  , 93 : 'Np' , 94 : 'Pu' , 95 : 'Am', \
96 : 'Cm' , 97 : 'Bk' , 98 : 'Cf' , 99 : 'Es' ,100 : 'Fm', \
101: 'Md' ,102 : 'No' ,103 : 'Lr' ,104 : 'Rf' ,105 : 'Db', \
106: 'Sg' ,107 : 'Bh' ,108 : 'Hs' ,109 : 'Mt' ,110 : 'Ds', \
111: 'Rg' ,112 : 'Uub',113 : 'Uut',114 : 'Uuq',115 : 'Uup',\
116: 'Uuh',117 : 'Uus',118 : 'Uuo'}
Form={1:'# ',2:'#P ',3:'#T '}
JobType={1:'opt ',2:'freq ',3:'td(NStates='}
Method={1:'b3lyp/',2:'wb97xd/',3:'m062x/',4:'ub3lyp/',5:'uwb97xd/',6:'um062x/'}
BasisSet={1:'6-31g(d,p) ',2:'6-31+g(d,p) '}

def checkcommand(n):
    if n!=2:
        raise SystemExit('\n python optlog2gjf logfile\n')
    else:
        log = sys.argv[1]
        if log[-4:]!='.log':
            raise SystemExit(':::>_<::: The suffix of %s must be log' % log)
        elif os.path.isfile(log):
            return log,log[:-4]
        else:
            raise SystemExit('\n%s Not Found!\n' % log)

def readlog(fl):
    check=0
    with open(fl,'r') as fo:
        lines = fo.readlines()
    for i in range(len(lines)):
        line = lines[i]
        if line[:len(KEY1)]==KEY1:
            check=1
        if check==1:
            if line.lstrip()[:len(KEY2)]==KEY2:
                keyline=i
                check=2
    if check==2:
        return lines[keyline:]
    else:
        print('\'<_\' Optimiazation not finish. Start to write restarted gjf file...')
        restartopt(fl[:,-3]+'gjf')
        raise SystemExit('\'<_\'Ended Normally...')

def restartopt(gjf):
    if not os.path.isfile(gjf):
        raise SystemExit(':::>_<:::%s Not Found! Cannot write restarted gjf file...' % gjf)
    with open(gjf,'r') as fo:
        lines = fo.writelines()
    lk = [l for l in lines if l.startswith('%') and not l.lower().startswith('%lindaworker') and not l.lower().startswith('%oldchk')]
    rt = [l for l in lines if l.startswith('#')]
    if not bool(lk) or not bool(rt):
        raise SystemExit(':::>_<:::No link section or/and route section found! Fail to write restarted gjf file...')
    if 'opt' in rt[0].lower():
        link = writelink(lk)
        route = writeroute(rt[0])
        newgjf = gjf[:-4]+'_rstrt.gjf'
    else:
        raise SystemExit(':::>_<:::Cannot locate opt in the route section! Fail to write restarted gjf file...')
    with open(newgjf,'w') as fo:
        fo.writelines(link)
        fo.write(route)
    print('^_^ Please check your new gjf file: %s. And do:' % newgjf)
    print(' ~/Hyak-Gaussian/gaussain-sub.py %s\n sbatch %s.sh' % (newgjf,newgjf[:-4]))

def writelink(oldlk):
    newlk=[]
    for l in oldlk:
        if l.lower().startswith('%chk'):
            tl = l.split('=')
            ttll = tl[1].split('.')
            newlk.append('%oldchk='+tl[1])
            newlk.append('%chk='+ttll[0]+'_add.chk\n')
        else:
            newlk.append(l)
    if not os.path.isfile(tl[1].strip()):
        print('Warning'.center(60,'-'),'\nyou should have %s file to continue tddft job!' % tl[1].strip())
    return newlk

def writeroute(optrt):
    newrt = []
    for r in optrt.split():
        if r.lower()=='opt':
            newrt.append('Opt=Restart')
        else:
            newrt.append(r)
    return ' '.join(newrt)+'\n\n'

def findkeylines(lss):
    numlines=[]
    for i in range(len(lss)):
        line = lss[i]
        if line[:len(KEY3)]==KEY3:
            numlines.append(i)
        elif line[:len(CHARGE)]==CHARGE:
            chg = int(float(getvalues(line,1)))
        elif KEY4 in line:
            tmpt = [tl.lstrip().strip('\n') for tl in lss[i-20:i+1]]
            tmpt = ''.join(tmpt)
            if HF in tmpt:
                 hf = findxinbtw(tmpt,HF,'\\')
            if SPIN2 in tmpt:
                spin2 = findxinbtw(tmpt,SPIN2,'\\')
                spin = (-1+pow(1+4*spin2,0.5))/2.0
                mp = int(round(2*spin+1))
            else:
                print('Warning:set multiplicity as 1!')
                mp = 1
    xyzstrt = numlines[1]+1
    xyzend = numlines[2]
    xyzlines = lss[xyzstrt:xyzend]
    return xyzlines,chg,mp,hf

def findxinbtw(s,m,n):
    mpos = s.find(m)
    s = s[mpos:]
    npos =s.find(n)
    x = s[len(m):npos]
    return float(x)
    
def getvalues(s,n):
    i = 0
    values = []
    ls = s.split()
    nums = list(map(str,range(0,10)))
    nums.append('-')
    for x in ls:
        if i>=n:
            break
        elif x[0] in nums:
            values.append(x)
            i += 1
    if not bool(values):
        raise SystemExit('No Values Found!')
    if n==1:
        return values[0]
    else:
        return values

def getcoords(xyzlines):
    coords = []
    for lss in xyzlines:
        v_xyz = getvalues(lss,6)
        xyz = '%2s%16s%16s%16s' % (PTCE[int(v_xyz[1])],v_xyz[3],v_xyz[4],v_xyz[5])
        coords.append(xyz+'\n')
    return coords

def RouteTitle(chg,mp):
    if chg==2 and mp==1:
        t='Dication '
    elif chg==1 and mp==2:
        t='CatRad '
    else:
        t='Complex'
    try:
        ws='-'*80
        print(ws+'\n Write route section(# lines):\n press [corresponding number to continue],[any other key to use the default one]\n'+ws)
        a1 = int(input('print form for later log file: [normal--1],[addtional output--2],[terse output--3]\nYour Choice: '))
        form = Form[a1]
        a2 = int(input('job type: [opt--1],[freq--2],[td--3]\nYour Choice: '))
        jt = JobType[a2]
        if a2==3:
            a22=int(input('How many states do you want to calculate? Please type a number: '))
            jt = jt+str(a22)+') '  
        a3 = int(input('method: [b3lyp--1],[wb97xd--2],[m062x--3],[ub3lyp--4],[uwb97xd--5],[um062x--6]\nYour Choice: '))
        mthd = Method[a3]
        if mp>1 and a3<4:
            print('WARNING'.center(20,'#')+'\nUsually choose unrestricted method if multiplicity doesn\'t equal one!\n'+'#'*20)
        a4 = int(input('basis function: [6-31g(d,p)--1],[6-31+g(d,p)--2]\nYour Choice: '))
        bf = BasisSet[a4]
        rt = form+jt+mthd+bf+ROUTE
    except (KeyError,SyntaxError,ValueError,NameError):
        print('Route=\'# opt wb97xd/6-31+g(d,p) pop=min scf=(xqc,tight)\' by default.')
        return '# opt wb97xd/6-31+g(d,p) '+ROUTE,t
    except KeyboardInterrupt:
        raise SystemExit('\n:::>_<:::Please Try Again!')
    return rt,t

def optlog2gjf(log,mo):
    ctts = readlog(log)
    [xyzl,charge,mtplicity,Ehf] = findkeylines(ctts)
    mospecify = getcoords(xyzl)
    out = mo+'_opt.gjf'
    route,title = RouteTitle(charge,mtplicity)
    with open(out,'w') as fo:
        fo.write(MEM+'\n')
        fo.write(NProc+'\n')
        fo.write(CHK+mo+'.chk'+'\n')
        fo.write(route+'\n')
        fo.write('\n')
        fo.write(title+mo+' '+str(Ehf)+'Hartrees\n')
        fo.write('\n')
        fo.write(str(charge)+' '+str(mtplicity)+'\n')
        fo.writelines(mospecify)
        fo.write('\n')
    print('**\(^O^)/**Please check your gjffile %s!' % out)

if __name__=='__main__':
    logfl,moname = checkcommand(len(sys.argv))
    optlog2gjf(logfl,moname)

