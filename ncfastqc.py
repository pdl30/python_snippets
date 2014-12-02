#!/usr/bin/python

########################################################################
# 20 Oct 2014
# Patrick Lombard, Centre for Stem Stem Research
# Core Bioinformatics Group
# University of Cambridge
# All right reserved.
########################################################################

import argparse
import subprocess
import sys, re, os

def run_fastqc(fq1):
	devnull = open('/dev/null', 'w')
	command = ["fastqc", "{}".format(fq1)] #outdir must exist!
	subprocess.call(command,  stdout=devnull)

def find_adapters(fq):
	adapters = []
	idir = re.sub(".fastq","", fq)
	report = idir+"_fastqc/fastqc_data.txt"
	flist = open(report).readlines()
	parsing = False
	for line in flist:
		if line.startswith(">>Overrepresented sequences\tfail"):
			parsing = True
		elif line.startswith(">>END_MODULE"):
			parsing = False
		if parsing:
			if line.startswith(">>"):
				continue
			if line.startswith("#"):
				continue
			else:
				line = line.rstrip()
				word = line.split("\t")
				if word[3] != "No Hit":
					adapters.append(word[0])
	return adapters

def single_cut_adapters(adapters, fq1, outdir):
	devnull = open('/dev/null', 'w')
	adapt1 = ""
	for i in adapters:
		adapters = "-a {} ".format(i)
		adapt1 = adapters+adapt1
	command1 = "cutadapt -q 20 {0} --minimum-length=10 -o {1}/trimmed.fastq {2}".format(adapt1, outdir, fq1)
	p = subprocess.Popen(command1.split())
	p.communicate()

def paired_cut_adapters(adapters, fq1, outdir, rev_adapters, fq2):
	devnull = open('/dev/null', 'w')
	adapt1 = ""
	for i in adapters:
		adapters = "-a {} ".format(i)
		adapt1 = adapters+adapt1

	adapt2 = ""
	for i in rev_adapters:
		adapters = "-a {} ".format(i)
		adapt2 = adapters+adapt2

	command1 = "cutadapt -q 20 {0} --minimum-length=10 --paired-output {1}/tmp.2.fastq -o {1}/tmp.1.fastq {2} {3}".format(adapt1, outdir, fq1, fq2)
	p = subprocess.Popen(command1.split())
	p.communicate()
	command2 = "cutadapt -q 20 {0} --minimum-length=10 --paired-output {1}/trimmed_1.fastq -o {1}/trimmed_2.fastq {1}/tmp.2.fastq {1}/tmp.1.fastq".format(adapt2, outdir)
	p = subprocess.Popen(command2.split())
	p.communicate()
	cleanup = ["rm", "{0}/tmp.2.fastq".format(outdir), "{0}/tmp.1.fastq".format(outdir)]
	subprocess.call(cleanup, stdout=devnull)

def main():
	parser = argparse.ArgumentParser(description='FastQC QC and adapter trimmer\n ')
	parser.add_argument('-f','--fastq', help='Single end fastq', required=False)
	parser.add_argument('-p','--pair', help='Paired end fastqs. Please put them in order!', required=False, nargs='+')
	parser.add_argument('-o','--outdir', help='Name of results directory', required=True)
	args = vars(parser.parse_args())
	path = os.getcwd()
	if os.path.isdir(args["outdir"]):
		print("Results directory already exists!")
	else:
		subprocess.call(["mkdir", args["outdir"]])
	if args["pair"]:
		fq1 = args["pair"][0]
		fq2 = args["pair"][1]
		print "==> Running FastQC...\n"
		#run_fastqc(fq1)
		#run_fastqc(fq2)
		fwd_adapt = find_adapters(fq1)
		rev_adapt = find_adapters(fq2)
		if fwd_adapt or rev_adapt:
			print "==> Removing adapters...\n"
			paired_cut_adapters(fwd_adapt, fq1, args["outdir"], rev_adapt, fq2)
			fq1 = args["outdir"]+"/trimmed_1.fastq"
			fq2 = args["outdir"]+"/trimmed_2.fastq"
	elif args["fastq"]:
		fq1 = args["fastq"]
		print "==> Running FastQC...\n"
		run_fastqc(fq1)
		adapt = find_adapters(fq1)
		if adapt:
			print "==> Removing adapters...\n"
			single_cut_adapters(adapt, fq1, args["outdir"])
			fq1 = args["outdir"]+"/trimmed.fastq"

main()
