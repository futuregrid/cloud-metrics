#!/usr/bin/env python

"""
MANUAL PAGE DRAFT

NAME - fg-cleanup-table

DESCRIPTION

usagea
	fg-cleanup-table <arguments>

fg-cleanup-table

	-t tbl_name
	   deletes rows from tbl_name

	-d db_name
	   a database name of a table specified by -t tbl_name

	-w where_condition (optional)
	   specifies the conditions that identify which rows to delete

	--conf filename
	   configuraton file of the database to be used. The configuration file has the following format
	   
	   [EucaLogDB]
	   host=HOST
	   port=PORT
	   user=USER
	   passwd=PASS
	   db=DB
	   
	   if this parameter is not specified and a database is used the default location for this file is in
	   
	   ~/.futuregrid/futuregrid.cfg

"""

import ConfigParser
from lib import FGEucaMetricsDB
import argparse

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-t", dest="table_name", required=True,
			help="table name to delete")
	parser.add_argument("-d", dest="db_name", required=True,
			help="db name")
	parser.add_argument("-w", dest="where_clause",
			help="WHERE clauses")
	args = parser.parse_args()

	eucadb = FGEucaMetricsDB("futuregrid.cfg.local") 
	eucadb.change_table(args.table_name)

	# where_clause need to be query dict type 
	query_dict=""
	ret = eucadb.delete(query_dict)

if __name__ == '__main__':
	main()
