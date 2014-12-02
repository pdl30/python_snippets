import argparse
import csv, re, os
import xlrd

def csv_from_excel(ifile):
	out = re.sub(".xls", ".csv", ifile)
	wb = xlrd.open_workbook(ifile)
	sh = wb.sheet_by_name('Sheet1')
	your_csv_file = open(out, 'wb')
	wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)
	for rownum in xrange(sh.nrows):
		wr.writerow(sh.row_values(rownum))
	your_csv_file.close()

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Convert tsv to xls\n')
	parser.add_argument('-i','--input', help='Input', required=True)
	args = vars(parser.parse_args())
	csv_from_excel(args["input"])