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

def generate_htaccess(path, user, password):
	output = open(".htaccess", "w")
	output.write("AuthType Basic\nAuthName \"restricted area\"\nAuthUserFile {}/.htpasswd\nrequire valid-user\n".format(path)),
	output.close()
	command = "htpasswd -c -b .htpasswd {} {}".format(user, password)
	subprocess.call(command.split())

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Generates htaccess\n')
	parser.add_argument('-user', help='username', required=True)
	parser.add_argument('-pass', help='password', required=True)
	args = vars(parser.parse_args())
	path = os.getcwd()
	generate_htaccess(path, args["user"], args["pass"])