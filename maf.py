import pandas

class MAF():
	'Class for calculating minor allele frequency from GTseq genotype files'

	def __init__(self, df, prefix):
		self.pdf = df
		self.outfile = prefix + ".maf.tsv"

	def getMajorMinor(self):
		f = open(self.outfile, "w")
		f.write("locus\tmaj_al\tmaj_cnt\tmaj_freq\tmin_al\tmin_cnt\tmin_freq\n")
		#print("locus\tmaj_al\tmaj_cnt\tmaj_freq\tmin_al\tmin_cnt\tmin_freq")

		# get counts of all genotypes at each locus and put into dictionary
		for columnName, columnData in self.pdf.items():
			alleledict = self.pdf[columnName].value_counts().to_dict()
			allelecounts = dict() #store allele counts for this locus
			for key, value in alleledict.items():
				# ignore missing data values
				# casting as str() in next line because sometimes Excel encodes as int or string
				if str(key) != "0":
					alleles = list(key)
					for allele in alleles:
						count = allelecounts.get(allele, 0) #return 0 if key does not exist yet
						count += value
						allelecounts[allele] = count

			#determine major and minor alleles based upon counts
			try:
				major = max(allelecounts, key=allelecounts.get) #get major allele
				majCount = max(allelecounts.values())
				
			except ValueError:
				#print("Cannot calculate major allele for", columnName, ": All data missing.")
				major = "NA"
				majCount = 0

			try:
				minor = min(allelecounts, key=allelecounts.get) #get minor allele
				minCount = min(allelecounts.values())
			except ValueError:
				#print("Cannot calculate minor allele: All data missing.")
				minor = "NA"
				minCount = 0
		
			# calculate major and minor allele frequencies
			total = majCount + minCount
			# check if monomorphic locus and reset total to major allele count if true
			if len(allelecounts.keys()) == 1:
				total=majCount
			elif len(allelecounts.keys()) > 2:
				print("WARNING: locus", columnName, "has >2 alleles.")

			# major frequency
			try:
				majFreq = majCount / total
			except ZeroDivisionError:
				majFreq = 0.0

			# minor frequency
			try:
				minFreq = minCount / total
			except ZeroDivisionError:
				minFreq = 0.0

			# if macs are equal, grab alleles in order they appear in dict. THIS ASSUMES BIALLELIC LOCI AND WILL BE BROKEN IF >2 ALLELES.
			if majCount == minCount and majCount != 0:
				major = str(list(allelecounts.keys())[0])
				minor = str(list(allelecounts.keys())[-1])
				# check if monomorphic locus
				if major is minor and majCount == minCount:
					minor="NA"
					minCount=0.0
					minFreq=0.0

			# print output with freq restricted to 3 decimal places
			#print(columnName, end="\t")
			#print(major, end="\t")
			#print(majCount, end="\t")
			#print('{:.3}'.format(majFreq), end="\t")
			#print(minor, end="\t")
			#print(minCount, end="\t")
			#print('{:.3}'.format(minFreq))
			
			f.write(columnName)
			f.write("\t")
			f.write(major)
			f.write("\t")
			f.write(str(majCount))
			f.write("\t")
			f.write(str('{:.3}'.format(majFreq)))
			f.write("\t")
			f.write(minor)
			f.write("\t")
			f.write(str(minCount))
			f.write("\t")
			f.write(str('{:.3}'.format(minFreq)))
			f.write("\n")

		f.close()
