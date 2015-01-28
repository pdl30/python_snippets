#!/usr/bin/python

########################################################################
# 28 Jan 2015
# Patrick Lombard, Centre for Stem Stem Research
# Core Bioinformatics Group
# University of Cambridge
# All right reserved.
########################################################################

import subprocess
import sys, os, re
import argparse

def read_tracks(ifile, anno, out):
	output = open(out, "w")
	with open(ifile) as f:
		for line in f:
			if line.startswith("track type=bigWig"):
				line = line.rstrip()
				word = line.split("\"")
				gsm =  word[1].strip("_track$")
				if gsm in anno:
					output.write('''{}"{}"{}"{}"{}\n'''.format(word[0], word[1], word[2], anno[gsm], word[4]))
				else:
					output.write('''{}"{}"{}"{}"{}\n'''.format(word[0], word[1], word[2], word[3], word[4]))
			else:
				output.write('''{}"{}"{}"{}"{}\n'''.format(word[0], word[1], word[2], word[3], word[4]))
	output.close()

def read_anno(ifile):
	anno = {}
	with open(ifile) as f:
		for line in f:
			line = line.rstrip()
			word = line.split("\t")
			anno[word[0]] = word[1]
	return anno

def main():
	parser = argparse.ArgumentParser(description='Replaces description text in tracks file\n')
	parser.add_argument('-t', '--tracks', help='UCSC format tracks file', required=True)
	parser.add_argument('-a', '--anno', help='2 column format with GSM and description text', required=True)
	parser.add_argument('-o', '--out', help='Output file', required=True)
	if len(sys.argv)==1:
		parser.print_help()
		sys.exit(1)
	args = vars(parser.parse_args())
	anno = read_anno(args["anno"])
	read_tracks(args["tracks"], anno, args["out"])

main()