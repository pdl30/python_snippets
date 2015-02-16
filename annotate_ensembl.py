#!/usr/bin/python

########################################################################
# 28 Apr 2014
# Patrick Lombard, Centre for Stem Stem Research
# Core Bioinformatics Group
# University of Cambridge
# All right reserved.
########################################################################


import argparse
import subprocess
import sys
import re
import os
import rpy2.robjects as ro
import csv
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import IntVector, FloatVector, StrVector
from collections import defaultdict


def annotate_ensembl(dict_obj):
	ens = importr("biomaRt")
	ensembl = ro.r.useMart("ensembl")
	genome="mmusculus_gene_ensembl"
	ensembl = ro.r.useDataset(genome, mart=ensembl)
	values = []
	for key1 in dict_obj:
		values.append(key1)
	C1BM = ro.r.getBM(attributes=StrVector(["ensembl_gene_id", "chromosome_name", "start_position", "end_position", "strand", "external_gene_name", "description", "gene_biotype"]), 
		filters="ensembl_gene_id", values=values, mart=ensembl)
	gene = list(C1BM.rx(True,1))
	chr1 = list(C1BM.rx(True,2))
	tss = list(C1BM.rx(True,3))
	end = list(C1BM.rx(True,4))
	st = list(C1BM.rx(True,5))
	name = list(C1BM.rx(True,6))
	des = list(C1BM.rx(True,7))
	bio = list(C1BM.rx(True,8))
	data = {}
	for index, g in enumerate(gene):
		data[g] = (chr1[index], tss[index], end[index], st[index], name[index], des[index], bio[index])
	return data

def reverse_dict(idict):
	inv_map = {}
	for k, v in idict.iteritems():
		inv_map[v] = inv_map.get(v, [])
		inv_map[v].append(k)
	return inv_map

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Annotate ensembl count matrices\n')
	parser.add_argument('-i','--input', help='Counts Matrix', required=True)
	parser.add_argument('-o','--output', help='Output name', required=True)
	if len(sys.argv)==1:
		parser.print_help()
		sys.exit(1)
	args = vars(parser.parse_args())
	idata = {}
	with open(args["input"]) as f:
		header = next(f)
		for line in f:
			line = line.rstrip()
			word = line.split("\t")
			ens = word[0].strip(" ")
			m = re.match("__", ens)
			if m:
				pass
			elif line.startswith("#"):
				pass
			else:
				idata[ens] = line
	results = annotate_ensembl(idata)
	output = open(args["output"], "w")
	header= header.rstrip()
	output.write("{}\tGene Name\tDescription\tBiotype\n".format(header)),
	for key in sorted(idata):
		anno = results.get(key, None)
		if anno:
			output.write("{}\t{}\t{}\t{}\n".format(idata[key], results[key][4], results[key][5],results[key][6])),
		else:
			output.write("{}\n".format(idata[key])),