slog analyzer for eucalyptus 2.0+
================================

This repository aims for collecting resource utilization information from 
log files of eucalyptus. It only looks up 'cc.log' files and a 'EUCADEBUG'
mode.

1) The number of running instances and terminated instances are collected 
by fg-euca-log-analyzer.pl
* Reporting interval: hourly

2) Minutes used by users and the number of instances used by users are 
collected by fg.log.analyzer.4.eucalyptus.pl
* Reporting interval: daily

3) log files from the backup storage are restored and decompressed and 
merged by fg.log.merger.sh, and fg.log.gz.decompressor.sh

4) Those routine jobs are executed by crontab with fg.crontabs.sh
- A snapshot is available through snapshot.of.crontab.i135

5) web pages for displaying graphs about data usage metrics are in 'www'
- Be displaying via google chart tools.

==================================
Last updated by 02/01/2012
Hyungro Lee (lee212 at indiana dot edu)
