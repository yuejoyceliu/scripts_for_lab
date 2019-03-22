#!/usr/bin/env python

'''
 Author: Yue Liu
 Created: 01202019
Usage: python tddft_plot.py csv_file(got from tddft_lorentzian.py)
Python Evironment: python 3
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
    if len(sys.argv)!=2:
        raise SystemExit('Usage: python tddft_plot.py uvvis.csv')
    else:
        fl = sys.argv[1]
        if fl.split('.')[1]!='csv':
            raise SystemExit('Error: file must in csv format!')
        elif os.path.isfile(fl):
            return fl
        else:
            raise SystemExit('Error: %s Not Found!' % fl)

def plot(fl):
    try:
        nm = fl.split('.')[0]
        data = pd.read_csv(fl,index_col=False)
        specdf = data.loc[:,['Wavelength(nm)','Spectrum']] #[data['Wavelength(nm)']>=210]
        procdf = data.loc[:,['MaxPeak(nm).1','intensity.1']] #[data['MaxPeak(nm).1']>=210]
        plt.figure(figsize=FigSize)
        ax=plt.gca()
    #plot    
        plt.plot(specdf['Wavelength(nm)'],specdf['Spectrum'],color='Black')
        plt.vlines(procdf['MaxPeak(nm).1'],[0],procdf['intensity.1'],color='DarkRed')
    # plot format
        plt.xlim((Xmin,Xmax))
        Ymax = ax.yaxis.get_ticklocs()[-1]
        plt.ylim((0,Ymax))
        plt.xticks(np.arange(Xmin,Xmax+1,Xmajor),fontsize=TickSize)
        plt.yticks(fontsize=TickSize)
        ax.xaxis.set_minor_locator(mtloc(Xminor))
        ax.set_xlabel('$\lambda$ (nm)',fontsize=LabelSize)
        plt.ylabel('Oscillator Strength',fontsize=LabelSize)
    #figure subtitle at upper right corner    
        nmparts = [x for x in nm.split('_') if x!='opt' and x!='add' and x!='uvvis']
        structnm = '_'.join(nmparts)
        plt.text(Xmax-10,Ymax*0.95,structnm,fontsize=LabelSize,verticalalignment="top",horizontalalignment="right")
        plt.savefig(nm+'.jpg')
        print('**\(^O^)/** Please check %s' % nm+'.jpg')
    except:
        err=sys.exc_info()
        print('python error in line: %s' % err[2].tb_lineno)
        print(err[1]) 
        raise SystemExit(':::>_<:::Fail to Plot %s!' % fl)

if __name__=='__main__':
    specfl = checkcommand()
    plot(specfl)
   
