#!/usr/bin/env python

#AUTHOR: Yue Liu
#EMAIL: yueliu96@uw.edu
#Created: 11/20/2018
#Edited: 12/03/2018

from __future__ import print_function
import sys,os,csv,math

DOF = 'Deg. of freedom'
NAtoms = 'NAtoms='
AMU = 'Molecular mass:'
T_CALC = 'Temperature'
ZPVE = 'Zero-point vibrational energy'
THERMAL = 'E (Thermal)'
FREQ = 'Frequencies'

SCALER = 0.975
FREQ2T = 1.4387687 #cm*K
T_REAL = 310.0 #K
C = 2.99792458*1e10 #cm/s
H = 6.6260755*1e-34 #J*s
NA = 6.0221367*1e23 #/mol
J2KJ = 1e-3 #kJ/J
R = 8.314510 #J/K/mol
CAL2J = 4.184 #J/cal

def checkcommand(n):
    if n!=2:
        raise SystemExit('\npython freq_thermal.py freq.log\n')
    else:
        if os.path.isfile(sys.argv[1]):
            return sys.argv[1]
        else:
            raise SystemExit(':::>_<:::%s Not Found!' % sys.argv[1])

def getvalues(s,n):
#get the first n positive values in the string s
    i = 0
    values = []
    ls = s.split()
    num = list(map(str,range(0,10)))
    for x in ls:
        if i>=n:
            break
        elif x[0] in num:
            values.append(float(x))
            i += 1
    if len(values)==1:
        return values[0]
    else:
        return values

def readlogfile(log):
    with open(log,'r') as fo:
        lines = fo.readlines()
    frequencies=[]
    ifreq,dof = 0,'?'
    try:
        for i in range(len(lines)):
            line = lines[i].lstrip()
            if line[:len(DOF)]==DOF:
                dof = getvalues(line,1)
            elif line[:len(NAtoms)]==NAtoms:
                natoms = getvalues(line,1)
            elif line[:len(AMU)]==AMU:
                amu = getvalues(line,1)
            elif line[:len(T_CALC)]==T_CALC: 
                #Temperature(Kelvin),Pressure(atm):
                t,p = getvalues(line,2)
            elif line[:len(ZPVE)]==ZPVE:
                #ZPVE(Joules/Mol)
                zpve = getvalues(line,1)
            elif line[:len(THERMAL)]==THERMAL:
                #S(Cal/Mol-Kelvin)
                S_elec = getvalues(lines[i+3],3)[-1]
                S_trans = getvalues(lines[i+4],3)[-1]
                S_rot = getvalues(lines[i+5],3)[-1]
            elif line[:len(FREQ)]==FREQ:
                #freq(cm^-1)
                ifreq += 1
                freq3 = getvalues(line,3)
                if ifreq==1 and len(freq3)!=3:
                    raise SystemExit(':::>_<:::Frequency Starts With A Negative Value')
                frequencies.extend(freq3)
        readinfo = [natoms,dof,amu,t,p,zpve,S_elec,S_trans,S_rot]
    except:
        err=sys.exc_info()
        print('python error in line %d: ' % err[2].tb_lineno)
        print(err[1])
        raise SystemExit(':::>_<:::%s Not Finished! FYI: %d out of %s frequencies found' % (log,len(frequencies),dof))
    return readinfo,frequencies


def pttfunc(f):
    #using partition function to calculate vibS & vibH
    ptt = []
    num = 1
    for x in f: 
        corrf = x*SCALER
        f2T = corrf*FREQ2T/T_REAL
        y = f2T/(math.exp(f2T)-1)
        z = math.log(1-math.exp(-f2T))
        s = y-z
        ptt.append([num,x,corrf,f2T,y,z,s])
        num += 1
    return ptt

def mysum(numbers):
    summ = 0
    for i in numbers:
        summ += i
    return summ

def thermodynamics(log):
    info,freq = readlogfile(log)
    vib_contrib = pttfunc(freq)
    f_zpve = 0.5*C*H*NA*J2KJ*mysum(freq)
    corrf_zpve = 0.5*C*H*NA*J2KJ*mysum([v[2] for v in vib_contrib])
    enthalpy = (mysum([v[4] for v in vib_contrib])+4)*R*T_REAL*J2KJ
    enthalpy_rovib = (mysum([v[4] for v in vib_contrib])+1.5)*R*T_REAL*J2KJ
    freerotor = [[v[0],v[4]] for v in vib_contrib if v[4]<0.5]
    enthalpy_freerotor = (mysum([v[1] for v in freerotor])+(freerotor[0][0]-1)/2.0+4)*R*T_REAL*J2KJ
    entropy_elec = info[-3]*CAL2J
    entropy_trans  = info[-2]*CAL2J+2.5*R*math.log(T_REAL/info[3])
    entropy_rot = info[-1]*CAL2J+1.5*R*math.log(T_REAL/info[3])
    entropy_vib = R*mysum([v[6] for v in vib_contrib])
    entropy = entropy_elec+entropy_trans+entropy_rot+entropy_vib
    t1,t2=vib_contrib[0][4],vib_contrib[0][3]
    Cv = (3+mysum([pow(v[4],2)*math.exp(v[3]) for v in vib_contrib]))*R
    Cp = Cv+R
   
    out = log[:-4]+'_freq.csv' 
    with open(out,'w') as fo:
        wrfo = csv.writer(fo)
        wrfo.writerow(['ReadFrom:',log])        
        wrfo.writerow(['NAtoms','dof_vib','molar mass','T(K)','pressure(atm)','ZPVE(J/mol)','S_elec(cal/mol/K)','S_trans(cal/mol/K)','S_rot(cal/mol/K)'])
        wrfo.writerow(info)
        wrfo.writerow(['CalcVibFreq:'])
        wrfo.writerow(['T(K)','ZVPE(kJ/mol)','corrZVPE(kJ/mol)','H_rotvib(kJ/mol)','H_tot(kJ/mol)','H_freerotor_tot(kJ/mol)',\
'S_elec(J/mol/K)','S_trans(J/mol/K)','S_rot(J/mol/K)','S_vib(J/mol/K)','S_tot(J/mol/K)','Cv(J/mol/K)','Cp(J/mol/K)'])
        wrfo.writerow([T_REAL,f_zpve,corrf_zpve,enthalpy_rovib,enthalpy,enthalpy_freerotor,entropy_elec,entropy_trans,entropy_rot,entropy_vib,entropy,Cv,Cp])
        wrfo.writerow(['Important:'])
        wrfo.writerow(['corrZPVE(kJ/mol)','H_tot(kJ/mol)','S_tot(J/mol/K)','H_freerotor_tot(kJ/mol)'])
        wrfo.writerow([corrf_zpve,enthalpy,entropy,enthalpy_freerotor])
        wrfo.writerow([''])
        wrfo.writerow(['H=(4+sum(y))*RT','Svib=sum(z)*R','S=Selec+Strans+Srot+Svib','Cv=(3+sum(y^2*e^x))*R','Cp=Cv+R'])
        wrfo.writerow([''])
        wrfo.writerow(['','v(cm-1)','0.975v','x=0.975vinK/T','y=x/(e^x-1)','z=ln(1-e^(-x))','s=y-z'])
        wrfo.writerows(vib_contrib) 

    print('**\(^O^)/**Please check your output file %s!' % out)


if __name__=='__main__':
    logfile = checkcommand(len(sys.argv))
    thermodynamics(logfile)
