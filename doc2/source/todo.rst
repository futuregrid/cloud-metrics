Eucalyptus 2.0 Data Integration
======================================================================

To achieve analysis of eucalyptus data, we are using 'cc.log'
files. The needed information must be gathered while eucalyptus runs
in 'EUCADEBUG' mode. We assume the following directory layout::

    ./futurgrid/
    ./futurgrid/bin - includes all commands needed to run the log analyzing
    ./futurgrid/lib - includes libraries that may be called from the bin files
    ./futurgrid/etc - location of configuration files
    ./futurgrid/www - location of the www files
    
    
Eucalyptus data gathering
----------------------------------------------------------------------

Eucalyptus provides a substantial set of log information. The
information is typically stored in the eucalyptus log directory
Typically it is also configured by the system administrator with log
rotation. This naturally would mean that the information is lost after
a time period specified by the log rotation configuration. There are
two mechanisms of avoiding this. The first method is to change the
eucalyptus configuration files in order to disable log
rotation. However this has the disadvantage that the directories may
fill up and eucalyptus runs out of space.  How to disable Eucalyptus
log rotation is discussed in the manaul at ... .  However we decided
to go another route, buy copying the Eucalyptus log files after a
particular period of time and place them onto our analysis server and
also a backup server. To set this mechanism up, a Eucalyptus system
administrator simply can install our tools in a predefined directory
and call a command that copies the log files. Ideally This is
integrated into a cron script so that the process is done on regular
basis.

Now you can call the command::

   [fg-euca-gather-log-files](./man/fg-euca-gather-log-files.md)
   
which will copy all logfiles that has not yet been copied into our
backup directory. The log files have a numerical value from 1 to 9 as
a postfix Once this is done, our analysis scripts can be called from
the commandline or a web page to create information about usage and
utilization.

To see more information about this command, please visit the manual
page [fg-euca-gather-log-files](./man/fg-euca-gather-log-files.md)



TODO
----------------------------------------------------------------------

define variables::

    FG_LOG_ANALYZER_WWW_OUTPUT - location where the www files for display are stored
    FG_TMP - location where temporary files are located that are analyzed
    FG_DATA - location where the permanent data is being stored 
    FG_HOME_LOG_ANALYZER - is set to the location of the "futuregrid" directory.
    EUCALYPTUS_LOG_DIR - location where the eucalyptus log dirs are stored

We recommend that the FutureGrid directory is included in the PATH of
the shell that will run the commands.


Commands
======================================================================

[fg-cleanup-db](./man/fg-cleanup-db.md)

erases the content of the database

[fg-parser](./man/fg-parser.md)

parses eucalyptus log entries and includes them into the database


[fg-euca-gather-log-files](./man/fg-euca-gather-log-files.md)

gathers all eucalyptus log files into a single directory from the
eucalyptus log file directory. This script can be called from cron
repeatedly in order to avoid that log data is lost by using log file
rotation in eucalyptus.


[fg-metric](./man/fg-metric.md)

a shell to interact with the metric database. 

