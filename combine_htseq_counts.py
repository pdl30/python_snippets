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
from collections import defaultdict

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

def join_counts(idir, output):
	ifiles = [f for f in os.listdir(idir) if f.endswith(".count")]
	data = defaultdict(list)
	output = open(output, "w")
	output.write("ID"),
	for count in sorted(ifiles):
		name = os.path.basename(count)
		name= re.sub(".count$", "", name)
		output.write("\t{}".format(name)),
		with open(count) as f:
			for line in f:
				line = line.rstrip()
				word = line.split("\t")
				if word[0].startswith("__"):
					pass
				else:
					data[word[0]].append(word[1])
	output.write("\n"),
	for key2 in sorted(data):
		data2 = data[key2]
		output.write(key2+"\t" + "\t".join(data2) + "\n"),
	output.close()

def main():
	parser = argparse.ArgumentParser(description='Combines counts\n')

	parser.add_argument('-i', '--idir', help='Input directory, files must end in .count', required=False)
	#parser.add_argument('-c', '--counts', help='Single counts file instead of input directory', required=False)
	parser.add_argument('-o', '--output', help='Report file', required=True)
	parser.add_argument('-c', '--combined', help='Combined counts file', required=True)
	if len(sys.argv)==1:
		parser.print_help()
		sys.exit(1)
	args = vars(parser.parse_args())

	if args["idir"]:
		result = read_dir(args["idir"])

	write(result, args["output"])
	join_counts(args["idir"], args["combined"])

main()