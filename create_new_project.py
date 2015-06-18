#!/usr/bin/python

########################################################################
# 11 Jan 2015
# Patrick Lombard, Centre for Stem Stem Research
# Core Bioinformatics Group
# University of Cambridge
# All right reserved.
########################################################################

import subprocess
import sys, re, os
import argparse
from sh import touch
import datetime

def create_dirs(idir):
	if os.path.isdir(idir):
		print "Directory already exists!"
	else:
		os.mkdir(idir)
	if os.path.isdir(idir+ "/analysis"):
		pass
	else:
		os.mkdir(idir + "/analysis")
	if os.path.isdir(idir+ "/alignment"):
		pass
	else:
		os.mkdir(idir + "/alignment")
	if os.path.isdir(idir+ "/results"):
		pass
	else:
		os.mkdir(idir + "/results")
	if os.path.isdir(idir+ "/scripts"):
		pass
	else:
		os.mkdir(idir + "/scripts")
	output = open("{}/scripts/main.py".format(idir), "w")
	output.write("""#!/usr/bin/python

########################################################################
# {}
# Patrick Lombard, Centre for Stem Stem Research
# Core Bioinformatics Group
# University of Cambridge
# All right reserved.
########################################################################

import subprocess
import sys, re, os
import argparse

base_dir = "{}"
raw_data = base_dir + '/raw_data'
anal_dir = base_dir + '/analysis'
align_dir = base_dir + '/alignment'
scripts_dir = base_dir + '/scripts/'\n""".format(datetime.date.today(), os.path.abspath(idir)))
	
	output.close()
	if os.path.isdir(idir+ "/logs"):
		pass
	else:
		os.mkdir(idir + "/logs")
	if os.path.isdir(idir+ "/raw_data"):
		pass
	else:
		os.mkdir(idir + "/raw_data")

def get_r_packages(idir):
	rscript = " y <- installed.packages()\n"
	rscript += "z <- y[,1:3]\n"
	rscript += "write.table(z, file='{}/logs/R_log.txt', sep='\\t', quote=F)\n".format(idir)
	run_rcode(rscript, "rpackages.R")
	os.remove("rpackages.R")

def get_logs(idir):
	subprocess.call("pip freeze > {}/logs/python_log.txt".format(idir), shell=True)
	subprocess.call("dpkg -l > {}/logs/base_packages_log.txt".format(idir), shell=True)
	get_r_packages(idir)
	misc_programs(idir)

def run_rcode(rscript, name):
	rcode = open(name, "w")
	rcode.write(rscript)
	rcode.close()
	try:
		subprocess.call(['Rscript', name])
	except:
		error("Error in running {}\n".format(name))
		error("Error: %s\n" % str(sys.exc_info()[1]))
		error( "[Exception type: %s, raised in %s:%d]\n" % ( sys.exc_info()[1].__class__.__name__, 
		os.path.basename(traceback.extract_tb( sys.exc_info()[2] )[-1][0]), 
		traceback.extract_tb( sys.exc_info()[2] )[-1][1] ) )
		sys.exit(1)

def misc_programs(idir):
	subprocess.call("tophat2 --version > {}/logs/misc_log.txt".format(idir), shell=True)
	subprocess.call("echo '-----------------' >> {}/logs/misc_log.txt".format(idir), shell=True)
	subprocess.call("bowtie2 --version >> {}/logs/misc_log.txt".format(idir), shell=True)
	subprocess.call("echo '-----------------' >> {}/logs/misc_log.txt".format(idir), shell=True)
	subprocess.call("perl Programs/configureHomer.pl -list >> {}/logs/misc_log.txt".format(idir), shell=True)

def main():
	parser = argparse.ArgumentParser(description='Will create project directory and subdirectories and program logfile.\n ')
	parser.add_argument('-i', '--idir', help='Name of project directory', required=False)
	if len(sys.argv)==1:
		parser.print_help()
		sys.exit(1)
	args = vars(parser.parse_args())
	create_dirs(args["idir"])
	get_logs(args["idir"])

main()