#!/usr/bin/env python

'''
Usage: python tdnx_plot.py td_csv cross-section.dat
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
FigSize=(10,6)
TickSize,LabelSize=18,20

def checkcommand():
    if len(sys.argv)!=3:
        raise SystemExit('Usage: python tdnx_plot.py td_uvvis.csv nx_cross-section.dat')
    td = sys.argv[1]
    nx = sys.argv[2]
    if os.path.isfile(td):
        if os.path.isfile(nx):
             return td,nx
        raise SystemExit('%s Not Found!' % nx)
    raise SystemExit('%s Not Found!' % td)

def nx_plot(fnx):
    df = pd.read_csv(fnx,delim_whitespace=True)
    df = df[df['lambda/nm']>0]

    x = df['lambda/nm'].values
    dceil = (df['sigma/A^2']+df['+/-error/A^2']).values
    dbottom = (df['sigma/A^2']-df['+/-error/A^2']).values

    plt.fill_between(x,dbottom, dceil,facecolor='cyan')
    plt.plot(x,df['sigma/A^2'],color='b')

def td_plot(ftd):
    nm = ftd.split('.')[0]
    data = pd.read_csv(ftd,index_col=False)

    plt.figure(figsize=FigSize)
    ax=plt.gca()
    #plot
    plt.plot(data['Wavelength(nm)'].values,data['Spectrum'].values,color='Black')
    plt.vlines(data['MaxPeak(nm).1'].values,[0],data['intensity.1'].values,color='DarkRed')
    # plot format
    plt.xlim((Xmin,Xmax))
    Ymax = ax.yaxis.get_ticklocs()[-1]
    plt.ylim((0,Ymax))
    plt.xticks(np.arange(Xmin,Xmax+1,Xmajor),fontsize=TickSize)
    plt.yticks(fontsize=TickSize)
    ax.xaxis.set_minor_locator(mtloc(Xminor))
    plt.xlabel('$\lambda$ (nm)',fontsize=LabelSize)
    plt.ylabel('Oscillator Strength',fontsize=LabelSize)
    #figure subtitle at upper right corner
    nmparts = [x for x in nm.split('_') if x!='opt' and x!='add' and x!='uvvis']
    structnm = '_'.join(nmparts)
    plt.text(Xmax-10,Ymax*0.95,structnm,fontsize=LabelSize,verticalalignment="top",horizontalalignment="right")
    return structnm

def tdnx_plot(ftd,fnx):
    try:
        nm = td_plot(ftd)
        nx_plot(fnx)
        plt.savefig(nm+'_tdnx.jpg')
        print('**\(^O^)/** Please check %s_tdnx.jpg!' % nm)
    except BaseException as err:
        print(err)
        raise SystemExit(':::>_<::: Error!')

if __name__=='__main__':
    td,nx = checkcommand()
    tdnx_plot(td,nx)
   

    
