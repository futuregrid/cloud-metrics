Quick Start
===========

1. Download FG Cloud Metric
---------------------------
from PyPI

We have a version on pypi that you can install with::

        pip install futuregrid-cloud-metric

2. Create Log Backup of Eucalyptus
----------------------------------

This section explains how to make a log backup transaction of eucalyptus using FG Metric tools. 
The Cluster Controller (CC) of eucalyptus generates a log file (named cc.log) which is a main resource provider for the tools, so creating log backup of eucalyptus is the most important start-up.

        1. Log into the management node of eucalyptus with access to the log files
        2. Create crontab::
           #Hourly
           0 * * * * fg-euca-gather-log-files -i <directory of log files> -o <directory of backup>

3. Parse log backup and store parsed data into MySQL database
-------------------------------------------------------------

Once we collected log backup by fg-euca-gather-log-files, we need to parse and store log files into database. MySQL configuration should be set by .futuregrid.cfg such as hostname, id, password, and port number.

 ::

        fg-parser -i <directory of the backup>

4. Generate Results
-------------------

Using examples

 ::

        cat examples/example2.txt | fg-metric

Or typing commands on python command-line interpreter.

 ::

        $ fg-metric
        ...
        (Cmd) analyze -Y 2012
        (Cmd) createreport -d 2012 

 
Additional notes
----------------

 We assume you have a valid python version (2.7.2 or higher) and all the needed
 libraries on the system where you run the code. We also assume you
 have installed a results database and populated it with data from log
 files.

 You will need the following python libraries:

    setuptools, pip, cmd2, pygooglechart, mysql-python

 Now you just download the code from github 

   git clone git@github.com:futuregrid/futuregrid-cloud-metrics.git

 Create a ~/.futuregrid/futuregrid.cfg file that includes the
 following::

    [EucaLogDB]
    host=<yourhostname>
    port=<portnumber>
    user=<username>
    passwd=<password>
    db=<dbname>

 Now you are ready to create results in a sphinx web page::

   cd futuregrid-cloud-metric*/doc
   make force

 If you met all the prerequisits, you will find the index file in 

   futuregrid-cloud-metric*/doc/build/html/index.html

 live example of the data is available at

   `http://portal.futuregrid.org/doc/metric/results.html <http://portal.futuregrid.org/doc/metric/results.html>`_

