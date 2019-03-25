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
	- extract Cp from all \*\_freq.csv files got from freq_thermal.py in the working directory

## ExtractStdOrient.py

- Usage:
	- python ExtractStdOrient.py inputfile N
- Descriptions:
	- extract a particular standard orientation from inputfile (i.e. log file)
	- N can not be 0; N=1: 1st orientation; N=-1: the last orientation; N=-2: the 2nd to last, ...
- Details:
	- use 'Standard orientation' to locate positions of all standard orientations
	- '--------' is used to locate coordinates
	- the 1st '#' after 'Standard orientation' to find charge and multiplicity; -1,-1 will be used if not found
	- output file will be named based on input file, and its suffix is gjf if more com files exist than gjf files; vice versa.

## GibbsEnergy.py

- Usage:
	- python GibbsEnergy.py energyfile
- Descriptions:
	- energyfile is got from HFenergies.py; also need \*\_freq.csv from freq_thermal.py
	- calcualte the relative gibbs energy for every structure listed in the energyfile
- Details:
	- energyfile: 2 columns with comma as the delimiter: 1st column is structure name, and 2nd column is the HF energy
	- if the structure is named with 'x', its thermal file named with 'x_freq.csv' must exist in the workding directory
	- use the minimum energy as a reference to calcualte relative Gibbs free energy
	
## HFenergies.py

- Usage:
	- python HFenergies.py
- Descriptions:
	- extract HFenerngy (the last SCF Done) from all log files in the working directory
	- if structrure not optimizaed (not found 'Stationary point found'), return 'NA'
	
## SCFextractor.py

- Usage:
	- python SCFextractor.py N
- Descriptions:
	- extract the particular SCF energy from all log files in the working directory
	- N cannot be zero; N=1: the 1st SCF energy; N=-1: the last SCF energy; N=-2: the 2nd SCF energy from the bottom

## action_spectra.py

- Usage:
	- python action_spectra.py
- Description:
	- action input file must be named with "ExportedData.csv"
	- one or more powerscan input files named with "PS*.CSV"
	- the above two kinds of files are used as taken from the MS experiment without any changes
	- calcualte the average intensities of each fragment to total ions (fragment ions + parent ion) and corrected by relative powerscan energies
- Details:
	- if the 1st wavelength is larger than the 2nd, it will be removed
	- if the scans of the 1st/last wavelength is larger than the default, only count the last/1st possible scans
	- the default-scan is calcualted by the mode of all scans
	- the last ion is considered as the parent ion
	
## comp2files.py

- Usage:
	- python comp2files.py file1 file2
- Descriptions:
 	- compare two files same or not and print the different lines
	
## cubegen.py

- Usage:
	- python cubegen.py tddftlog N_state
- Descriptions:
	- N_state is the number of the excited state
	- generate all cubegen files for all orbitals of the N_state: wirte them into a task file and submit it to hyak-ckpt using parallel-run
- Details:
	- need tddft log file, chk/fchk file in the working directory
	- if fchk not found, "formchk" will be written into the sbatch file
	- log file is used to find the name of chk file, orbitals to calcualted, and the number of alpha electrons and virtual alpha electrons
	- how to calcualte beta electrons: mo(beta) += mo(NAE)+mo(NVA)
	
## dat2tsv.py

- Usage:
	- python dat2tsv.py datafile
- Descriptions:
	- change the delimiter from space or multispaces to '\t' and written to a new file
	
## extract_pm6opt.py

- Usage:
	- python extract_pm6opt.py
- Descriptions:
	- read optimized.xyz in all subdirectories whose name starts with 'd', change their format from xyz to gaussian input and extract energies from these xyz files
	- all new files are written to a new directory optresult
	- the name of the structures and the gaussian input files depends on these subdirectories – test if dtest

## freq_thermal.py

- Usage:
	- python freq_thermal.py freq.log
- Descriptions:
	- calculate the enthalpy, entropy and corrected zero-point energy for frequency-log file
- Details:
	- The temperature is set to 310.0K, normal modes is corrected by a scaler 0.975
	- calculated process and final data are written into \*\_freq.csv file
	- If the first frequency is negative, it will print a warning and stop processing data

## gaussian-mox.py

- Usage:
    - python gaussian-mox.py input-file partition node-num time-in-hour
- Descriptions:
    - create gaussian submitting bash file on Hyak-mox 

## generateLogName.py

- Usage:
	- python generateLogName.py name_prefix name_suffix num_start num_end
- Descriptions:
	- generate a list of name and written to an outpuf file
	- e.g. prefix5.suffix - prefix9.suffix if "python generateLogName.py prefix suffix 5 9"

## get_action.py

- Usage:
	- python get_action.py outfile
- Descriptions:
	- an old version to calculate action spectra same to action_spectra.py
	
## gjfcom2xyz.py

- Usage:
	- python gjfcom2xyz.py inputfile
- Descriptions:
	- write the gaussian input file to xyz format
