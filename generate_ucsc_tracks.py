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
from os.path import isfile, join

def generate_tracks(path, user, password, genome):
	if path == None:
			path = os.getcwd()
	link = re.sub("/raid", "", path)
	if user:	
		link = re.sub("/home/pdl30/htdocs/", "http://{}:{}@patrick.results.cscr.cam.ac.uk/".format(user, password), link)
	else:
		link = re.sub("/home/pdl30/htdocs/", "http://patrick.results.cscr.cam.ac.uk/", link)
	files = [ f for f in os.listdir(path) if isfile(join(path,f)) ]
	output = open("tracks.txt", "w")
	for f in sorted(files, reverse=True):
		if f.endswith(".bb"):
			name = f.strip(".bb")
			output.write("""track type=bigBed name="{0}_peaks" description="{0}_Peaks" bigDataUrl={1}/{2} visibility=dense color=31,120,180\n""".format(name, link, f))
		elif f.endswith(".bw"):
			name = f.strip(".bw")
			output.write("""track type=bigWig name="{0}_track" description="{0}_Track" bigDataUrl={1}/{2} alwaysZero=on windowingFunction=maximum visibility=full\n""".format(name, 
				link, f))
	output.close()
	output = open("links.txt", "w")
	if genome == "mm10":
		output.write("http://genome-euro.ucsc.edu/cgi-bin/hgTracks?org=mouse&hgt.customText={}/tracks.txt&db=mm10\n".format(link))
	elif genome == "hg19":
		output.write("http://genome-euro.ucsc.edu/cgi-bin/hgTracks?org=human&hgt.customText={}/tracks.txt&db=hg19\n".format(link))
	elif genome == "mm9":
		output.write("http://genome-euro.ucsc.edu/cgi-bin/hgTracks?org=human&hgt.customText={}/tracks.txt&db=mm9\n".format(link))
	output.close()


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Generates UCSC tracks by reading all bigBig and bigWig files in a directory and creates a link for vizualisation on UCSC\n')
	parser.add_argument('-p', '--path', help='Optional path to directory', required=False)
	parser.add_argument('-u', '--user', help='Optional username', required=False)
	parser.add_argument('-a', '--pass', help='Optional password', required=False)
	parser.add_argument('-g', '--genome', help='Default=mm10, hg19 and mm9 available', default="mm10", required=False)
	args = vars(parser.parse_args())
	generate_tracks(args["path"], args["user"], args["pass"], args["genome"])