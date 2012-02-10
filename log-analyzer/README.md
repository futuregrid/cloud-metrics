SLOG ANALYZER FOR EUCALYPTUS 2.0+
=================================

We are developing an open source code that allows to analyze the log files from eucalyptus and displays the results in a convenient graphical user interface.

To achieve this we are using 'cc.log' files. Te needed information must be gathered while eucalyptus runs in 'EUCADEBUG' mode.

We assume the following directory layout

  ./futurgrid/
  ./futurgrid/bin - includes all commands needed to run the log analyzing
  ./futurgrid/lib - includes libraries that may be called from the bin files
  ./futurgrid/etc - location of configuration files
  ./futurgrid/www - location of the www files

TODO: create a make install that installs the package into /.../futuregrid

The scripts generate the folloing output files

#TODO: clean the variables

    FG_LOG_ANALYZER_WWW_OUTPUT - location wher ethe www files for dispaly are stored
    FG_TMP - location where temporary files are located that are analyzed
    FG_DATA - location where the permamnent data is being stored 

The scripts assume the following input files

    EUCALYPTUS_LOG_DIR - location wher the eucalyptus log dirs are stored


It is assumed that this tree is installed and a ahell variable 

#TODO:
  FG_HOME_LOG_ANALYZER  

is set to the location of the "futuregrid" directory.

We recommend that the futureGrid directory is included in the PATH of the shell that will run the commands.

INSTALATION
===========

please download the code/egg from github with ....

make distall
make install

This will install the programs in 

/usr/bin/*

#TODO:
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

CONTRIBUTORS
============
Hyungro Lee (lee212 at indiana dot edu)
Gregor von laszewski (laszewski@gmail.com)

KNOWN BUGS
==========
* we like to move to a python script at one point
* we like to move to a python egg with easy_install
