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


# Read 
# BIN = ...
source log-analyzer.cfg


TMP=$BIN/.collecting.cc.logs
cclogs=$BIN/cc.logs

$FIND_SH $EUCA_LOG_DIR -name "cc.log*" -mmin -60 -exec grep " $HOUR:" {} \; > $cclogs #$TMP
#/bin/cut -d":" -f2- $TMP > $cclogs

cd $BIN
RES=`$BIN/fg-euca-log-analyzer.pl cc.logs`

NumofTer=`echo -e "$RES"|grep Terminate|cut -d":" -f2`
NumofRun=`echo -e "$RES"|grep RunInstance|cut -d":" -f2`

cd NetloggerAmqpJava/

$NETLOGGER fgtest.india.terminate $NumofTer
echo "$NETLOGGER fgtest.india.terminate $NumofTer"
$NETLOGGER NetloggerAmqpJava fgtest.india.run $NumofRun
echo "$NETLOGGER fgtest.india.run $NumofRun"

cd $BIN

rm -f $TMP
rm -f $cclogs
