#!/usr/bin/env python3

from comline import ComLine
from gtseq import GTseq
from maf import MAF
#from gtconvert import GTconvert

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
	#pops = gtFile.getPops(pdf) #remove populations column

	# calculate minor allele frequency
	gtmaf = MAF(pdf)
	gtmaf.getMajorMinor()

main()

raise SystemExit
