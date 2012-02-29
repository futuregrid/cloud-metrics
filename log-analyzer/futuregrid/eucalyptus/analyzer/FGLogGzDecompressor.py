'''
fg-log-gz-decompressor.py
=========================

This script is decompressing cc.log.tar.gz files under /var/log/eucalyptus/logbackup/YYYYMMDDhhmmss/

Usage
-----
fg-log-gz-decompressor.py [arguments] [options]

Arguments
---------
-s: start date
-e: end date
-o: output directory

*All arguments are required*

Options
-------
-i: input directory (default: /var/log/eucalyptus/logbackup)

Example
-------
./fg-log-gz-decompressor.py -s 20120216 -e 20120216 -o /var/log/eucalyptus/BACKUP

Contact
=========================
Hyungro Lee (lee212 at indiana dot edu)
'''

import argparse
from datetime import datetime, time
import sys

def CheckDate(str):
	'''Checks a date if it is in a valid format'''
	try:
		d = datetime.strptime(str, "%Y%m%d")
		return True
	except:
		return False

def main():
	# Set variables
	# -------------
	default_input_dir="/var/log/eucalyptus/logbackup"
	compressed_file="cclog.tar.gz"
	# 1. Set default argument values
	# 1.1. date
	# ---------
	from datetime import date
	today = date.today()
	def_s_date = today.strftime("%Y%m%d")
	def_e_date = def_s_date
	# 1.2. output directory
	def_output_dir = "/tmp/uncompressed-euca-logbackup/"


	# Parse arguments
	# ---------------
	parser = argparse.ArgumentParser()
	parser.add_argument("-s", dest="s_date", default=def_s_date,
		help="start date to begin decompression (type: YYYYMMDD)")
	parser.add_argument("-e", dest="e_date", default=def_e_date,
		help="end date to finish decompression (type: YYYYMMDD)")
	parser.add_argument("-i", dest="input_dir", default=default_input_dir,
		help="Absolute path where compressed .tar.gz files exist")
	parser.add_argument("-o", dest="output_dir", default=def_output_dir,
		help="Absolute path where decompressed files to be saved")
    
	args = parser.parse_args()
	#print args.s_date, args.e_date, args.input_dir, args.output_dir

	# Validate arguments
	# ------------------
	if not CheckDate(args.s_date) or not CheckDate(args.e_date):
		print "input dates is(are) invalid!"
		sys.exit(-1)

	# Set variables
	s_date = datetime.strptime(args.s_date, "%Y%m%d")
	e_date = datetime.strptime(args.e_date, "%Y%m%d")
	e_date = datetime.combine(e_date,time(23, 59, 59))

	# Read input directory
	import os
	list = os.listdir(args.input_dir)
	for infile in list:
		if not CheckDate(infile[0:8]):
			continue;
		dir_date = datetime.strptime(infile, "%Y%m%d%H%M")
		if dir_date < s_date:
			continue
		if dir_date > e_date:
			continue
		#print s_date, e_date, dir_date

		# Extract .tar.gz log files
		import tarfile
		print "Extracting... "+infile+"/"+compressed_file+" to "+args.output_dir+"/"+infile+"/..."
		tar = tarfile.open(args.input_dir+"/"+infile+"/"+compressed_file, "r:gz")
		if not os.path.exists(args.output_dir):
			os.makedirs(args.output_dir)
		tar.extractall(args.output_dir+"/"+infile)

		
if __name__ == '__main__':
	main()
