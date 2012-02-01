#!/bin/bash

sdate=$1
edate=$sdate
YESTERDAY=`date -d '1 day ago' +%Y%m%d`
if [ -z $sdate ]
then
	sdate=$YESTERDAY
	edate=$YESTERDAY
fi

# 1. Collecting log backup data and generates data from the logs that make is usable via Google chart.
cd ~/eloga/logbackup

# a) Decompressing logs
bash fg.log.gz.decompressor.sh -s $sdate -e $edate >> scripts.logs/fg.log.gz.decompressor.sh.log

# b) Merging logs
bash fg.log.merger.sh -i logs -o merged.logs >> scripts.logs/fg.log.merger.sh.log

# c) temporary step for reducing file loading burden
grep "print_ccInstance(): refresh_instances():" merged.logs/merged.${sdate}*.${edate}*.cc.logs > merged.logs/fined.merged.$sdate.cc.logs

# d) sym link
ln -s merged.logs/fined.merged.$sdate.cc.logs cc.log

# e) log analyzer
perl fg.log.analyzer.4.eucalyptus.pl cc.log > data4graphs/user.data.of.eucalyptus.india.$sdate.$edate

# e) remove
rm -rf logs/${sdate}*
rm -rf merged.logs/merged.${sdate}*.${edate}*.cc.logs
rm -rf merged.logs/fined.merged.$sdate.cc.logs
rm -rf cc.log

# f) scp
scp -i ~/.ssh/.india2hyungro data4graphs/user.data.of.eucalyptus.india.$sdate.$edate hyungro@129.79.49.76:fg/accounting/eucalyptus/data4graphs/
