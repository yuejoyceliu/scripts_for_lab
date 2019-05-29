#!/usr/bin/env python

'''
Usage: python tdnx_plot.py td_csv cross-section.dat num
       num is where to start coat the excitation states
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
    if len(sys.argv)!=3 and len(sys.argv)!=4:
        raise SystemExit('Usage: python tdnx_plot.py td_uvvis.csv nx_cross-section.dat num\n\tnum: lowest wavenumer contributing to newtonx,default=200')
    td = sys.argv[1]
    nx = sys.argv[2]
    try:
        n = float(sys.argv[3])
    except:
        n = 200
    if os.path.isfile(td):
        if os.path.isfile(nx):
             return td,nx,n
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

def td_plot(ftd,nxcut=200):
    nm = ftd.split('.')[0]
    data = pd.read_csv(ftd,index_col=False)

    plt.figure(figsize=FigSize)
    ax=plt.gca()
    #plot
    plt.plot(data['Wavelength(nm)'].values,data['Spectrum'].values,color='Black')
    plt.vlines(data['MaxPeak(nm).1'].values,[0],data['intensity.1'].values,color='DarkRed')
    #coat excitation lines for newtonx with aqua color
    nxdata = data[data['MaxPeak(nm).1']>nxcut]
    plt.vlines(nxdata['MaxPeak(nm).1'].values,[0],nxdata['intensity.1'].values,color='aqua')
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

def tdnx_plot(ftd,fnx,n):
    try:
        nm = td_plot(ftd,n)
        nx_plot(fnx)
        plt.savefig(nm+'_tdnx.jpg')
        print('**\(^O^)/** Please check %s_tdnx.jpg!' % nm)
    except BaseException as err:
        print(err)
        raise SystemExit(':::>_<::: Error!')

if __name__=='__main__':
    td,nx,n = checkcommand()
    tdnx_plot(td,nx,n)
   

    
