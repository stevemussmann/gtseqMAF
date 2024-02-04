#!/usr/bin/env python3

from comline import ComLine
from gtseq import GTseq
from maf import MAF

import argparse
import os
import pandas
import re
import sys

def main():
	input = ComLine(sys.argv[1:])

	# make list of file formats; grab relevant options from argparse object
	d = vars(input.args)
	
	# modify input .xslx filename to replace space with _ and remove .xlsx extension
	fileName = input.args.infile.replace(" ", "_") #replace spaces in original filename if they exist
	fileName = re.sub('.xlsx$', '.REPLACE.xlsx', fileName)
	logfile = re.sub('.REPLACE.xlsx$', '.log', fileName)
	
	#check if logfile exists and delete if true
	if os.path.isfile(logfile):
		os.remove(logfile)

	gtFile = GTseq(input.args.infile, logfile)
	pdf = gtFile.parseFile() #returns pandas dataframe with unfiltered data
	pops = gtFile.getPops(pdf) #remove populations column

	s = sorted(list(set(pops.values()))) # make list of populations

	# calculate global major and minor allele frequencies
	gtmaf = MAF(pdf, "global")
	print("Writing global allele frequencies to global.maf.tsv")
	print("")
	gtmaf.getMajorMinor()
	
	# calculate major and minor allele frequencies for populations
	for pop in s:
		samples = list([k for k, v in pops.items() if v is pop]) # get list of samples in this population
		popdf = pdf.loc[samples] # pull those samples from the global pandas dataframe
		print("Writing population allele frequencies for ", pop, " to ", pop, ".maf.tsv.", sep="" )
		print("")
		popmaf = MAF(popdf, pop)
		popmaf.getMajorMinor()


main()

raise SystemExit
