=========
fg-metric
=========

NAME
====

 **fg-metric** - analyze utilization data and generate graphical reports using various chart formats

SYNOPSIS
========

 **fg-metric**

DESCRIPTION
===========

 This tool works in python cmd2 mode. It accepts multi-lines stdin to
 run cmd2 commands. Also, it goes into a new command line interfaces
 by simply run fg-metric.

 **analyze**
   function to analyze utilization of cloud

     -f, --start start_date
                start time of the interval (type. YYYY-MM-DDThh:mm:ss)
     -t, --end end_date
                end time of the interval (type. YYYY-MM-DDThh:mm:ss)
     -M, --month month
                month to analyze (type. MM)
     -Y, --year year
                year to analyze (type. YYYY)
     -S, --stats
                item name to measure (e.g. runtime, vms)
     -P, --period
                search period (weekly, daily)

 **changecharttype** [pie|bar|motion]
   - change chart type to pie, bar, and motion chart. Default type is pie chart.

 **table** [OPTION]...

 **loaddb**
   Read the statistical data from MySQL database

 **dump**
        Print the data from all instances

 **printlist**
        List all instance ids id's

 **clear**
        Clear all instance data and user data from the memory
        ::
                clear users (clear user data)
        ::
                clear instances (clear instance data)
        ::
                clear all (clear all data)

 **createreport**
        Create PNG graphs which display statistics

 count_images_
        Count bucket images per user

 .. _count_images: fg-metric/commands.html


EXAMPLES
========

 TODO

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
