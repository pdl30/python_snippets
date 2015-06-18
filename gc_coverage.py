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
import tempfile
import numpy
import HTSeq
import tempfile
from datetime import date
import ConfigParser

today = date.today()
date_format = "{}_{}_{}".format(today.day, today.month, today.year)

def get_genes(tss=False):
	genes = {}
	with open("/home/patrick/Scripts/pyatactools/pyatactools/data/mm10_ensembl_80.txt") as f:
		next(f)
		for line in f:
			line = line.rstrip()
			word = line.split("\t")
			if word[4] == "1":
				strand = "+"
			else:
				strand = "-"
			if re.match(r"^\d", word[1]):
				new_chr = "chr" + word[1]
			elif re.match(r"^X", word[1]):
				new_chr = "chrX"
			elif re.match(r"^Y", word[1]):
				new_chr = "chrY"
			elif word[1] == "MT":
				new_chr = "chrM"
			else:
				pass
			if tss:
				genes[word[0]] = (new_chr, int(word[2]), strand)
			else:
				genes[word[0]] = (new_chr, word[2], word[3], strand)
	return genes

def write_bed(genes, tss=False):
	g_file = tempfile.NamedTemporaryFile(delete = False)
	for g in genes:
		if tss:
			start = int(genes[g][1]) - 2000
			if start < 0:
				start = 0
			g_file.write("{}\t{}\t{}\t{}\t0\t{}\n".format(genes[g][0], start, int(genes[g][1]) + 2000, g, genes[g][2])),
		else:
			g_file.write("{}\t{}\t{}\t{}\t0\t{}\n".format(genes[g][0], genes[g][1], genes[g][2], g, genes[g][3])),
	g_file.close()
	print g_file.name
	return g_file.name

def bedtofasta(g_file):
	fa_file = tempfile.NamedTemporaryFile(delete = False)
	fa_file.close()
	command = "fastaFromBed -fi /home/patrick/Reference_Genomes/mm10/UCSC/Sequence/ucsc_mm10.fa -bed {} -fo {}".format(g_file, fa_file.name)
	subprocess.call(command.split())
	return fa_file.name

def reverse_dict(idict):
	inv_map = {}
	for k, v in idict.iteritems():
		inv_map[v] = inv_map.get(v, [])
		inv_map[v].append(k)
	return inv_map

def read_fasta(fa_file, rev_genes, tss=False):
	result = {}
	for s in HTSeq.FastaReader( fa_file ):
		name = s.name.split(":")
		pos = name[1].split("-")
		name = name[0].strip(">")
		if tss:
			gene = rev_genes.get((name, int(pos[1])- 2000, "+"), None)
			if gene == None:
				gene = rev_genes.get((name, int(pos[1]) - 2000, "-"), None)
				s =  s.get_reverse_complement()
		else:
			gene = rev_genes.get((name, pos[0], pos[1], "+"), None)
			if gene == None:
				gene = rev_genes.get((name, pos[0], pos[1], "-"), None)
				s =  s.get_reverse_complement()
		AT= 0
		GC =0
		for i in list(str(s.seq)):
			if i.upper() == "A" or i.upper() == "T":
				AT += 1
			elif i.upper() == "G" or i.upper() == "C":
				GC += 1
		if AT == 0 and GC == 0:
			pass
		else:
			tot = GC+AT
			res = float(GC)/tot
			result[gene[0]] = res
	return result

def separate_genes(gc_content, outdir):
	output1 = open(outdir+'/1st_gc_genes.txt', "w")
	output2 = open(outdir+'/2nd_gc_genes.txt', "w")
	output3 = open(outdir+'/3rd_gc_genes.txt', "w")
	output4 = open(outdir+'/4th_gc_genes.txt', "w")
	gc_values = list(gc_content.values())
	one = numpy.percentile(gc_values, 25)
	two = numpy.percentile(gc_values, 50)
	three = numpy.percentile(gc_values, 75)
	four = numpy.percentile(gc_values, 100)
	for key in gc_content:
		if float(gc_content[key]) < one:
			output1.write("{}\n".format(key)),
		elif float(gc_content[key]) < two:
			output2.write("{}\n".format(key)),
		elif float(gc_content[key]) < three:
			output3.write("{}\n".format(key)),
		else:
			output4.write("{}\n".format(key)),

def run_ngs(conditions, outdir, tss=False):
	for key in conditions:
		config = open(outdir+'/{}_ngs_config.txt'.format(conditions[key]), "w")
		config.write("{}\t{}/1st_gc_genes.txt\t'1st Quantile'\n".format(key, outdir)),
		config.write("{}\t{}/2nd_gc_genes.txt\t'2nd Quantile'\n".format(key, outdir)),
		config.write("{}\t{}/3rd_gc_genes.txt\t'3rd Quantile'\n".format(key, outdir)),
		config.write("{}\t{}/4th_gc_genes.txt\t'4th Quantile'\n".format(key, outdir)),
		config.close()
		if tss:
			command = "ngs.plot.r -C {}/{}_ngs_config.txt -G mm10 -O {}/{}_{}_tss -R tss -D ensembl -FL 300".format(outdir, conditions[key], outdir, conditions[key], date_format)
			subprocess.Popen(command.split())
		else:
			command = "ngs.plot.r -C {}/{}_ngs_config.txt -G mm10 -O {}/{}_{}_genebody -R genebody -D ensembl -FL 300".format(outdir, conditions[key], outdir, conditions[key], date_format)
			subprocess.Popen(command.split())

def ConfigSectionMap(Config, section):
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

def main():
	parser = argparse.ArgumentParser(description='Plots quantiles of genes/tss regions of bam files\n')
	subparsers = parser.add_subparsers(help='Programs included',dest="subparser_name")
	tss_parser = subparsers.add_parser('tss', help='TSS plotter')
	tss_parser.add_argument('-c', '--config', help='Contains [Conditions] with bam files as keys.', required=False)
	tss_parser.add_argument('-o', '--outdir', help='Output directory', required=True)
	gene_parser = subparsers.add_parser('gene', help='Genebody plotter')
	gene_parser.add_argument('-c', '--config', help='Contains [Conditions] with bam files as keys.', required=False)
	gene_parser.add_argument('-o', '--outdir', help='Output directory', required=True)
	if len(sys.argv)==1:
		parser.print_help()
		sys.exit(1)
	args = vars(parser.parse_args())
	Config = ConfigParser.ConfigParser()
	Config.optionxform = str
	Config.read(args["config"])
	conditions = ConfigSectionMap(Config, "Conditions")
	if args["subparser_name"] == "gene":
		print "Genebody GC analysis...\n"
		genes = get_genes()
		rev_genes = reverse_dict(genes)
		g_file = write_bed(genes)
		fa_file = bedtofasta(g_file)
		gc_content = read_fasta(fa_file, rev_genes)
		separate_genes(gc_content, args["outdir"])
		run_ngs(conditions, args["outdir"])
	if args["subparser_name"] == "tss":
		print "TSS GC analysis...\n"
		genes = get_genes(tss=True)
		rev_genes = reverse_dict(genes)
		g_file = write_bed(genes, tss=True)
		fa_file = bedtofasta(g_file)
		gc_content = read_fasta(fa_file, rev_genes, tss=True)
		separate_genes(gc_content, args["outdir"])
		run_ngs(conditions, args["outdir"], tss=True)

main()