#!/usr/bin/env python

#AUTHOR: Yue Liu
#EMAIL: yueliu96@uw.edu
#Created on 11/18/2018
#Edited on 12/06/2018

from __future__ import print_function
import sys,os,math,csv
from functools import reduce

MAXSS2 = 2.6
KEY = ' Excited State '
HWHM = 10
SCALER = 1
WaveNumbers = range(200,1101)
START = 210 #nm
END = 700 #nm

def checkcommand(n):
    if n!=2 and n!=3:
        raise SystemExit('Usage:\n    python tddft_lorentzian.py tddft.log\nOR  python tddft_lorentzian.py tddft.log N\n(N=210 means count excitations > 210nm, otherwise N=0 for default)')
    else:
        inpfile = sys.argv[1]
        if inpfile[-4:].lower()!='.log':
            raise SystemExit('\nThe suffix of %s must be log!\n' % inpfile)
        if os.path.isfile(inpfile):
            try:
                calstart = float(sys.argv[2])
            except:
                calstart= 0
            return inpfile,inpfile[:-4]+'_uvvis.csv',calstart
        else:
            raise SystemExit('\n%s File Not Found\n' % inpfile)
 
def tddft(logfile,outfile,calcst):
    keylines = readlogfile(logfile)
    allpeaks = list(map(readpeaks,keylines))
    allpeaks = [list(x) for x in allpeaks]#type(x)=tuple
#check if it covers 210nm
    if allpeaks[-1][0]>START:
        print('Warning'.center(60,'-'),'\n%s doesn\'t reach %snm' % (logfile,START))
        print('the last three excitations in the log [freq,f,S^2]:\n%s\n%s\n%s' % (allpeaks[-3],allpeaks[-2],allpeaks[-1]))
        print('-'*60)
        addstates(logfile[:-4])
        try:
            float(input('? Do you still want to calculate spectrum using the current tddft log---[any number:yes],[any string or enter:no]: '))
        except:
            raise SystemExit('\'<_\' Ended Normally......')
#count peaks as long as S**2<2.6
    realpeaks = [x for x in allpeaks if x[2]<MAXSS2 and x[0]>calcst]
#anoher way: count peaks in 700-210nm and S***2<2.6; then choose to keep or delete peaks out of range:
    '''
    realpeaks = [x for x in allpeaks if x[2]<MAXSS2 and START<=x[0]<=END]
    extrapeaks = [x for x in allpeaks if x[2]<MAXSS2 and (x[0]<START or x[0]>END)]
    if bool(extrapeaks):
        realpeaks = addpeaks(realpeaks,extrapeaks)
    '''
    spectrum=[]
    for wn in WaveNumbers:
        intensities = list(map(lorentzian,realpeaks,[wn]*len(realpeaks)))
        spectrum.append(reduce(mysum,intensities))
    max_spec = max(spectrum)
    T = [x/max_spec for x in spectrum]
    Absorbance = []
    for x in spectrum:
        if x<1:
            Absorbance.append(-math.log10(1-x))
        else:
            Absorbance.append('infinite')
    spectra = [[WaveNumbers[i],spectrum[i],T[i],Absorbance[i]] for i in range(len(spectrum))]
    outcome = chformat(allpeaks,realpeaks,spectra)
    with open(outfile,'w') as fo:
        wrfo = csv.writer(fo,delimiter=',')
        wrfo.writerows(outcome)
    print('**\(^O^)/**Finish spectra calculation successfully. Please check your output: %s!' % outfile)
     
def readlogfile(name):
    with open(name,'r') as fo:
        lines = fo.readlines()
    outlines = [line for line in lines if line.startswith(KEY)]
    if bool(outlines):
        return outlines
    else:
        print(':::>_<:::TDDFT Job Not Finished!')
        raise SystemExit('The last 5 lines in %s:\n%s%s%s%s%s' % (name,lines[-5],lines[-4],lines[-3],lines[-2],lines[-1]))

def readpeaks(s):
    ss = s.split()
    peak = float((ss[6]))*SCALER
    f = float(ss[-2].split('=')[1])
    s22 = float(ss[-1].split('=')[1])
    return peak,f,s22

