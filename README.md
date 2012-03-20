<<<<<<< HEAD
LOG ANALYZER FOR CLOUDS v2.1
============================

FEATURE REQUESTS
================

This project is under active development. In order for us to identify
priorities please let us know what features you like us to add.  We
will than include a list here and identify based on resources and
priorities how to integrate them.

JOINING THE TEAM AND CONTRIBUTIONS
==================================

Uf you like to join the development efforts, please e-mail us. We can
than discuss how best you can contribute. You may have enhenced our
code already or used it in your system. If so, please let us know.

CONTACT
=======

send mail to laszewski@gmail.com

INTRODUCTION
============

We are developing an open source code that allows to analyze the log
files from eucalyptus and displays the results in a convenient
graphical user interface.


Shell to analyze data
---------------------

Our framework is build around analyzing some data from various
production clouds and uploading this data into a database.  We have
several mechanisms to deal with the data. First we can create summary
data that we can export in a variety of formats. This includes png,
googlecharts, and cvs tables. Second, we provide a simpel php
framework that displayse the information in some web pages.

However, as part of our analyzis we are also developing an interactive
shell that can be used to query data directly from our database.

In the source code we included som simple example so you can test this
interface out. However it requires hat you have set up the database.

The following will create a table with data produced for the month of January

> fg-metric
fg> clear users
fg> analyze -M 01
fg> table --type users --seperator ,  --caption Testing_the_csv_table
fg> quit

Naturally you could store this script in a file and pipe to fg-metric
in case you have more complex analysis to do. 


Eucalyptus Integration
----------------------

To achieve analysiz of eucalyptus data we are using 'cc.log'
files. The needed information must be gathered while eucalyptus runs
in 'EUCADEBUG' mode.
=======
LOG ANALYZER FOR EUCALYPTUS 2.0+
================================

We are developing an open source code that allows to analyze the log files from eucalyptus and displays the results in a convenient graphical user interface.

To achieve this we are using 'cc.log' files. The needed information must be gathered while eucalyptus runs in 'EUCADEBUG' mode.
>>>>>>> new_www

We assume the following directory layout

  ./futurgrid/
  ./futurgrid/bin - includes all commands needed to run the log analyzing
  ./futurgrid/lib - includes libraries that may be called from the bin files
  ./futurgrid/etc - location of configuration files
  ./futurgrid/www - location of the www files

TODO: create a make install that installs the package into /.../futuregrid

The scripts generate the folloing output files

#TODO: clean the variables

    FG_LOG_ANALYZER_WWW_OUTPUT - location where the www files for display are stored
    FG_TMP - location where temporary files are located that are analyzed
    FG_DATA - location where the permamnent data is being stored 

The scripts assume the following input files

    EUCALYPTUS_LOG_DIR - location where the eucalyptus log dirs are stored


It is assumed that this tree is installed and a shell variable 

#TODO:
  FG_HOME_LOG_ANALYZER  

is set to the location of the "futuregrid" directory.

<<<<<<< HEAD
We recommend that the futureGrid directory is included in the PATH of
the shell that will run the commands.
=======
We recommend that the futureGrid directory is included in the PATH of the shell that will run the commands.
>>>>>>> new_www

INSTALLATION
===========

please download the code/egg from github with ....

<<<<<<< HEAD
make force
=======
make distall
make install
>>>>>>> new_www

This will install the programs in 

/usr/bin/*

#TODO:
Do not forget to set the 

  FG_HOME_LOG_ANALYZER  

<<<<<<< HEAD
than call 
fg-metric

If you like to use the php framework, we have not yet written a
documentation for that.

=======
>>>>>>> new_www

COMMANDS
========

<<<<<<< HEAD
fg-clenaup-db
* erases the content of the database

fg-parser
* parses eucalyptus log entries and includes them into the database

fg-euca-gather-log-files 
* gathers all eucalyptus log files into a single directory from the
eucalyptus log file directory. This script can be called from cron
repeatedly in order to avoid that log data is lost by using log file
rotation in eucalyptus.

fg-metric
* a shell to interact with the metric database. 
=======
fg-euca-log-analyzer.pl 
* Analyses the number of running instances and terminated instances are 
  collected 
* Reporting interval: hourly

fg.log.analyzer.4.eucalyptus.pl
* Analyses minutes used by users and the number of instances used by users 
* Reporting interval: daily

fg.log.merger.sh, and fg.log.gz.decompressor.sh
* mereges log files from the backup storage are restored and decompressed 
>>>>>>> new_www

OTHER
=====
./www
* displays graphs about data usage metrics are in 'www'
* Be displaying via google chart tools.

CONTRIBUTORS
============
Hyungro Lee (lee212 at indiana dot edu)   
Gregor von laszewski (laszewski@gmail.com)

KNOWN BUGS
==========
* we like to move to a python egg with easy_install
