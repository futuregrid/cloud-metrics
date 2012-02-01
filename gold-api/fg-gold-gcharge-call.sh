#!/bin/bash
#
# Hyungro Lee (lee212 at indiana dot edu)

BASEPATH=~/eloga
export PATH=$PATH:$BASEPATH
SSH_SET="ssh -i $HOME/.ssh/.india2hr-gold gold@129.79.49.76"

_DEBUG=1
function DEBUG()
{
 [ $_DEBUG -eq 1 ] &&  $@
}

#variables for gold's command
PRJ_NAME=fg #default

RES=`fg-chargedata-from-euca-cclog.sh`
#TEST
#RES="gcharge -J i-43060801 -p fg -u hrlee -m emi-308A11D6 -P 1 -t 642 -X WallDuration=642
#gcharge -J i-4D0908BA -p fg -u hrlee2 -m emi-D778156D -P 1 -t 77261 -X WallDuration=77261 -X StartTime=1315866745 -X EndTime=1315944006
#gcharge -J i-4D0908BA -p fg -u hrlee3 -m emi-D778156D -P 1 -t 77261 -X WallDuration=77261 -X StartTime=1315866745 -X EndTime=1315944006"

function ssh_c()
{
	cmd=$@
	DEBUG echo "$SSH_SET \"source .bash_profile;$cmd\""
	$SSH_SET "source .bash_profile;$cmd"
}

TEMP=$BASEPATH/.gcharge.log
echo "$RES" > $TEMP
exec 9< $TEMP
skip_read=0

while true
do
	res=0
	if [ $skip_read -eq 0 ]
	then
		read -u9 "line"
		res=$?
		DEBUG echo $line
	fi
	if [ $res -ne 0 ]
	then
		break
	fi

	# Call gcharge 
	DEBUG echo "$SSH_SET \"source .bash_profile;$line\""
	RES2=`$SSH_SET "source .bash_profile;$line"`
	RET_CODE=$?

	# Success
	if [ $RET_CODE -eq 0 ]
	then
		#success
		# LOG
		echo "[SUCC][$RET_CODE][$RES2]$line"
		skip_read=0

	elif [ $RET_CODE -eq 74 ]
	then
		#user doesn't exist
		if [ "${RES2:0:4}" == "User" ]
		then	
			echo "[ERR][$RET_CODE][$RES2]$line"

			#Temporarily, I create a user account in Gold and specify the project name is "fg".
			# gmkuser -n "Wilkes, Amy" -E "amy@western.edu" amy
			user_name=`echo $line|awk ' { print $7 }'`
			DEBUG echo "$SSH_SET \"source .bash_profile;gmkuser -p $PRJ_NAME $user_name\""
			RES3=`$SSH_SET "source .bash_profile;gmkuser -p $PRJ_NAME $user_name"`
			
			# Call gcharge again
			skip_read=1
		
		#Machine doesn't exist
		elif [ "${RES2:0:7}" == "Machine" ]
		then
			echo "[ERR][$RET_CODE][$RES2]$line"
			
			#Temporarily, I create a machine in Gold.
			#gmkmachine -d "Linux Cluster" colony
			machine_name=`echo $line|awk ' { print $9 }'`
			DEBUG echo "$SSH_SET \"source .bash_profile;gmkmachine $machine_name\""
			RES3=`$SSH_SET "source .bash_profile;gmkmachine $machine_name"`

			# Call gcharge again
			skip_read=1
		fi
	fi

done

rm -f $TEMP
