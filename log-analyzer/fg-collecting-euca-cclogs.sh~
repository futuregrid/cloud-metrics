#!/bin/sh
# 
# fg-collecting-euca-cclogs.sh
# ----------------------------
#
# Description
# ============================
# Once a result from log analyzer comes, the metrics from it will be reported via netlogger tools to inca.futuregrid.org
# This script will be executed by crontab hourly
#
# ============================
# Last updated by September 21th, 2011
# Hyungro Lee (lee212 at indiana dot edu)
#
HOUR=`/bin/date +%H`
HOUR=`/usr/bin/expr $HOUR - 1`
HOUR=`printf "%02d" $HOUR`
set PATH=$PATH:./
export PATH
BASEPATH=~/eloga
TMP=$BASEPATH/.collecting.cc.logs
cclogs=$BASEPATH/cc.logs

/usr/bin/find /var/log/eucalyptus/ -name "cc.log*" -mmin -60 -exec grep " $HOUR:" {} \; > $cclogs #$TMP
#/bin/cut -d":" -f2- $TMP > $cclogs

cd $BASEPATH
RES=`$BASEPATH/fg-euca-log-analyzer.pl cc.logs`

NumofTer=`echo -e "$RES"|grep Terminate|cut -d":" -f2`
NumofRun=`echo -e "$RES"|grep RunInstance|cut -d":" -f2`

cd NetloggerAmqpJava/

java -cp .:netlogger-java-trunk.jar:rabbitmq-client.jar:commons-io-1.2.jar NetloggerAmqpJava fgtest.india.terminate $NumofTer
echo "java -cp .:netlogger-java-trunk.jar:rabbitmq-client.jar:commons-io-1.2.jar NetloggerAmqpJava fgtest.india.terminate $NumofTer"
java -cp .:netlogger-java-trunk.jar:rabbitmq-client.jar:commons-io-1.2.jar NetloggerAmqpJava fgtest.india.run $NumofRun
echo "java -cp .:netlogger-java-trunk.jar:rabbitmq-client.jar:commons-io-1.2.jar NetloggerAmqpJava fgtest.india.run $NumofRun"

cd $BASEPATH

rm -f $TMP
rm -f $cclogs
