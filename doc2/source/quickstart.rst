Quick Start
===========

.. sidebar:: 
   . 

  .. contents:: Table of Contents
     :depth: 3


..

Download 
---------------------------

The FG Cloud Metric is available from PyPI and can be easily installed
with pip. We recommend that you use virtualenv to manage your local
python instalations. As install tool we recommend pip.

        pip install futuregrid-cloud-metric

Development version
----------------------------------------------------------------------

The development version is available from github at 

* ... TODO: Hyungro

YOu can download a tar.gz file from 

* ... TODO: Hyungro

Once you donloaded and uncompressed the file you will see a folder
``cloud-metric``. Cd in this folder and say::

     python setup.py install


Create A Log Backup of Eucalyptus
----------------------------------

This section explains how to make a log backup transaction of
eucalyptus using FG Metric tools.  The Cluster Controller (CC) of
eucalyptus generates a log file (named cc.log) which is a main
resource provider for the tools, so creating log backup of eucalyptus
is the most important start-up.

1. Log into the management node of eucalyptus with access to the log files

2. Create crontab::

      #Hourly
      0 * * * * fg-euca-gather-log-files -i <directory of log files> -o <directory of backup>


Parse the Log Backup 
-----------------------------------

Once we collected log backup by ``fg-euca-gather-log-files``, we need to
parse and store log files into database. MySQL configuration should be
set by ``.futuregrid.cfg`` such as hostname, id, password, and port
number::

        fg-parser -i <directory of the backup>


Generate Results
-------------------

Now you can use the convenient fg-metric shell to create results::

        $ fg-metric
        ...
        (Cmd) analyze -Y 2012
        (Cmd) createreport -d 2012 

..


You can sore also the templates you use to create results with in a
file and input them to our fg-metric shell::

        cat examples/example2.txt | fg-metric


 
Additional Notes
----------------

We assume you have a valid python version (2.7.2 or higher) and all
the needed libraries on the system where you run the code. We also
assume you have installed a results database and populated it with
data from log files.

You will need the following python libraries::

    setuptools, pip, cmd2, pygooglechart, mysql-python

..


Now you just download the code from github::

   git clone git@github.com:futuregrid/futuregrid-cloud-metrics.git

..


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

If you met all the prerequisits, you will find the index file in::

   futuregrid-cloud-metric*/doc/build/html/index.html


..

A live example of the data is available at

*  `http://portal.futuregrid.org/doc/metric/results.html <http://portal.futuregrid.org/doc/metric/results.html>`_

OpenStack
======================================================================

TODO: Hyungro