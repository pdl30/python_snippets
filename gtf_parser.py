#!/usr/bin/python

########################################################################
# 14 Oct 2015
# Patrick Lombard, Centre for Stem Stem Research
# Core Bioinformatics Group
# University of Cambridge
# All right reserved.
########################################################################

import subprocess
import sys, re, os
import argparse

def bed_to_gtf(ifile, output):
	with open(ifile) as f:
		c = 0
		for line in f:
			line = line.rstrip()
			word = line.split("\t")
			if int(word[2]) > int(word[1]):
				if len(word) >= 6:
					output.write("""{}\tBEDtoGTF\texon\t{}\t{}\t.\t{}\t.\tgene_id "{}";\n""".format(word[0],word[1], word[2], word[5], word[3])),
				elif len(word) == 3:
					output.write("""{}\tBEDtoGTF\texon\t{}\t{}\t.\t+\t.\tgene_id "gene_{}";\n""".format(word[0],word[1], word[2], c)),
					c += 1

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Converts an bed file to gtf file, tested with HTSEQ-count. Accepts either BED3 or BED6\n')
	parser.add_argument('-i', '--input', help='input bed file', required=True) 
	parser.add_argument('-o', '--output', help='output GTF file', required=True) 
	if len(sys.argv)==1:
		parser.print_help()
		sys.exit(1)
	args = vars(parser.parse_args())
	#Change how you do things, supply file handles and return them
	outfile = open(args["output"], "w")
	bed_to_gtf(args["input"], outfile)
	outfile.close()
	#Test by supplying temp filehandle which is then deleted after testing!

