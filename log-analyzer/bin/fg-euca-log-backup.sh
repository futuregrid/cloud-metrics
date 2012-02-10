#TOD
# euca log snapshot
#10        12        *        *        *        /root/bin/euca_log.sh
#10        20        *        *        *        /root/bin/euca_log.sh
*         *        *        *        *        /root/bin/euca_log.sh

The default folder is /var/log/eucalyptus.

___________SCRIPT___________
#! /bin/bash
#This compresses up /var/log/eucalyptus
mkdir -p /var/log/eucalyptus/logbackup/`date +%Y%m%d%H%S`
tar -czf /var/log/eucalyptus/logbackup/`date +%Y%m%d%H%S`/cclog.tar.gz /var/log/eucalyptus/cc.log*
#echo Backup Completed `date`
___________SCRIPT___________