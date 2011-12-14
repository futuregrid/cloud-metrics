#!/bin/bash
logpath="/var/log/eucalyptus/"
logfile="cc.log"
num_of_rotations=5
num_of_rotations2=5
stp=0
cnt=0
folders=(`ls`)
arrSize=${#folders[@]} #array size of "folders"

for i in `seq 0 $arrSize`
do
	num_of_rotations=5
	num_of_rotations2=5
	stp=0
	current_dir=${folders[$i]}
	next_dir=${folders[` expr $i + 1`]}
	if [ -d $current_dir ] && [ "$current_dir" != "" ]
	then
		while [ $num_of_rotations -gt 0 ] && [ $stp -eq 0 ]
		do
			current_file=$current_dir$logpath"cc.log."$num_of_rotations
			next_file=$next_dir$logpath"cc.log."$num_of_rotations2
			if [ -f $current_file ] && [ -f $next_file ]
			then
				#echo diff -q $current_file $next_file
				diff -q $current_file $next_file
				res=$?
				#echo $res
				if [ $res -eq 0 ] # files are same
				then
					# skip to next directory to combine log files
					#echo $num_of_rotations
					stp=1
					break
				elif [ "$res" = "1" ] # files are differ
				then
					stp=0 #echo #
				fi
			else
				echo "no files"
			fi
			num_of_rotations=`expr $num_of_rotations - 1`
		done
		while [ $stp -ne 0 ] && [ $num_of_rotations2 -gt $num_of_rotations ]
		do
			file_lst=$file_lst" "$current_dir$logpath"cc.log."$num_of_rotations2
			num_of_rotations2=`expr $num_of_rotations2 - 1`
			#echo $file_lst
		done
		tmp=5
		last_file_lst=""
		while [ $stp -eq 0 ] && [ $tmp -gt 0 ]
		do
			last_file_lst=$last_file_lst" "$current_dir$logpath"cc.log."$tmp
			let tmp-=1
			#echo $tmp
		done
		last_file_lst=$last_file_lst" "$current_dir$logpath"cc.log"

		if [ $cnt -eq 0 ]
		then
			start_filename=$current_dir
		else
			end_filename=$current_dir
		fi
		let cnt+=1
	fi
done

file_lst=$file_lst" "$last_file_lst
for j in $file_lst
do
	echo $j
	cat $j >> ./.tmp
done

mv ./.tmp combined_"$start_filename"."$end_filename".cc.logs

