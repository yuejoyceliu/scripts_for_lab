#!/usr/bin/env python

#AUTHOR: Yue Liu
#EMAIL: yueliu96@uw.edu
#Wirte on 11/23/2018
#Edit on 11/26/2018

import sys,os

KEY=' Step number'
FINISH = 'Stationary point found'

def checkcommand(n):
    if n!=3:
        raise SystemExit('\npython mergeOPTlog.py mainlog attachlog\n')
    else:
        m = sys.argv[1]
        a = sys.argv[2]
        if os.path.isfile(m) and os.path.isfile(a):
            return m,a
        else:
            raise SystemExit('\n%s Not Found!\n' % [x for x in sys.argv[1:] if not os.path.isfile(x)])

def getvalue(s):
#split string s into several strings by space and find the first one could be a number.
#Here is to find the step number in one long string
    ls = s.split()
    num = list(map(str,range(0,10)))
    for x in ls:
        if x[0] in num:
            return int(x)

def FindSteps(f,n):
#find the last(if n=-1) or the first(if n=1) step number and its corresponding line number in f file.
    with open(f,'r') as fo:
        lines = fo.readlines()
    steps = [x for x in lines if x[:len(KEY)]==KEY]
    for line in lines:
        if FINISH in line:
            print(':::Reminder:::%s: optimization finish!' % f)
    if not bool(steps):
        raise SystemExit(':::>_<:::%s doesn\'t have useful information!' % f)
    num_steps = list(map(getvalue,steps))
    if len(steps)==num_steps[-1]-num_steps[0]+1:
        print('  Find %d steps in %s: step No.%02d----No.%02d' % (len(steps),f,num_steps[0],num_steps[-1]))
    else:
        mistep=[mis for mis in list(range(num_steps[0],num_steps[-1])) if mis not in num_steps]
        print('  Find %d steps in %s: step No.%02d----No.%02d, except %s' % (len(steps),f,num_steps[0],num_steps[-1],mistep))
    if n==-1:
        keystep = steps[-1]
        keyn = num_steps[-1]
    elif n==1:
        keystep = steps[0]
        keyn = num_steps[0]
    for i in range(len(lines)):
        if lines[i]==keystep:
            return keyn,i

def outname(s1,s2):
#return the name of output file, should be the same part of name s1 and s2 plus 'merge.log'
    s=''
    for i in range(min(len(s1),len(s2))):
        if s1[i]==s2[i]:
            s += s1[i]
        else:
            break
    s = s+'merge.log'
    return s

def merge(mfile,afile):
    mlast,mline = FindSteps(mfile,-1)
    afirst,aline = FindSteps(afile,1)
    check='anything'
    try:
        if mlast!=afirst:
            print(':::>_<:::%s & %s are not suitable to be merged!' % (mfile,afile))
            check=input('[Force Them Together press 1] or [others to exit]: ')
        if mlast==afirst or str(check)=='1':
            outfile = outname(mfile,afile)
            with open(mfile,'r') as fm:
                mcontents = fm.readlines()
            m_keep = mcontents[:mline]
            with open(afile,'r') as fa:
                acontents = fa.readlines()
            a_keep = acontents[aline:]
            with open(outfile,'w') as fo:
                fo.writelines(m_keep)
                fo.writelines(a_keep)
            print('**\(^O^)/**%s & %s are merged to %s!\n' % (mfile,afile,outfile))
    except:
         raise SystemExit(':::>_<:::Fail To Merge!\n')
    


if __name__=='__main__':
    mainfile,appendfile=checkcommand(len(sys.argv))
    merge(mainfile,appendfile)
