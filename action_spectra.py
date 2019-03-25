#!/usr/bin/env python

'''
 Author: Yue Liu
 Usage: python action_spectra.py
 Description:
 - action input file must be named with "ExportedData.csv"
 - powerscan files must be started with "PS" and ended with "CSV", e.g. "PS10030432.CSV"
 - output file is the relative intensities of each fragment to total ions(fragements + parent ions) and corrected by relative power scan energies
'''

import csv,time,glob

ACT = 'ExportedData.csv'
PSE = 'PS*.CSV'
OUT = 'OUT'+time.strftime('%m%d%H%M%S',time.localtime(time.time()))+'.csv'

def mymode(s):
    unq_s = list(set(s))
    n = [s.count(unq_s[i]) for i in range(len(unq_s))]
    index_unq = n.index(max(n))
    return unq_s[index_unq]

def action():
    with open(ACT,'r') as fa:
        rfa = csv.reader(fa)
        data = [row for row in rfa]
    ions = [x[6:] for x in data[0][5:] if bool(x)]
    print('Reminder: Find Ions m/z: %s, the last one is taken as the parent ion' % ions)
    n_ions = len(ions)
# find first positions of all wavelengths in data
    x_wl = data[1][1]
    wl = [float(x_wl)]
    mark_row=[1]
    for p_row, row in enumerate(data[1:]):
        if row[1]!= x_wl:
            mark_row.append(p_row+1)
            x_wl = row[1]
            wl.append(float(x_wl))
    mark_row.append(len(data))
# tell if the wavelength is in ascending order. sometimes the first wavelength is not reasonable
    if wl[0]>wl[1]:
        wl.pop(0)
        mark_row.pop(0)
    scans = [mark_row[i+1]-mark_row[i] for i in range(len(mark_row)-1)]
# check scan-number of every wavelength based on the mode of all scans; count the last 100 scans for the 1st wavelength or the first 100 scans for the last wavelength if the default scan number is 100 and more than 100 scans found for these two wavelength
    scan = mymode(scans)
    for i_x, x in enumerate(scans):
        if x > scan:
            if i_x == 0:
                mark_row[i_x] = mark_row[i_x+1]-scan
            elif i_x == len(scans)-1:
                mark_row[i_x+1] = mark_row[i_x]+scan
            print('Reminder: %s scans found for %snm, count %s-%sth lines (%s scans)' % (x,data[mark_row[i_x]][1],mark_row[i_x]+1,mark_row[i_x+1],scan))
        elif x < scan:
            print('Warning: only find %s scans for %snm!' % (x,data[mark_row[i_x]][1]))
# calculate the average intensities of all monitored charged substances at every wavelength; (wavelength, ion1, ion2, ..., ionN,total-ions)
    ave_action=[]
    totions = []
    for i,mark in enumerate(mark_row[0:-1]):
        tmp = []
        for j in range(5,5+n_ions):
            s = 0
            for t_data in data[mark:mark_row[i+1]]:
                s += float(t_data[j])
            tmp.append(s/(mark_row[i+1]-mark))
        totions.append(sum(tmp))
        ave_action.append(tmp)
    return ions,wl,ave_action,totions

def PSenergy(wl):
    energy=[]
    fps = glob.glob(PSE)
    if bool(fps):
        print('Reminder: PS files are %s' % fps)
    else:
        raise SystemExit('Error: PowerScan Files (PS*.CSV) Not Found!')
    for f in fps:
        with open(f,'r') as fo:
            readfo = csv.reader(fo)
            rows = [line for line in readfo]
        column1 = [float(x[0]) for x in rows]
        if column1 != wl:
            raise SystemExit('Error: %s(%s-%snm) Not Match Wavelength in %s(%s-%snm)' % (f,column1[0],column1[-1],ACT,wl[0],wl[-1]))
        column2 = [float(x[1]) for x in rows]
        energy.append(column2)
    n_ps = len(energy)
    n_wl = len(wl)
    ave_ps = [0]*n_wl
    for i in range(n_wl):
        for j in range(n_ps):
            ave_ps[i] += energy[j][i]
        ave_ps[i] /= n_ps
    maxps = max(ave_ps)
    return [x/maxps for x in ave_ps]
    
def wrout(ps,ave_ions,tot,wl,ions):
    mI = []
    for i in range(len(wl)):
        tI=[x/tot[i]/ps[i] for x in ave_ions[i]]
        tI.pop(-1)
        tI_tot=sum(tI)
        tI.append(tI_tot)
        tI.insert(0,wl[i])
        mI.append(tI)
    title=['m/z '+x for x in ions[0:-1]]
    title.append('all fragments')
    title.insert(0,'wavelength(nm)')
    with open(OUT,'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(title)
        writer.writerows(mI)

def main_script():
    try:
        ions,wl,ave_int,tot_int = action()
        mod_ps = PSenergy(wl)
        wrout(mod_ps,ave_int,tot_int,wl,ions)
        print('**\\(^O^)/**Please Check %s: relative intensities to total ions and corrected by laser power!' % OUT)
    except IOError:
        raise SystemExit('%s Not Found!' % ACT)

if __name__=='__main__':
    main_script()
