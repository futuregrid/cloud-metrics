NAME
====

 **fg-metric** - analyze utilization data with python cmd tool

SYNOPSIS
========

 **fg-metric**

DESCRIPTION
===========
This tool works in python cmd2 mode. It accepts multi-lines stdin to run cmd2 co
mmands. Also, it goes into a new command line interfaces by simply run fg-metric
. 

(cmd) commands are following:

**analyze** [OPTION]...
 - A main function to analyze utilization of cloud

 -f, --start start_date
             start time of the interval (type. YYYY-MM-DDThh:mm:ss)
 -t, --end end_date
           end time of the interval (type. YYYY-MM-DDThh:mm:ss)
 -M, --month month
             month to analyze (type. MM)
 -Y, --year year
            year to analyze (type. YYYY)

**changecharttype** [pie|bar|motion]
 - change chart type to pie, bar, and motion chart. Default type is pie chart.

**table** [OPTION]...

**loaddb**

**dump**

**printlist**

**clear**

**printusers**

**creategraph**

**createhtml**

**createreport**

**createreports**


EXAMPLES
========

```
```

AUTHOR
======

Written by H. Lee, Fugang Wang and Gregor von Laszewski.

REPORTING BUGS
==============

Report fg-cleanup-table bugs to laszewski@gmail.com
Github home page: <https://github.com/futuregrid/futuregrid-cloud-metrics>

COPYRIGHT
=========

SEE ALSO
========
