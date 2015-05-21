#!/usr/bin/python

########################################################################
# 28 July 2014
# Patrick Lombard, Centre for Stem Research
# Core Bioinformatics Group
# University of Cambridge
# All right reserved.
########################################################################

import os, re, sys
import argparse

def read_dir(idir):
	ifiles = [f for f in os.listdir(idir) if f.endswith(".count")]
	result = {}
	for ifile in ifiles:
		name = ifile.strip(".count$")
		result[name] = {}
		count_sum, amb, no_feature = read_count(idir + "/" + ifile)
		result[name]["Transcript counts"] = count_sum
		result[name]["Ambiguous counts"] = amb
		result[name]["Counts with no features"] = no_feature
		result[name]["Total Unique counts"] = count_sum + amb + no_feature
	return result

def read_count(count):
	count_sum = 0
	with open(count) as f:
		for line in f:
			line = line.rstrip()
			word = line.split("\t")
			if word[0] == "__no_feature":
				no_feature = int(word[1])
			elif word[0] == "__ambiguous":
				amb = int(word[1])
			elif word[0] == "__too_low_aQual" or word[0] == "__not_aligned" or word[0] == "__alignment_not_unique":
				pass
			else:
				count_sum += int(word[1])
	return count_sum, amb, no_feature

def read_ifile(ifile):
	result = {}
	name = ifile.strip(".count$")
	result[name] = {}
	count_sum, amb, no_feature = read_count(ifile)
	result[name]["Transcript counts"] = count_sum
	result[name]["Ambiguous counts"] = amb
	result[name]["Counts with no features"] = no_feature
	result[name]["Total Unique counts"] = count_sum + amb + no_feature
	return result

def write(result, out):
	output = open(out, "w")
	for key in sorted(result):
		for key2 in sorted(result[key]):
			output.write("{}\t{}\t{}\n".format(key, key2, result[key][key2]))
	output.close()

def main():
	parser = argparse.ArgumentParser(description='Pyrnapipe is a pipeline for RNA-seq and ChIP-seq samples from the GEO database\n')
	parser.add_argument('-i', '--idir', help='Input directory, files must end in .count', required=False)
	parser.add_argument('-c', '--counts', help='Single counts file', required=False)
	parser.add_argument('-o', '--output', help='Report file', required=True)
	if len(sys.argv)==1:
		parser.print_help()
		sys.exit(1)
	args = vars(parser.parse_args())

	if args["idir"]:
		result = read_dir(args["idir"])
	elif args["counts"]:
		result = read_ifile(args["counts"])
	write(result, args["output"])


main()