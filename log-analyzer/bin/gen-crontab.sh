#! /bin/bash

#
# LOG = ...
# BIN = ...
#
source log-analyzer.cfg
#


cp $BIN/crontab.template euca-log-analyzer.crontab
perl -p -i -e 's/LOG/${LOG}/g'  euca-log-analyzer.crontab
perl -p -i -e 's/BIN/${BIN}/g'  euca-log-analyzer.crontab
cat euca-log-analyzer.crontab

#
