#!/bin/bash

# fg.log.merger.sh
# ================
#
# Description
# - This Bash shell script reads directories that have backup log files and combines multiple log files by removing duplicated lines.
#
# Input
# - N/A (current directory)
#
# Output
# - Combined log files
#
# Structure of backup log files
# - YYYYMMDDhhmm (directory name)
#   - cclog.tar.gz (compressed file)
#   - var/log/eucalyptus/
#     - cc.log (normally it has seven files with a sequential numbers)
#     - cc.log.0
#     - cc.log.1
#     - cc.log.2
#     - cc.log.3
#     - cc.log.4
#     - cc.log.5
#
# Written by
# Hyungro Lee (lee212 at indiana dot edu)
#
# Updates
#
# 01/23/2012 
# 1) Description added
# 2) Input / output added
#
########################################################################

logpath="/var/log/eucalyptus/"
logfile="cc.log"
compressed_filename="cclog.tar.gz"
temp_file="./.tmp"
cnt=0

while getopts "i:o:" opt;
do
	case "$opt" in
		i) input_dir=$OPTARG;;
		o) output_dir=$OPTARG;;
		\?)		# unknown flag
			echo >&2 \
			"usage: $0 [-i input directory] [-o output directory]"
			exit 1;;
	esac
done

if [ -d $input_dir ]
then
	input_dir=`echo "$( readlink -f "$( dirname "$input_dir" )" )/$( basename "$input_dir" )"`
else
	input_dir="output"
fi

if [ -d $output_dir ]
then
	output_dir=`echo "$( readlink -f "$( dirname "$output_dir" )" )/$( basename "$output_dir" )"`
else
	output_dir="."
fi

# 1. Read folders
# Folder should be listed in a chronological order
folders=(`ls $input_dir`)
arrSize=${#folders[@]} #array size of "folders"
end_i=`expr $arrSize - 1`

# 2. Iteration for all $folders
for i in `seq 0 $arrSize`
do
	current_ext=5
	end_ext=5
	match_YN=0
	last_file_YN=0

	current_dir=$input_dir/${folders[$i]}
	next_dir=$input_dir/${folders[` expr $i + 1 `]}
	current_file=$current_dir$logpath"cc.log."$current_ext
	oldest_file=$next_dir$logpath"cc.log."$end_ext

	# There could be some missing files, directories.
	if [ ! -f $current_file ]
	then
		echo Invalid current [$current_file]
		continue;
	fi
	if [ ! -f $oldest_file ] && [ $i -lt $end_i ]
	then
		tmp_cnt=0
		echo Invalid oldest [$oldest_file]
		while [ ! -f $oldest_file ]
		do
			let tmp_cnt+=1
			n_d=${folders[` expr $i + $tmp_cnt `]}
			next_dir=$input_dir/$n_d
			oldest_file=$next_dir$logpath"cc.log."$end_ext
			echo New $oldest_file could be valid
			if [ -z $n_d ]
			then
				#No more valid next_dir, will stop finding next level of backup logs. Will merge logs with current stacks
				echo There is no valid next_dir, will stop finding oldest_file. Current stack files will only be used.
				last_file_YN=1
				break;
			fi
		done
	fi

	if [ $i -eq $end_i ]
	then
		last_file_YN=1
	fi

	if [ -d $current_dir ] && [ "$current_dir" != "" ]
	then
		while [ $current_ext -gt 0 ] && [ $match_YN -eq 0 ]
		do
			current_file=$current_dir$logpath"cc.log."$current_ext

			if [ -f $current_file ] && [ -f $oldest_file ]
			then
				# If files are same between one in the current dir ($current_file) and the other in the next dir ($oldest_file)
				# It means, we can ignore one of the files which duplicated.
				# * All log files with different ending numbers are connected with previous one.
				# - It only seperates due to a size limit.
				diff -q $current_file $oldest_file
				res=$?
				if [ $res -eq 0 ] # files are same
				then
					# skip to next file to combine log files
					match_YN=1
					break # It will break only in this 'while' iteration range
				elif [ "$res" = "1" ] # files are differ then DO merge it.
				then
					match_YN=0
				fi
			else
				echo "no current or next files ($current_file, $oldest_file)"
			fi

			current_ext=`expr $current_ext - 1`
		done

		tmp_cnt=5
		# If the files are same and older than current extension log files will be stacked up.
		# ex) if current_ext = 3 that means .log.4, and .log.5 should be stacked up because .log.3 and .log.5 (in next directory) are same
		# $file_lst will have '...log.4 ...log.5' with a white space separator
		while [ $match_YN -eq 1 ] && [ $tmp_cnt -gt $current_ext ]
		do
			file_lst=$file_lst" "$current_dir$logpath"cc.log."$tmp_cnt
			let tmp_cnt-=1
		done

		tmp_cnt=5
		last_file_lst=""

		# Will count last directory with cc.log file
		while [ $match_YN -eq 0 ] && [ $last_file_YN -eq 1 ] && [ $tmp_cnt -gt 0 ]
		do
			last_file_lst=$last_file_lst" "$current_dir$logpath"cc.log."$tmp_cnt
			let tmp_cnt-=1
		done

		last_file_lst=$last_file_lst" "$current_dir$logpath"cc.log"

		let cnt+=1
	fi
done

file_lst=$file_lst" "$last_file_lst
for j in $file_lst
do
	echo $j
	cat $j >> $temp_file
done

start_dir=${folders[0]}
end_dir=${folders[$end_i]}

if [ -f $temp_file ]
then
	if [ ! -d $output_dir ]
	then
		mkdir $output_dir
	fi
	mv $temp_file $output_dir/merged."$start_dir"."$end_dir".cc.logs
fi
