#!/usr/bin/env python

'''
Usage: python action_plot *xlsx
Descriptions:
- input file should be in xlsx format with a tile on the 1st row, wavelength on the 1st columns and sum of all fragments on the last column
- plot the sum fragments first 
- fragments whose maximum intensity larger than 10% (defined by SCALOR) of maximum of sum fragments wil be plotted later
'''
try:
    import os,sys
    import pandas as pd
    import numpy as np
    import matplotlib as mpl
    mpl.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.ticker import MultipleLocator as mtloc
except ImportError as err:
    print(err)
    raise SystemExit('Error: Must python3!')

Xmin,Xmax,Xmajor,Xminor=200,700,50,10
FigSize=(10,4)#(10,6) 
TickSize,LabelSize=18,20
MARKER= ['+','x','*','^',',','1','2','3','4']
SCALOR = 0.1

def checkcommand():
    if len(sys.argv)!=2:
        raise SystemExit('Usage: python action_plot.py *.xlsx')
    else:
        fl = sys.argv[1]
        if fl.split('.')[1]!='xlsx':
            raise SystemExit('Error: file must in xlsx format!')
        elif os.path.isfile(fl):
            return fl
        else:
            raise SystemExit('Error: %s Not Found!' % fl)

def plot(fl):
    try:
        df = pd.read_excel(fl)
        dtitle = df.columns.values.tolist()
        x = df[dtitle[0]].values
        y = df[dtitle[-1]].values
        plt.figure(figsize=FigSize)
        ax=plt.gca()
        plt.scatter(x,y,label='sum',marker='o',c='',edgecolors='k')

        i = 0
        for ion in dtitle[1:-1]:
            if max(df[ion].values)<SCALOR*max(y):
                break
            try:
                m = MARKER[i]
            except:
                i = 0
                m = MARKER[i]
            plt.scatter(x,df[ion].values,label=ion,marker=m)
            i += 1
        #plot format
        plt.xlim((Xmin,Xmax))
        Ymax = ax.yaxis.get_ticklocs()[-1]
        plt.ylim((0,Ymax))
        plt.xticks(np.arange(Xmin,Xmax+1,Xmajor),fontsize=TickSize)
        plt.yticks(fontsize=TickSize)
        ax.xaxis.set_minor_locator(mtloc(Xminor))
        ax.set_xlabel('$\lambda$ (nm)',fontsize=LabelSize)
        plt.ylabel('Relative Intensity',fontsize=LabelSize)
        leg = plt.legend(loc='best',fontsize=LabelSize)
        leg.get_frame().set_linewidth(0.0)
        figname = fl.split('.')[0]+'.jpg'
        plt.savefig(figname)
        print('**\(^O^)/** Please check %s!' % figname)
    except:
        err = sys.exc_info()
        print('python error in line: %s' % err[2].tb_lineno)
        print(err[1])
        raise SystemExit(':::>_<:::Fail to Plot %s!' % fl)

if __name__=='__main__':
    fxls = checkcommand()
    plot(fxls)

