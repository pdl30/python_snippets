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
import ConfigParser
from multiprocessing import Pool
import itertools

def ConfigSectionMap(section, Config):
	dict1 = {}
	options = Config.options(section)
	for option in options:
		try:
			dict1[option] = Config.get(section, option)
			if dict1[option] == -1:
				DebugPrint("skip: %s" % option)
		except:
			print("exception on %s!" % option)
			dict1[option] = None
	return dict1

def read_config(conditions):
	data = {}
	output = open(outfile, "w")
	output.write("ID"),
	for key in sorted(conditions):
		data[key] = {}
		with open(key) as f:
			for line in f:
				line = line.rstrip()
				word = line.split("\t")
				if word[0].startswith("__"):
					pass
				else:
					data[key][word[0]] = word[1]
	return data

def read_spread(ifile):
	data = {}
	with open(ifile) as f:
		header = next(f)
		head = header.rstrip().split("\t")
		for i in range(1, len(head)):
			data[i] = {}
		for line in f:
			line = line.rstrip()
			word = line.split("\t")
			for i in range(1, len(word)):
				data[head[i]][word[0]] = word[i]
	return data

def 

def main():
	parser = argparse.ArgumentParser(description='Converts counts between TPM, RPKM and DESEQ2 normalised formats\n')
	parser.add_argument('-c','--config', help='Config file with [Conditions] with keys as count files and values as output file', required=True)
	parser.add_argument('-i','--input', help='Spreadsheet of counts with first column as genes.', required=False)
	parser.add_argument('-n','--genome', help='Samples genome aligned to, options are hg19/mm10', required=True)
	parser.add_argument('-g','--gtf', help='GTF for annotation. If not supplied, will use the packages GTF')
	parser.add_argument('-t', help='Converts counts to TPM', action="store_true", required=False)
	parser.add_argument('-r', help='Converts counts to RPKM',  action="store_true", required=False)
	parser.add_argument('-d', help='Converts counts to DESEQ2 normalised counts',  action="store_true", required=False)
	parser.add_argument('-o','--output', help='Output file for Spreadsheet input', required=True)
	if len(sys.argv)==1:
		parser.print_help()
		sys.exit(1)
	args = vars(parser.parse_args())

	if args["config"]:
		Config = ConfigParser.ConfigParser()
		Config.optionxform = str
		Config.read(args["config"])
		conditions = ConfigSectionMap("Conditions", Config)
		counts = read_config(conditions)
	elif args["input"]:
		counts = read_spread(args["input"])
