# gtseqMAF
Python program for calculating minor allele frequency (MAF) both globally and by population

## Dependencies
- python3
- pandas
- matplotlib

## Installation
One option for installation is the setup of a conda environment. This can be accomplished by first installing [Miniconda](https://docs.conda.io/en/latest/miniconda.html), and might be the easiest option if you do not have admin privileges on your computer. Once conda is setup, configure it so that the base environment does not automatically load on startup.
```
conda config --set auto_activate_base false
```

Next, create a conda environment in which this program can be run. Use the following command, which should install a sufficiently recent version of python:
```
conda create -n python3 -c conda-forge python=3 pandas openpyxl matplotlib
```
The environment can be activated and deactivated as needed with the following commands:
```
conda activate python3
conda deactivate
```

Next, download this package to the location of your choice with the following command.
```
git clone https://github.com/stevemussmann/gtseqMAF.git
```

If necessary, make the software executable:
```
chmod u+x gtseqMAF.py
```

## Input Requirements
### Required
The input is a Microsoft Excel formatted file (.xlsx). All data should be in a worksheet titled exactly `Final Genotypes`. The first row should be a header line, with cell A1 specifying the individual sample column. Cell B1 to the end should specify locus names. Alleles for a genotype should be concatenated per locus (e.g., AA, AT, etc.). A missing genotype for a locus should be recorded as '0'. 

### Optional
If you want to calculate population allele frequencies, then cell B1 should contain exactly `Population ID` and cell C1 to the end should specify locus names. 
An example file is provided in this repository as `testdata.xlsx`.

## Program Options
Required Inputs:
* **-x / --infile:** Specify an input Excel file containing GTseq data.
Optional Inputs:
* **-p / --populations:** (Boolean switch) Turn on population allele frequency calculations.

## Example Run
Activate your python environment:
```
conda activate python3
```

Place your data file in the same folder as the code you downloaded from this github repository. For example, to run on the test data execute the following command:
```
./gtseqMAF.py -x testdata.xlsx
```

This will create a tab-delimited output file named `global.maf.tsv` which contains global major and minor allele frequencies for each locus:
```
locus   maj_al  maj_cnt maj_freq        min_al  min_cnt min_freq
locus_01        G       13      0.722   C       5       0.278
locus_02        A       12      0.75    G       4       0.25
locus_03        G       6       1.0     NA      0       0.0
locus_04        NA      0       0.0     NA      0       0.0
```

Allele frequencies will also be calculated per population if the `-p` option is invoked:
```
./gtseqMAF.py -x testdata.xlsx -p
```

Populations will be parsed according to the data entered in the `Population ID` column of your Excel document. These allele frequencies will be printed to separate tab-delimited text files for each population. For example, if you have populations named `pop1` and `pop2`, then files named `pop1.maf.tsv` and `pop2.maf.tsv` will be generated.

The tab-delimited text files can be opened in a program such as Microsoft Excel.
