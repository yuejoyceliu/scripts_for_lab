#!/usr/bin/env python

'''
 AUTHOR: Yue Liu
 EMAIL: yueliu96@uw.edu
 Created: 12/16/2018
Usage: python nxplot.py
run this script 'python nxplot.py' in INITIAL_CONDITIONS directory
First, it will check if I* finished. If all finished,it will first merge all I* files together to give you I_merged file. All important data are in final_optput.1.* file, which contains transition information from state 1 to state *
Second, it goes to I_merged directory, to generate cross-section.dat by $NX/nxinp to calculate absorption spectra
'''
import os,glob,shutil,sys,subprocess
import time

def checkfinish(fd):
    fl = fd+'/initcond.log'
    try:
        n_cond = 0
        with open(fl,'r') as fo:
           ctts = fo.readlines()
        for line in ctts:
            if 'Done' in line:
                n_cond += 1
            elif 'NEWTON-X ends here' in line:
                return True,n_cond
        print(' Warning: %s Not Finished!' % fd)
        return False,n_cond
    except:
        print(' Warning: %s/initcond.log Not Found!' % fd)
        return False,n_cond

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
        fo.write('5\n1\n1\n2-'+str(nstates)+'\nF\n0\n-1\nlocal\n1\nlorentz\n0.1\n310\n1\n0.005\n3\n7\n')
    sdo2 = 'cd I_merged; module load contrib/newtonX; $NX/nxinp < temptinp'
    p = subprocess.Popen(sdo2, shell=True)
    a = p.wait()
    os.remove('I_merged/temptinp')
    if a!=0:
        raise SystemExit(':::>_<:::Fail to process spectra data!')

def nxplot():
    try:
        if os.path.exists('I_merged'):
            print('I_merged  exists and will be removed...')
            shutil.rmtree('I_merged')
        allI = glob.glob('I*')
        n = len(allI)
        if n==0:
            raise SystemExit(':::>_<::: I* subfolder Not Found!')
        print('\'<_\' %d jobs found! Start to check if they finish...' % n)
        chk = []
        n_cond = 0
        allI.sort(key=lambda x: (len(x),x))
        for I in allI:
            t_chk,t_n = checkfinish(I)
            chk.append(t_chk)
            n_cond += t_n
        print('\'<_\' Finish checking! %s initial conditions found!' % n_cond)
        if False in chk:
            print('\n\'<_\':   enter <any number>: continue to process data\n\tenter <A-Z> or <ENTER>: stop processing data')
            try:
                float(input())
            except:
                raise SystemExit('Quit Normally!')
        nx_merge(n)
        nx_spec()
        with open('I_merged/cross-section.dat') as fo:
            lines = fo.readlines()
        x = float(lines[-1].split()[1])
        print('**\(^O^)/**Please check your I_merged/cross-section.dat!\n\t   The last wavelength is %5.2fnm\n' % x) 
    except:
        err=sys.exc_info()
        print('python error in line: %s' % err[2].tb_lineno )
        raise SystemExit(err[1])

if __name__=='__main__':
    nxplot()
