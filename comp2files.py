#!/usr/bin/env python

#---AUTHOR: YUE LIU
#---EMAIL: yueliu96@uw.edu

import csv,sys,os

def checkcommand(n):
    if n!=3:
        raise SystemExit('python comp2files.py file1 file2')
    else:
        m = sys.argv[1]
        n = sys.argv[2]
        boolm = os.path.isfile(m)
        booln = os.path.isfile(n)
        if boolm and booln:
            return m,n
        elif not boolm and not booln:
            raise SystemExit('%s and %s Files Not Found!' % (m,n))
        elif not boolm:
            raise SystemExit('%s File Not Found!' % m)
        else:
            raise SystemExit('%s File Not Found!' % n)

def readfile(s):
    with open(s,'r') as fo:
        reader = csv.reader(fo)
        rows = [row for row in reader]
    return rows

def comp2files(file1,file2):
    out1 = readfile(file1)
    out2 = readfile(file2)
    if out1 == out2:
        print('**\(^O^)/**%s and %s are same!' % (file1,file2))
    else:
        print(':::>_<:::%s and %s are different!' % (file1,file2))
    
if __name__=='__main__':
    file1,file2 = checkcommand(len(sys.argv))
    comp2files(file1,file2)
