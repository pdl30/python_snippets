#!/usr/bin/python

########################################################################
# 08 Oct 2014
# Patrick Lombard, Centre for Stem Stem Research
# Core Bioinformatics Group
# University of Cambridge
# All right reserved.
########################################################################

import argparse
import subprocess
import os, re, sys
from multiprocessing import Pool
import ConfigParser
import itertools

def sam_to_bam(sam):
	name = sam.rstrip("$.sam")
	print name
	command1 = "samtools view -bS {} > {}.bam".format(sam, name)
	command2 = "samtools sort {0}.bam {0}_sort".format(name)
	command3 = "samtools index {}_sort.bam".format(name)
	subprocess.call(command1, shell=True)
	subprocess.call(command2.split())
	subprocess.call(command3.split())

def function1(args):
	return sam_to_bam(*args)

def ConfigSectionMap(section):
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

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='QC results from htSeqTools package. Not even close to finished!\n')
	parser.add_argument('-config', help='Config file containing [Conditions] i.e. sam files, please see documentation for usage!', required=True)
	parser.add_argument('-threads', help='Number of threads to use, default=4', default=4, required=False) #Careful here!! v.v. high memory usage
	args = vars(parser.parse_args())
	Config = ConfigParser.ConfigParser()
	Config.optionxform = str
	Config.read(args["config"])

	conditions = ConfigSectionMap("Conditions")
	pool = Pool(int(args["threads"]))
	keys = list(conditions.keys())
	pool.map(function1, itertools.izip(keys))
	pool.close()
	pool.join()