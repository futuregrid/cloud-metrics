NAME
====
 
 **fg-euca-gather-log-files** - collect cc.log files of eucalyptus and
 rename it with unique file names with 'YYYY-MM-DD-HH-mm-ss-cc.log'
 type. Duplicated file s are ignored.

SYNOPSIS
========

 **fg-euca-gather-log-files** [OPTION]... -i <from_dir> -o <backup_dir>

DESCRIPTION
===========

 Eucalyptus 2.0 provides a number of log files that are written into a
 directory.  The log files are maintained with the rrd tool, thus they
 will be overwritten after a particular time period. This tool copies
 the log files that end with .log.? into a backup directory. A log
 file will only be copied into backup if it is not already there. This
 avoids unnecessary operations and allows the integrat ion of this
 script into cron.

 The program has a number of parameters by default it takes two
 directories. The first directory is the directory from which all log
 files are copied. The second is the directory to which the files are
 to be copied (e.g our Backup directory).  If the backup directory
 does not exists it is being utomatically created.

 One thing is important to not that the current script looks
 recuresively through all subdirectories starting from the from
 dir. This is due to the fact that our initial script backed up all
 files into various subdirectories. All files will be renamed to

   YYYY-MM-DD-HH-mm-ss-cc.log

 Specific arguments can be controlled as follows

  -r, -R, --recursive
      search directories and their contents recursively

  -o, --backup <dir>
      specify the backup directory (renamed log files will be saved here)

  -i, --source <dir>
      specify the source directory of eucalyptus logs 
      (default: /var/log/eucalyptus)

  -t, --log-type <filename>
      specify a log type to be gathered (default: cc.log)
      
 If any of the parameters are used the specification of any
 parameters without named parameters is not allowed. Calling::

    fg-euca-gather-log-files --source <from_dir> --backup <backup_dir>

 is equicvalent to::

    fg-euca-gather-log-files -i <from_dir> -o <backup_dir>

 In a production environment we recommend using explicit parameter naming
 in order to be more transparent.

EXAMPLES
========

 **Cron Setup**
 
 The following line causes the fg-euca-gather-log-files to be run once an hour::

    0 * * * * /usr/local/bin/fg-euca-gather-log-files --source <from_dir> --backup <backup_dir>


AUTHOR
======

 Written by Gregor von Laszewski, Fugang Wang and H. Lee

REPORTING BUGS
==============

 Report fg-cleanup-table bugs to laszewski@gmail.com
 Github home page: <https://github.com/futuregrid/futuregrid-cloud-metrics>

CONTRIBUTION
============

 If you like to contribute to the code, please contact Gregor von Laszewski
 at laszewski@gmail.com. The code is located on github at

 https://github.com/futuregrid/eucalyptus-cloud-metrics

 in the directory cloud-metrics

COPYRIGHT
=========

 The code is distributed under Apache 2.0 License

SEE ALSO
========
