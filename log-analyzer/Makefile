LOG=gregor\/etc\/lib
BIN=gregor\/usr\/bin

all:
	cp crontab.template euca-log-analyzer.crontab
	perl -p -i -e 's/LOG/${LOG}/g'  euca-log-analyzer.crontab
	perl -p -i -e 's/BIN/${BIN}/g'  euca-log-analyzer.crontab
	cat euca-log-analyzer.crontab

clean:
	rm -f euca-log-analyzer.crontab *~
#
