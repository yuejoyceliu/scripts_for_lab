#!/usr/bin/env python

#AUTHOR: Yue Liu
#EMAIL:  yueliu96@uw.edu

import sys,os,csv
from functools import reduce

SCANS = 100
ACTION = 'ExportedData.csv'
KEY = 'User Value 1, User Value 2, User Value 3, User Value 4, SprayCurrent'

def str2int(s):
    return int(float(s))

def str2float(s):
    return float(s)

def mysum(x,y):
    return x+y

def checkcommand(n):
    if n!=2:
        raise SystemExit('\npython get_action.py outputfile\n')
    else:
        return sys.argv[1]

def findaction(fa,fcvs):
    check = 1
    if os.path.isfile(fa):
        print('Action File Found: %s' % fa)
        check = int(input('satisfied please press 1, otherwise press other number: '))
    if not os.path.isfile(fa) or check!=1:
        fa = ''
        for f in fcvs:
            with open(f,'r') as fo:
                line = fo.readline() 
            if line[:68]== KEY:
                check = int(input('Is %s your action file? 1 for yes, other number for no: ' % f))
                if check==1:
                    fa=f
                    break
        if not bool(fa):
            raise SystemExit('\nAction File Not Found!\n\
Reminder: action file should be named with \'ExportedData.csv\', or at least filename suffix is \'.csv\'\n')
    return fa

def readaction(fa):
    with open(fa,'r') as fo:
        readfo = csv.reader(fo)
        rows = [row for row in readfo]
    wl = list(map(str2int,[row[1] for row in rows[1:]]))
    wl.insert(0,'wavelength(nm)')
    m2z = [ion[6:] for ion in rows[0][5:] if bool(ion)]
    n = len(m2z)
    for i in range(1,len(rows)):
        rows[i][5:5+n] = list(map(str2float,rows[i][5:5+n]))
    return rows,wl,m2z
          
def findpsfile(fcvs):
    psfiles = [s for s in fcvs if s[:2].lower()=='ps']
    n = len(psfiles)
    check = 1
    if 1<=n<=3:
        print('%d PowerScan File(s) Found: %s' % (n,psfiles))
        check = int(input('satisfied press 1, otherwise press any other number: '))
    if n==0 or n>3 or check!=1:
        psfiles = []
        for f in fcvs:
            with open(f,'r') as fo:
                readfo = csv.reader(fo)
                line = [s for s in readfo if readfo.line_num==1]
            if len(line[0])==2:
                psfiles.append(f)
                n += 1
        if bool(psfiles):
            print('###CHECK###PowerScan Files Found: %s' % psfiles)
            check = input('press 1 to continue, 2 to pick, any other number to exit: ')
            if int(check)==2:
                f_select = []
                for s in psfiles:
                    select = input('%s---1 for yes,other for no: ' % s)
                    if int(select)==1:
                        f_select.append(s)
                psfiles = f_select
        if not bool(psfiles) or (int(check)!=1 and int(check)!=2):
            raise SystemExit('\nPowerScan Files Not Found!\n\
Reminder: powerscan filename should be \'PS*.CSV\', or at least suffix is \'.csv\'.\n\
Usually we should have 3 ps files, but this script also works for 1 or 2 ps files.\n')
    return psfiles

def readpsfile(psname):
    with open(psname,'r') as fo:
        readfo = csv.reader(fo)
        column1= list(map(str2int,[row[0] for row in readfo]))
    with open(psname,'r') as fo:
        readfo = csv.reader(fo)              
        column2=list(map(str2float,[row[1] for row in readfo]))
    return column1,column2

def calcpower(ps):
    n = len(ps)
    result = list(map(readpsfile,ps))
    wl = result[0][0]
    for rt in result:
        if rt[0] != wl:
            raise SystemExit('\nPowerScan Files Contain Different Wavelength Regions!\n')
    if n==3:
        psvalues = [(result[0][1][i]+result[1][1][i]+result[2][1][i])/3 for i in range(len(wl))]
    elif n==2:
        psvalues = [(result[0][1][i]+result[1][1][i])/2 for i in range(len(wl))]
    else:
        psvalues = result[0][1]
    return wl,psvalues

def actionstart(wl,start):
    i = 0
    while i<len(wl):
        if wl[i]!=start:
            i = i+1
        else:
            break
    return i

def ave_action(i,n,rows,wl_ps,wl_action):
    result = []
    start = wl_ps[0]
    end = wl_ps[-1]
    for stdwl in wl_ps:
        j = i
        for wl in wl_action[i:]:
            if wl==stdwl:
                j += 1
            else:
                break
        count = j-i
        if stdwl==start and count>100:
            print('Reminder: %s nm has %s scans, and only take the last %s!' % (start,count,SCANS))
            i,count = j-SCANS,SCANS
        elif stdwl==end and count>100:
            print('Reminder: %s nm has %s scans, and only take the first %s!' % (end,count,SCANS))
            j,count = i+SCANS,SCANS
        elif count!=SCANS:
            print('Warning: %s nm has %s scans, which should be %s!' % (stdwl,count,SCANS))
        temp = []
        for k in range(n):
            temp.append(reduce(mysum,[row[5+k] for row in rows[i:j]])/count)
        result.append(temp)
        i = j
    return result
    
def rel_intensity(I,wl,psvalues):
    maxps = max(psvalues)
    for i in range(len(wl)):
       tot = reduce(mysum,I[i])
       rel_energy =  psvalues[i]/maxps
       frag2tot = [frag/tot/rel_energy for frag in I[i][:-1]]
       allfrags2tot = reduce(mysum,frag2tot)
       frag2parent = [frag/I[i][-1]/rel_energy for frag in I[i][:-1]]
       allfrags2parent = reduce(mysum,frag2parent)
       I[i].insert(0,wl[i])
       I[i].extend([tot,'',psvalues[i],rel_energy,''])
       I[i].extend(frag2tot)
       I[i].extend([allfrags2tot,''])
       I[i].extend(frag2parent)
       I[i].append(allfrags2parent)
    return I

def writetitle(m2z):
    title_ions = ['m/z '+ion for ion in m2z]
    title_ions.insert(0,'WaveLength(nm)')
    title = title_ions
    title.extend(['Total Ions','','Average PS','Rel Energy',''])
    title.extend([frag+' to tot' for frag in m2z[:-1]])
    title.extend(['All Fragments',''])
    title.extend([frag+' to '+m2z[-1] for frag in m2z[:-1]])
    title.append('All Fragements')
    return title

def action(outfile):
    allcsv = [f for f in os.listdir('.') if os.path.isfile(f) and f[-4:].lower()=='.csv']
    f_action = findaction(ACTION,allcsv)
    rows,WLaction,m2z_ions = readaction(f_action) 
    n_ions = len(m2z_ions)
    f_powerscan = findpsfile(allcsv)
    wavelength,psvalues = calcpower(f_powerscan)
    icheck = actionstart(WLaction,wavelength[0])
    ave_result = ave_action(icheck,n_ions,rows,wavelength,WLaction)
    outcome = rel_intensity(ave_result,wavelength,psvalues)    
    title = writetitle(m2z_ions)
    with open(outfile,'w') as fo:
        wrfo = csv.writer(fo)
        wrfo.writerow(title)
        wrfo.writerows(outcome)
    print('---Congratulations!---')
    print('Finish action calculation. Please check your output: %s!' % outfile )

if __name__=='__main__':
    outfile = checkcommand(len(sys.argv))
    action(outfile)
