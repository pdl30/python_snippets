#!/usr/bin/python

import sys, re, os
import argparse

def split_file(ifile, number_of_lines, output_name):
	ifile1 = open(ifile, "r")
	idata = ifile1.read().split("\n")
	count = 0
	split = int(number_of_lines)
	for lines in range(0, len(idata), split):
		outputData = idata[lines:lines+split]
		output = open("{}_{}".format(output_name, count)+".txt", "w")
		output.write('\n'.join(outputData))
		output.close()
		count += 1

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Splits a file\n ')
	parser.add_argument('-i','--IFILE', help='Input file', required=True)
	parser.add_argument('-n','--NUM', help='Number of lines per split', required=True)
	parser.add_argument('-o','--OUTPUT', help='Output prefix', required=True)
	args = vars(parser.parse_args())
	split_file(args["IFILE"], args["NUM"], args["OUTPUT"])