#!/usr/bin/python

########################################################################
# 09 Oct 2014
# Patrick Lombard, Centre for Stem Research
# Core Bioinformatics Group
# University of Cambridge
# All right reserved.
########################################################################

import os, re, sys
import argparse

def split(ifile, oend):
	data = {}
	with open(ifile) as f:
		header = next(f)
		header = header.rstrip()
		head = header.split("\t")
		for i in range(1, len(head)):
			data[head[i]] = {}
		for line in f:
			line = line.rstrip()
			word = line.split("\t")
			for i in range(1, len(word)):
				data[head[i]][word[0]] = word[i]
	for key in data:
		output = open(key + oend, "w")
		for value in sorted(data[key]):
			output.write("{}\t{}\n".format(value, data[key][value])),
		output.close()

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Splits a file by column with output files named by column name. Will treat column one as rownames\n ')
	parser.add_argument('-i', '--input', help='Input matrix', required=False)
	parser.add_argument('-e', '--end', help='Output files ending name', required=False)
	args = vars(parser.parse_args())
	split(args["input"], args["end"])