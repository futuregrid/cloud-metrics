#!/bin/bash
#
# Hyungro Lee (lee212 at indiana dot edu)

BASEPATH=~/eloga
export PATH=$PATH:$BASEPATH
cclogs=$BASEPATH/cc.2.logs
elogpath=/var/log/eucalyptus/

#variables for gcharge 
# gcharge - charge command for Gold accounting
#ex> gcharge -J test3 -p fg -u lee212 -m localhost -P 2 -t 11 -X WallDuration=1 -X StartTime=1315924212 -X EndTime=1315924213
PRJ_NAME="fg"
PRC_NUM=1

# option -t (time period to retrieve)
if [ $# -ge 2 ] && [ "$1" == "-t" ]
then 
	Hrs=$2
	Mns=`expr 60 \* $Hrs`
else 
	Hrs=1
	Mns=60
fi
# option -f (specific log filename)
if [ $# -ge 2 ] && [ "$1" == "-f" ]
then
	cclogs=$2
	nodelete=1
else
	# Gathering logs last 60 mins from /var/log/eucalyptus (default log directory)
	HOUR=`/bin/date +%H` 			# current hour
	HOUR=`/usr/bin/expr $HOUR - $Hrs`	# last hour
	HOUR=`printf "%02d" $HOUR`		# make it 2 digits e.g. 9 -> 09
	/usr/bin/find $elogpath -name "cc.log*" -mmin -$Mns -exec grep " $HOUR:" {} \; > $cclogs
	cd $BASEPATH
fi

# print_ccInstance has information of VM's termination in cc.log
#
# ex> [Tue Sep 13 10:59:24 2011][008774][EUCADEBUG ] print_ccInstance(): refresh_instances():  instanceId=i-38F0078D reservationId=r-4E010956 emiId=emi-F3E41594 kernelId=eki-78EF12D2 ramdiskId=eri-5BB61255 emiURL=http://149.165.146.135:8773/services/Walrus/ajyounge/ubuntu-lucid-twister-0.9.img.manifest.xml kernelURL=http://149.165.146.135:8773/services/Walrus/xenkernel/vmlinuz-2.6.27.21-0.1-xen.manifest.xml ramdiskURL=http://149.165.146.135:8773/services/Walrus/xeninitrd/initrd-2.6.27.21-0.1-xen.manifest.xml state=Teardown ts=1315924212 ownerId=steenoven keyName=ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDFTX2d0XynEUaBJWE4KfHMcxKN5ODYOOJH1Vi3SYvXtBu8+Yxq/gUxRbqxEK3S7Pxw2xtMaKkzWsjW3Q/6VIBky/N3AeTD1w4QyqeKndNbGl7K4q1PUVbpSO5YY0lTT6C8fYiEjh6HLBrbIcTMLMJq4TG7KmIoH7LSYXvpDSEKPNo12UExhXvjNj/q0qYH8i2pbE5vijo2ijre5Jw8tv7Im1E2yxIefGMJr99uAvq1pro2tKN9FfjfJF9yUQPvncm2opYr6tf6waHj2AjC6wyCpPgt5qNbBKi6Rq8mLT+bC8o0hD3Tr4J9EPEQ8MyZtVmxfPzEv6WqWNNnqnKDz70H steenoven@eucalyptus ccnet={privateIp=10.0.2.195 publicIp=0.0.0.0 privateMac=D0:0D:38:F0:07:8D vlan=13 networkIndex=3} ccvm={cores=1 mem=1024 disk=7} ncHostIdx=21 serviceTag=http://i4:8775/axis2/services/EucalyptusNC userData= launchIndex=0 volumesSize=0 volumes={} groupNames={default }
#
# Once a VM instance terminated, print_ccInstance leaves information such as instanceId, emiId, state, ts (running start time), and ownerId that gcharge needs.
# 1. print_ccInstance is the function that I am looking for in cc.log
# 2. "state=Teardown" indicates a VM is terminated. Otherwise, state=Extant means it's running.
# 3. instanceId & ts & ownerId is going to be a key to charge usage of a VM instance.
# 4. ts is a running start time of a specific VM in the type of unixtimestamp and I ASSUME the log time stamp (e.g. [Tue Sep 13 10:59:24 2011]) is a end time of the VM.
# 4.1. So I convert Date to unixtimestamp
# 4.2. and calculate the difference by expr
# 5. Make a command to call Gold accounting manager
# 6. print_ccInstance repeats to print the information several times since VMs terminated while about 6 minutes. So, I picked the first line of print_ccInstance to charge for it. (this is about sort does)
#

RES=`grep print_ccInstance $cclogs|\
grep Teardown|\
awk -F "[][ =]+" ' { if ($11 == "instanceId" && $29 == "ts" && $31 == "ownerId")\
("date --date=\""$2" "$3" "$4" "$5" "$6"\" +%s")|getline e_time 
("expr "e_time" - "$30"")|getline charge_duration 
{print "gcharge -J", $12, "-p '$PRJ_NAME' -u", $32, "-m", $16, "-P '$PRC_NUM' -t", charge_duration, "-X WallDuration="charge_duration, "-X StartTime="$30, "-X EndTime="e_time } }'|\
sort -k 3,9 -u`


# et cetera
# 1013 Tue Sep 13 10:27:16 2011 instanceId i-3BA6076F emiId emi-F3E41594 ts 1315923023 ownerId steenoven \
#{print charge_duration, $2, $3, $4, $5, $6, $16, $17, $20, $21, $34, $35, $36, $37} }'\
#{print "gcharge -J", $17, "-p '$PRJ_NAME' -u", $37, "-m", $21, "-P '$PRC_NUM' -t", charge_duration, "-X WallDuration="charge_duration } }'\
#{print "gcharge -J", $7, "-p '$PRJ_NAME' -u", $13, "-m", $9, "-P '$PRC_NUM' -t", charge_duration, "-X WallDuration="charge_duration } }'`

if [ "$RES" != "" ] 
then
	printf "$RES\n"
fi

cd $BASEPATH

if [ $nodelete -ne 1 ]
then
	rm -f $cclogs
fi
