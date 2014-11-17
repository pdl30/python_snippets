import xlrd
import csv
import sys
import re

def csv_from_excel(input):
	out = re.sub(".xls", ".csv", input)
	wb = xlrd.open_workbook(input)
	sh = wb.sheet_by_name('Sheet1')
	your_csv_file = open(out, 'wb')
	wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)
	for rownum in xrange(sh.nrows):
		wr.writerow(sh.row_values(rownum))
	your_csv_file.close()

if __name__ == "__main__":
	xls = sys.argv[1]
	csv_from_excel(xls)