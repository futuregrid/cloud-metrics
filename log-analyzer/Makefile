LIB=~/etc/lib
BIN=~/usr/bin

all:
	cp crontab.template euca-log-analyzer.crontab
	perl -p -i -e 's/LIB/$(LIB)/g'  *.euca-log-analyzer.crontab
	perl -p -i -e 's/LIB/$(BIN)/g'  *.euca-log-analyzer.crontab
	cat euca-log-analyzer.crontab

#
