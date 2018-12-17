#!/usr/bin/env python

'''
 AUTHOR: Yue Liu
 EMAIL: yueliu96@uw.edu
 Created: 12/16/2018
Usage: python nxplot.py
run this script 'python nxplot.py' in INITIAL_CONDITIONS directory
First, it will check if I* finished. If all finished,it will first merge all I* files together to give you I_merged file. All important data are in final_optput.1.* file, which contains transition information from state 1 to state *
Second, it goes to I_merged directory, to generate cross-section.dat by $NX/nxinp to calculate absorption spectra
Third, extract wavelength within 0-1200nm from cross-section.dat to cross-section.tsv. tsv fill only contains the second and third column information of dat file; tsv can be opened by excel
If in python3, it will plot cross-section.tsv to cross-section.png
'''
import os,glob,shutil,sys,subprocess
import time

def checkfinish(fd):
    fl = fd+'/initcond.log'
    try:
        with open(fl,'r') as fo:
            ctts = fo.read()
        if 'NEWTON-X ends here' in ctts:
            return True
        else:
            print(' Warning: %s Not Finished!' % fd)
            return False
    except:
        print(' Warning: %s Not Finished!' % fd)
        return False

def nx_merge(n):
    with open('temptno','w') as fo:
        fo.write(str(n))
    sdo1 = 'module load contrib/newtonX; $NX/merge_initcond.pl < temptno'
    p = subprocess.Popen(sdo1,stdout=subprocess.PIPE,shell=True)
    print('Number of directories to be merged: %d\n\n\tPlease wait a little bit...' % n)
    a = p.wait()
    os.remove('temptno')
    if a!=0:
        raise SystemExit(':::>_<:::Fail to merge jobs to I_merged!')

def nx_spec():
    nstates = len(glob.glob('I_merged/final_output.1.*'))+1
    with open('I_merged/temptinp','w') as fo:
        fo.write('5\n1\n1\n2-'+str(nstates)+'\nF\n0\n-1\nlocal\n0\nlorentz\n0.1\n310\n1\n0.005\n3\n7\n')
    sdo2 = 'cd I_merged; module load contrib/newtonX; $NX/nxinp < temptinp'
    p = subprocess.Popen(sdo2, shell=True)
    a = p.wait()
    os.remove('I_merged/temptinp')
    if a!=0:
        raise SystemExit(':::>_<:::Fail to process spectra data!')
 
def dat2tsv():
    with open('I_merged/cross-section.dat','r') as fo:
        lines = fo.readlines()
    with open('I_merged/cross-section.tsv','w') as fo:
        title = lines[0].split()
        fo.write(title[1]+'\t'+title[2]+'\n')
        x,y = [],[]
        for line in lines[1:]:
            lss = line.split()
            if 0<float(lss[1])<1200:
                x.append(float(lss[1]))
                y.append(float(lss[2]))
                fo.write(lss[1]+'\t'+lss[2]+'\n')
    return x,y

def myplot(X,Y):
        import matplotlib as mpl
        mpl.use('Agg')
        import matplotlib.pyplot as plt
        plt.figure()
        plt.xlabel('wavelength(nm)')
        plt.ylabel('cross-section')
        plt.plot(X,Y)
        plt.savefig('I_merged/cross-section.png')

if __name__=='__main__':
    if os.path.exists('I_merged'):
        print('I_merged  exists and will be removed...')
        shutil.rmtree('I_merged')
    allI = glob.glob('I*')
    n = len(allI)
    if n==0:
        raise SystemExit(':::>_<::: I* subfolder Not Found!')
    print('\'<_\' %d jobs found! Start to check if they finish...' % n)
    chk = []
    for I in allI:
        chk.append(checkfinish(I))
    if False in chk:
        raise SystemExit(':::>_<:::')
    else:
        print('\'<_\' Finish checking, all finished...')
    nx_merge(n)
    nx_spec()
    x,y = dat2tsv()
    print('**\(^O^)/**Please check your I_merged/cross-section.tsv!\n\
\t   It only contains wavelength less than 1200nm and the last wavelength is %5.2fnm\n\t   The full data file is I_merged/cross-section.dat' % x[-1]) 
    if 1/2!=0:#in python2 1/2=0, python3: 1/2=0.5
        myplot(x,y)
        print('\t   Also I_merged/cross-section.png')


    #err=sys.exc_info()
    #print('python error in line: %s' % err[2].tb_lineno )
    #raise SystemExit(err[1])
