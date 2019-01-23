#!/usr/bin/env python

PTT = ['stf','chem','ilahie','scrubbed']
try:
    print('%-10s%-12s%-12s%-12s%-12s%-15s%-16s' % ('Name','Use(GB)','Quota(GB)','Limit(GB)','Files','FilesQuota','FilesLimit'))
    for p in PTT:
        f = '/gscratch/'+p+'/usage_report.txt'
        with open(f,'r') as fo:
            lines = fo.readlines()
        s = lines[2].split()
        print('%-10s%-12s%-12s%-12s%-12s%-15s%-16s' % (s[0],s[2],s[3],s[4],s[6],s[7],s[8]))
except BaseException as err:
    print(err)
