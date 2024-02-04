import argparse
import os.path
import distutils.util

class ComLine():
	'Class for implementing command line options'


	def __init__(self, args):
		parser = argparse.ArgumentParser()
		parser._action_groups.pop()
		required = parser.add_argument_group('required arguments')
		optional = parser.add_argument_group('optional arguments')
		required.add_argument("-x", "--infile",
							dest='infile',
							required=True,
							help="Specify an Excel file in xlsx format for input."
		)
		optional.add_argument("-p", "--populations",
							dest='populations',
							action='store_true',
							help="Turn on population allele frequency calculations."
		)
		self.args = parser.parse_args()

		#check if input file ends with .xlsx
		if not self.args.infile.endswith(".xlsx"):
			print("ERROR: Input file " + self.args.infile + " does not end with .xlsx file extension.")
			print("Is this a valid excel file?")
			print("Exiting Program...")
			print("")
			raise SystemExit

	def exists(self, filename):
		if( os.path.isfile(filename) != True ):
			print("")
			print(filename, "does not exist")
			print("Exiting program...")
			print("")
			raise SystemExit
