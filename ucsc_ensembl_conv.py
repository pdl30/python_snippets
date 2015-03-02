#!/usr/bin/python

########################################################################
# 12 Jan 2015
# Patrick Lombard, Centre for Stem Stem Research
# Core Bioinformatics Group
# University of Cambridge
# All right reserved.
########################################################################

import subprocess
import sys, re, os
import argparse

def ucsc_conv(ifile, out):
	output = open(out, "w")
	with open(ifile) as f:
		for line in f:
			new_chr = None
			line = line.rstrip()
			word = line.split("\t")
			ichr = word[0]
			if line.startswith("#"):
				pass
			if re.match(r"^\d", word[0]):
				new_chr = "chr" + word[0]
			elif re.match(r"^X", word[0]):
				new_chr = "chrX"
			elif re.match(r"^Y", word[0]):
				new_chr = "chrY"
			elif word[0] == "MT":
				new_chr = "chrM"
			else:
				pass
			del word[0]
			if new_chr:
				output.write("{}\t".format(new_chr)),
				output.write("\t".join(word)),
				output.write("\n"),
	output.close()

def ens_conv(ifile, out):
	output = open(out, "w")
	with open(ifile) as f:
		for line in f:
			line = line.rstrip()
			word = line.split("\t")
			ichr = word[0]
			if line.startswith("#"):
				pass
			if word[0] == "chrM":
				new_chr = "MT"
			else:
				new_chr = word[0].strip("chr")
			del word[0]
			if new_chr:
				output.write("{}\t".format(new_chr)),
				output.write("\t".join(word)),
				output.write("\n"),
	output.close()

def main():
	parser = argparse.ArgumentParser(description='Converts Ensembl/GTF files from UCSC to Ensembl format by default but does vice versa\n')
	parser.add_argument('-i', '--input', help='Input file', required=True)
	parser.add_argument('-e', action='store_true', help='Convert Ensembl to UCSC instead', required=False)
	parser.add_argument('-o', '--output', help='Output file', required=True)
	if len(sys.argv)==1:
		parser.print_help()
		sys.exit(1)
	args = vars(parser.parse_args())

	if args["e"]:
		ens_conv(args["input"], args["output"])
	else:
		ucsc_conv(args["input"], args["output"])

main()