def addpeaks(real,extra):
    red=[]
    print('Find Another %d Peaks out of the range %d-%dnm(press any numbers to delete, enter or any strings to keep):' % (len(extra),START,END))
    print('FYI: If multiplicity=2, spin**2=0.75. Super bad one=3.75. Here cut off at %s' % MAXSS2)
    print('%9s%10s%9s'% ('peak(nm)','intensity','spin**2:'))
    for x in extra:
        try:
            a = float(input('%8.2f%9.4f%9.3f   ---[enter:keep],[number:delete]---your choice: ' % (x[0],x[1],x[2])))
            continue
        except KeyboardInterrupt:
            raise SystemExit('\n~(T^T)~ KeyboardInterrupt!')
        except:
            if x[0]<START:
                real.append(x)
            elif x[0]>END:
                red.append(x)
    if bool(red):
        red.extend(real)
        return red
    else:
        return real

def lorentzian(x,wn):
    return x[1]/(1+pow((wn-x[0])/HWHM,2))
    
def mysum(m,n):
    return m+n

def myextend(x,y):
    if len(x)>len(y):
        for i in range(len(y)):
            x[i].append('')
            x[i].extend(y[i])
        return x
    else:
        for i in range(len(x)):
            y[i].append('')
            y[i].extend(x[i])
        return y
    
def chformat(allpeaks,realpeaks,result):
    title1 = ['Wavelength(nm)','Spectrum','T=Spec/maxSpec','Absorbance=-1og10(1-Spec)']
    title2 = ['MaxPeak(nm)','intensity','all S**2']
    title3 = ['MaxPeak(nm)','intensity','S**2<'+str(MAXSS2)]
    result.insert(0,title1)
    allpeaks.insert(0,title2)
    realpeaks.insert(0,title3)
    finalresult = myextend(result,myextend(allpeaks,realpeaks))
    return finalresult

def addstates(fl):
    suffix = '.gjf'
    gjf=fl+suffix
    print('\'<_\' start to write new gaussian input file for adding more states to calculate...')
    if not os.path.isfile(gjf):
        suffix = '.com'
        gjf = fl+suffix
        if not os.path.isfile(gjf):
            print(':::>_<::: %s.gjf/com Not Found! Couldn\'t write restarted input file!' % fl)
            return
    with open(gjf,'r') as fo:
        lines = fo.readlines()
    lk = [l for l in lines if l.startswith('%') and not l.lower().startswith('%lindaworker') and not l.lower().startswith('%oldchk')]
    rt = [l for l in lines if l.startswith('#')]
    if not bool(lk) or not bool(rt) or 'td' not in rt[0].lower():
        print(':::>_<:::%s format not correct! Couldn\'t write restarted input file!' % gjf)
        return
    link = writelink(lk)
    route = writeroute(rt[0])
    newgjf = fl+'_add'+suffix
    with open(newgjf,'w') as fo:
        fo.writelines(link)
        fo.writelines(route)
    print('\'<_\' Finish writing gjf file. Please check:', newgjf)
    print('Next Step:\n ~/Hyak-Gaussian/gaussian-sub.py %s\n sbatch %s.sh' % (newgjf,newgjf[:-4]))

def writelink(oldlk):
    newlk=[]
    for l in oldlk:
        if l.lower().startswith('%chk'):
            tl = l.strip().split('=')
            ttll = tl[1].split('.')#considering that %chk=mychk same as %chk=mychk.chk
            newlk.append('%oldchk='+ttll[0]+'.chk\n')
            newlk.append('%chk='+ttll[0]+'_add.chk\n')
        else:
            newlk.append(l)
    if not os.path.isfile(ttll[0]+'.chk'):
        print('Warning'.center(60,'-'))
        print('you should have %s.chk file to continue tddft job!' % ttll[0])
        print('-'*60)
    return newlk

def writeroute(oldrt):
    newrt = []
    for r in oldrt.split():
        if r.lower().startswith('td'):
            try:
                n = int(input('? How many states do you want to add: '))
            except:
                raise SystemExit(':::>_<:::Invalid Input!')
            newrt.append('td(add='+str(n)+')')
            newrt.append('Geom=AllCheck')
        elif r.lower().startswith('geom'):
            continue
        else:
            newrt.append(r)
    return ' '.join(newrt)+'\n\n'
    
if __name__=='__main__':
    log,out,calcst = checkcommand(len(sys.argv))
    tddft(log,out,calcst) 
