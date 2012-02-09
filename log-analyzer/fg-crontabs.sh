#!/bin/bash
#
# fg.crontabs.sh
# ==============
#
# This is for a batch job by crontaba daily.
# Couple of scripts are executed by this script.
# 
# * Some lines should be obsolete due to security reasons

# ==========================
# Last updated by 02/01/2012
# Hyungro Lee (lee212 at indiana dot edu)
# 
sdate=$1
edate=$sdate
YESTERDAY=`date -d '1 day ago' +%Y%m%d`
if [ -z $sdate ]
then
	sdate=$YESTERDAY
	edate=$YESTERDAY
fi

# READ BIN
source log-analyzer.cfg

# 1. Collecting log backup data and generates data from the logs that make is usable via Google chart.
# cd $BIN

# a) Decompressing logs
bash $BIN/fg-log-gz-decompressor.sh -s $sdate -e $edate >> $LOG_DIR/fg-log-gz-decompressor-sh-log

# b) Merging logs
bash $BIN/fg-log-merger.sh -i logs -o $BIN/merged.logs >> $LOG_DIR/fg-log-merger.sh.log

# c) temporary step for reducing file loading burden
grep "print_ccInstance(): refresh_instances():" $LOG_DIR/merged.${sdate}*.${edate}*.cc.logs > $LOG_DIR/fined.merged.$sdate.cc.logs

# d) sym link
ln -s $LOG_DIR/fined.merged.$sdate.cc.logs cc.log

# e) log analyzer
perl $BIN/fg-log-analyzer-4-eucalyptus-pl cc.log > $DATA/user.data.of.eucalyptus.india.$sdate.$edate

# e) remove
rm -rf $EUCA_LOGOUTPUT_DIR/${sdate}*
rm -rf $LOG_DIR/merged.${sdate}*.${edate}*.cc.logs
rm -rf $LOG_DIR/fined.merged.$sdate.cc.logs
rm -rf cc.log

# f) scp

$SCP  $DATA/user.data.of.eucalyptus.india.$sdate.$edate $WEB_OUTPUT_DIR
# TODO