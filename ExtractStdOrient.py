#!/usr/bin/env python

'''
 AUTHOR: Yue Liu
 EMAIL: yueliu96@uw.edu
 Created on 11/26/2018
 Edited on 03/23/2019
Usage:
 python ExtractStdOrient.py inputfile N (N=1: 1st standard orientation, N=-1: the last standard orientation)
Description:
 - extract the  coordinate (key: $XYZ1,$XYZ2) and find charge and mutiplicity from the last paragragh (key: the 1st $STOP after last $XYZ1). If most suffixes are gjf, it will be named as com; vice versa.
 - N is an integer in -1,1,2,3,..., and N should not larger than the number of standard orientations in the input file!
'''

import sys,os,glob

LINK='%UseSSH\n%mem=100GB\n%nprocshared=28\n'
ROUTE='# td(NStates=50) um062x/6-31+g(d,p) pop=none scf=(xqc,tight)'
CHK='%chk='
XYZ1='Standard orientation:'
XYZ2=' --------------'
STOP = '#'
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

def checkcommand(n):
    if n!=3:
        raise SystemExit('\n python ExtractStdOrient.py input-file number (1:1st orientation; -1: last orientation)\n')
    else:
        return sys.argv[1],sys.argv[2]

def getvalues(s,n):
#split a string s by space and return the first n numbers, but type is still string
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
        raise SystemExit(':::>_<:::No Values Found in %s\n Warning: Delimiter Must be space or spaces' % ls)
    if n==1:
        return values[0]
    else:
        return values

def findcoords(lines,fl,N):
#'Standard orientation' as the 1st key because every run generates one 'Standard orienctation'.
#'---------' as the 2nd key. There are three these dash lines. Coords are in btw the second and the third dash lines.
    strt=['na']
    for i in range(len(lines)):
        line = lines[i]
        if XYZ1 in line:
            strt.append(i)
    try:
        newlines = lines[strt[N]:]
    except:
        raise SystemExit(':::>_<:::Found %s Standart Orientations, %s Specified' % (len(strt)-1,N))
    numl=[]
    for j in range(len(newlines)):
        line = newlines[j]
        if line.startswith(XYZ2):
            numl.append(j)
            if len(numl)==3:
                 break
    coords = []
    for lss in newlines[numl[1]+1:numl[2]]:
        v_xyz = getvalues(lss,6)
        xyz = '%-4s%16s%16s%16s' % (PTCE[int(v_xyz[1])],v_xyz[3],v_xyz[4],v_xyz[5])
        coords.append(xyz+'\n')
    return strt[-1],coords
  
def findchgmp(lss):
#find the charge and multiplicity from 1st '#' after find opt coord; if not found,  use -1 -1 be default
    key='key'
    for i in range(len(lss)):
        line=lss[i]
        if STOP in line:
            key = i
            break
    if isinstance(key,str):
        print(':::>_<:::Couldn\'t find charge and multiplicity. Use -1 -1 by default')
        return -1,-1
    
    if len(lss[key:])>50:
        newlss = lss[key:key+50]
    else:
        newlss = lss[key:]
    tmpt = [s.lstrip().strip('\n') for s in newlss]
    tmpt = ''.join(tmpt)
    tmpt = tmpt.split('\\')
    for t in tmpt:
        ts = t.split(',')
        if len(ts)==2:
            try:
                return int(ts[0]),int(ts[1])
            except:
                continue
    print(':::>_<:::Couldn\'t find charge and multiplicity. Use -1 -1 by default.You could change 50 in findchgmp function to a larger number to fix it.')
    return -1,-1
        
def Extract_xyz(log,N):
    mo = log.split('.')[0]
    with open(log,'r') as fo:
        ctts = fo.readlines()
    num_line,mospecify = findcoords(ctts,log,N)
    charge,mtplicity = findchgmp(ctts[num_line:])
    allgjf = glob.glob('*.gjf')
    allcom = glob.glob('*.com')
    if len(allgjf)>=len(allcom):
        out = mo+'_opt.com'
    else:
        out = mo+'_opt.gjf'
    print('  Default: %s' % ROUTE)
    with open(out,'w') as fo:
        fo.write(LINK)
        fo.write(CHK+mo+'.chk'+'\n')
        fo.write(ROUTE+'\n')
        fo.write('\n')
        fo.write('Complex '+mo+'\n')
        fo.write('\n')
        fo.write(str(charge)+' '+str(mtplicity)+'\n')
        fo.writelines(mospecify)
        fo.write('\n')
    print('**\(^O^)/**Please check your optimized structure: %s\n' % out)

if __name__=='__main__':
    fl,n = checkcommand(len(sys.argv))
    try:
        n = int(n)
        if n==0:
            raise SystemExit(':::>_<::: Input couldn\'t be zero!')
        Extract_xyz(fl,n)
    except IOError:
        raise SystemExit(':::>_<:::%s Not Found!' % fl)
    except ValueError:
        raise SystemExit(':::>_<:::\"%s\" is supposed to be an integer!' % n)
