#!/usr/bin/python

########################################################################
# 09 Oct 2014
# Patrick Lombard, Centre for Stem Research
# Core Bioinformatics Group
# University of Cambridge
# All right reserved.
########################################################################

import os, re, sys
import argparse
import subprocess
import ConfigParser
import MySQLdb as mdb
import re
from string import replace

def get_gsms(user, passwd, gse=False, gsm_list=False):
	con = mdb.connect(host="tobias.cscr.cam.ac.uk",port=3306,user=user,passwd=passwd,db="bioinformatics")
	gsms = {}
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		if gse:
			query = "SELECT GSM, filename FROM codex WHERE GSE='{}';".format(gse)
			cur.execute(query)
			rows = cur.fetchall()
			for row in rows:
				gsms[row["GSM"]] = row["filename"]
		elif gsm_list:
			for gsm in gsm_list:
				query = "SELECT filename FROM codex WHERE GSM='{}';".format(gsm)
				cur.execute(query)
				rows = cur.fetchall()
				for row in rows:
					gsms[gsm] = row["filename"]
	return gsms

def download_gsms(gsm_dict, codex_path, d_all=False):
	for gsm in sorted(gsm_dict):
		if d_all:
			command = "scp pdl30@tobias.cscr.cam.ac.uk:/raid/websites/codex.stemcells.cam.ac.uk/data/fq/mm10/{}.fq.gz .".format(gsm_dict[gsm])
			subprocess.call(command.split())
			command = "scp pdl30@tobias.cscr.cam.ac.uk:/raid/websites/codex.stemcells.cam.ac.uk/data/BED/mm10/{}.BED.gz .".format(gsm_dict[gsm])
			subprocess.call(command.split())
			command = "scp pdl30@tobias.cscr.cam.ac.uk:/raid/websites/codex.stemcells.cam.ac.uk/data/bed/mm10/{}.bed .".format(gsm_dict[gsm])
			subprocess.call(command.split())
			command = "scp pdl30@tobias.cscr.cam.ac.uk:/raid/websites/codex.stemcells.cam.ac.uk/data/fastqc/mm10/{}_fastqc.zip .".format(gsm_dict[gsm])
			subprocess.call(command.split())
		command = "scp pdl30@tobias.cscr.cam.ac.uk:/raid/websites/codex.stemcells.cam.ac.uk/data/bw/mm10/{}.bw .".format(gsm_dict[gsm])
		subprocess.call(command.split())
		command = "scp pdl30@tobias.cscr.cam.ac.uk:/raid/websites/codex.stemcells.cam.ac.uk/data/bb/mm10/{}.bb .".format(gsm_dict[gsm])
		subprocess.call(command.split())

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

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Downloads samples from CODEX\n')

	parser.add_argument('-g', '--gse', help='GEO accession number', required=False )
	parser.add_argument('-m', '--gsm', help='GSM accession', required=False, nargs='+' )
	parser.add_argument('-c', '--config', help='Contains [Config] section with user and pass', required=False )
	parser.add_argument('-a', action='store_true', help='Download all files', required=False )
	if len(sys.argv)==1:
		parser.print_help()
		sys.exit(1)
	args = vars(parser.parse_args())

	Config = ConfigParser.ConfigParser()
	Config.optionxform = str
	Config.read(args["config"])
	configs = ConfigSectionMap("Config", Config)
	codex_path = "/raid/websites/codex.stemcells.cam.ac.uk/data/"
	if args["gse"]:
		gsm_dict = get_gsms(configs["user"], configs["pass"], gse=args["gse"])
	else:
		gsm_dict = get_gsms(configs["user"], configs["pass"], gsm_list = args["gsm"])
	download_gsms(gsm_dict, codex_path, args["a"])

    