- Details:
	- the line containing two integers is seen as charge and multiplicity
	- all lines containing 4 elements are taken as molecular coordinates: valid delimiter: space, spaces or comma

## gscratch_space.py

- Usage:
	- python gscratch_space.py
- Descriptions:
	- print the first line of usage_report.txt in several partition: [stf chem ilahie scrubbed]
	- usage_report.txt contains the info about diskspace-usage on Hyak
	
## mergeOPTlog.py

- Usage:
	- python mergeOPTlog.py main_log attach_log
- Descriptions:
	- merge two optimization log files based on their step numbers
- Details:
	- if main_log is 'xyzabcd.log' and attach_log is 'xyzcda.log', the merge_log has the name of 'xyzmerge.log'
	- if 'Stationart point found' is in the log file, a reminder will be printed out on the screen
	- this script and 'generateLogName.py' may be useful if run gaussian opt with 'opt=restart'
	
## newtonx.py

- Usage:
	- python newtonx.py opt.gjf\/com freq.log
- Descriptions:
	- write all requried folders and files for running newtonx: [more details](http://yueliu.wang/2018/12/30/Newton-X-on-Hyak/)
	- NPoints=300, ANH_F=0.975: easy to change in the head of the script

## note8email.py

- Usage:
	- python note8email.py sh-file
	- python note8email.py sh-file job-name
- Descriptions:
	- turn on email notification for bash job running on Hyak: it only works for UW email
- Details:
	- write '#SBATCH --mail-type=ALL' and '#SBATCH --mail-user='+emal-address before the first blank line if these two words are not found in the file
	- job-name can be changed if choose the second usage

## nxplot.py

- Usage:
	- python nxplot.py
- Descriptions:
	- use it to handle newtonx output files in INITIAL_CONDITIONS folder when newtonx jobs finish
- Details:
	- first check if all I\* finish
	- merge all I\* folder into I_merged
	- create cross-section.dat by $NX\/nxinp
	- extract wavelength within 0-1200nm from cross-section.dat to cross-section.tsv and plot it if in python3 environment
	
## optlog2gjfcom.py

- Usage:
	- python optlog2gjfcom.py optlogfile
- Descriptions:
	- if optimization finishes, extract optimized coordinates and charge and multiplicty from it
	- if not finishes, write the restarted gaussian input file
- Details:
	- 'Stationary point found' is used to tell if optimization completes
	- see more details: [click me](http://yueliu.wang/2018/12/16/Gaussian-on-Hyak/#hfenergies)
	
## pm6bomd_parallel.py

- Usage:
	- python pm6bomd_parallel.py
- Descriptions:
	- create input files for every xyz file in the working directory to run BOMD with MOPAC package
	- move each xyz file into a new subdirectory (dxyz) and create corresponding yaml file
	- tasklist and bash file are generated in the working directory to submit it to Hyak with parallel-run

## pm6opt_parallel.py

- Usage:
	- python pm6opt_parallel.py
- Descriptions:
	- create input files for every xyz file in the working directory to run pm6 opt with MOPAC  package

## prlsql_pm6opt.py

- Usage:
	- python prlsql_pm6opt.py
- Descriptions:
	- Similiar to pm6opt_parallel.py but using parallel_sql environment, another parallel run of Huak

## prlsql_pm6traj.py

- Usage:
	- python prlsql_pm6traj.py
- Descriptions:
	- Similair to pm6bpmd_parallel.py but using parallel_sql environment

## restart_gaussian.py

- Usage:
    - python restart_gaussian.py oldgjf
- Descriptions:
    - create a new gjf file used to restart gaussian optimization or add more states for gaussian tddft jobs
    - chk file required for the above two jobs

## tddft_lorentzian.py

- Usage:
	- python tddft_lorentzian.py tddft.log
		- count all excitations > 0 nm
	- python tddft_lorentzian.py tddft.log N
		- N=200.0 means count excitations > 200.0nm
- Descriptions:
	- check if the last excitation exceed 210nm (START, set in the head of the script)
		- if not: write a new gaussian input file with 'TD(ADD=xx)'
		- if yes: procee data
	- count excitations whose SS2 < 2.6 (MAXSS2, set in the head of the script)
	- use lorentzian function to calcualate absorption spectra from 200-1100nm (WaveNumbers)
	
## tddft_plot.py

- Usage:
	- python tddft_plot.py csv_file (got from tddft_lorentzian.py)
- Descriptions:
	- need python3 environment to plot absortion spectra with black line and exctations strength with dark red vertical lines
	- load anaconda3_5.3 on Hyak
	
## traj2xyz.py

- Usage:
	- python traj2xyz.py N
- Descriptions:
	- for all child directories in the working directory, it will find trajectory_anneal.xyz file to extract the 1st struct for every N structures.
	- if N=100 and it has 20,000 cycles in the trajectory_anneal.xyz, you will get 20,000/100=200 structures

## xyz2gjf.py

- Usage:
	- python xyz2gjf.py xyzfile
- Descriptions:
	- write xyz file to gaussian input file
	- default route, charge and multiplicity can be easily edited on the head of the script