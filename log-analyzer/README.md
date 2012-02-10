SLOG ANALYZER FOR EUCALYPTUS 2.0+
=================================

We are developing an open source code that allows to analyze the log files from eucalyptus and displays the results in a convenient graphical user interface.

To achieve this we are using 'cc.log' files. Te needed information must be gathered while eucalyptus runs in 'EUCADEBUG' mode.

We assume the following directory layout

  ./futurgrid/
  ./futurgrid/bin - includes all commands needed to run the log analyzing
  ./futurgrid/lib - includes libraries that may be called from the bin files
  ./futurgrid//etc - location of configuration files

It is assumed that this tree is installed and a ahell variable 

  FG_HOME_LOG_ANALYZER  

is set to the location of the "futuregrid" directory.

We recommend that the futureGrid directory is included in the PATH of the shell that will run the commands.

INSTALATION
===========

please download the code from github with ....

  cd log-analyzer
  emacs Makefile

make changes to the location of where you like to install the scripts
e.g.

  DEPLOY_PATH=/share

  make install

This will create directories 

/share/futuregrid with its subdirectories

Do not forget to set the 

  FG_HOME_LOG_ANALYZER  


COMMANDS
========

fg-euca-log-analyzer.pl 
* Analyses the number of running instances and terminated instances are 
  collected 
* Reporting interval: hourly

fg.log.analyzer.4.eucalyptus.pl
* Analyses minutes used by users and the number of instances used by users 
* Reporting interval: daily

fg.log.merger.sh, and fg.log.gz.decompressor.sh
* mereges log files from the backup storage are restored and decompressed 

OTHER
=====
fg.crontabs.sh
* Those routine jobs are executed by crontab with 
* A snapshot is available through snapshot.of.crontab.i135

./www
* displays graphs about data usage metrics are in 'www'
* Be displaying via google chart tools.


Hyungro Lee (lee212 at indiana dot edu)
Gregor von laszewski (laszewski@gmail.com)