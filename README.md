# scripts_for_lab

## CheckSCFEnergy.py

- Usage:
 - python CheckSCFEnergy.py
- Descriptions:
 - extract 'Step number', 'Predicted change' and 'SCF Done' from all log files in the working directory

## CpExtractor.py

- Usage:
 - python CpExtractor.py
- Descriptions:
 - extract Cp from all \*\_freq.csv files got from freq_lorentzian.py in the working directory

## ExtractStdOrient.py

- Usage:
 - python ExtractStdOrient.py inputfile N
 - N $\neq$ 0; N=1: 1st orientation; N=-1: the last orientation; N=-2: the 2nd to last, ...
- Descriptions:
 - extract a particular standard orientation from inputfile (i.e. log file)
- Details:
 - use 'Standard orientation' to locate positions of all standard orientations
 - '--------' is used to locate coordinates
 - the 1st '#' after 'Standard orientation' to find charge and multiplicity; -1,-1 will be used if not found
 - output file will be named based on input file, and its suffix is gjf if more com files exist than gjf files; vice versa.
 

## GibbsEnergy.py

- Usage:
 - python GibbsEnergy.py energyfile
 - energyfile is got from HFenergy.py
 
