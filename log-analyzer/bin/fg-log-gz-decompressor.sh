#!/bin/bash

# fg.log.gz.decompressor.sh
# =========================
#
# log decompressor from backup log files
# This is basically to run 'tar'
#
# =========================
# Last updated by 01/26/2012
# Hyungro Lee (lee212 at indiana dot edu)

source fg-log-analyzer-lib.sh 

# Read from log-analyzer.cfg
#
# EUCA_LOGINPUT_DIR= ...
# EUCA_LOGOUTPUT_DIR= ...
#
source log-analyzer.cfg
#

LIST=`ls $EUCA_LOGINPUT_DIR`


while getopts "s:e:" opt;
do
	case $opt in
	s) s_date=$OPTARG;;
	e) e_date=$OPTARG;;
	\?) echo invalid options $@;
		echo "ex) $0 -s start date (20120115) -e end date (20120123)"
		exit 1;;
	esac
done

if [ ! -z $s_date ] && [ ! -z $e_date ] 
then
	if ( ! is_integer $s_date ) || ( ! is_integer $e_date )
	then
		echo "$s_date, $e_date are not valid for date type (YYYYMMDD)."
		exit 1;
	fi

	s_year=`echo $s_date|cut -c -4`
	s_month=`echo $s_date|cut -c 5-6`
	s_day=`echo $s_date|cut -c 7-8`
	e_year=`echo $e_date|cut -c -4`
	e_month=`echo $e_date|cut -c 5-6`
	e_day=`echo $e_date|cut -c 7-8`
else
	# Put yesterday
	s_year=`date -d '1 day ago' +%Y`
	s_month=`date -d '1 day ago' +%m`
	s_day=`date -d '1 day ago' +%d`
	e_year=$s_year
	e_month=$s_month
	e_day=$s_day
fi

for i in $LIST
do
	year=`echo $i|cut -c -4`
	month=`echo $i|cut -c 5-6`
	day=`echo $i|cut -c 7-8`
	hour=`echo $i|cut -c 9-10`

	if ( ! is_integer $year ) || ( ! is_integer $month ) || ( ! is_integer $day ) || ( ! is_integer $hour )
	then
		echo no valid folder/file name "$i"
		continue
	fi

	if [ "$year$month$day" -lt "$s_year$s_month$s_day" ]
	then
		#echo "Start date is $s_year/$s_month/$s_day, $year/$month/$day will be skipped"
		continue
	fi
	if [ "$year$month$day" -gt "$e_year$e_month$e_day" ]
	then
		#echo "End date is $e_year/$e_month/$e_day, $year/$month/$day will be skipped"
		continue
	fi

	echo "[$i] [$year/$month/$day $hour]"

	dest=$EUCA_LOGOUTPUT_DIR/$i
	mkdir -p $dest
	echo mkdir -p $dest

	compressed_file=$EUCA_LOGINPUT_DIR/$i/cclog.tar.gz

	tar xvzf $compressed_file -C $dest
	echo tar xvzf $compressed_file -C $dest

done
