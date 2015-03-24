#!/usr/bin/python

########################################################################
# 28 Apr 2014
# Patrick Lombard, Centre for Stem Stem Research
# Core Bioinformatics Group
# University of Cambridge
# All right reserved.
########################################################################

import csv, re
import argparse
from xlsxwriter.workbook import Workbook

def convert_tsv_xls(tsv):
	name = tsv.strip(".tsv$")
	workbook = Workbook(name+".xls")
	worksheet = workbook.add_worksheet()
	tsv_reader = csv.reader(open(tsv, 'rb'), delimiter='\t')
	for row, data in enumerate(tsv_reader):
		worksheet.write_row(row, 0, data)
	workbook.close()

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Convert tsv to xls\n')
	parser.add_argument('-i','--input', help='Input', required=True)
	args = vars(parser.parse_args())
	convert_tsv_xls(args["input"])
