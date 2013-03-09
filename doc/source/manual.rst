**********************************************************************
Administrator Guide
**********************************************************************

.. sidebar:: 
   . 

  .. contents:: Table of Contents
     :depth: 5


..

Installing the Code
======================================================================

Prerequisites
----------------------------------------------------------------------

We assume you have a valid python version (2.7.2 or higher) and all
the needed libraries on the system where you run the code.

Production Version
----------------------------------------------------------------------

The FG Cloud Metric is available from PyPI and can be easily installed
with pip. We recommend that you use virtualenv to manage your local
python instalations. As install tool we recommend pip::

        pip install futuregrid-cloud-metric

Development Version
----------------------------------------------------------------------

The development version is available from github at and you can clone
it and install with::

  git clone https://github.com/futuregrid/cloud-metrics
  cd cloud-metrics
  python setup.py install

Additional packages for sphinx
------------------------------------------

.. warning:: 
   TODO Hyungro please document here all packages that can not be
   installed via pip. I think there may be one or two. all others do
   not need to be mentioned as we ave them in setup, which i modified.
   if something is mssing add them to setup. HOpe setup works, if not, fix.
   ideally i like the setup be also outo install these packages with
   wget, hg, curl, or other tools, so that thinsg are done
   automatically. if a tool is installed with hg, we need to test if
   its on system and interrupt if it can not be found to ask users to
   install hg, and other tools


Setting Up a Database
======================================================================

.. warning:: TODO Hyungro, where is this documented?

`mysql community server <http://dev.mysql.com/downloads/mysql/>`_

Getting Data
----------------------------------------------------------------------

For cloud-metric to work, you naturally need some data to ingest into
it. Cloudmetric can at this time uses mostly IaaS log files as input,
but in future we will add additional information sources form other
information providors. Currently we support Eucalyptus, OpenStack, as
well as Nimbus.

Eucalyptus
----------------------------------------------------------------------

Log Frequency
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

.. warning:: TODO 
   Hyungro, describe how to se the log frequency, point
   to manual if needed, list concrete parameter and filename where
   parameters is to be set. Work with Allan on that.

HERE IS AN OLD INCOMPLETE TEXT I FOUND, THERE IS NOW SOME REDUNDANT
INFORMATION HERE WITH OTHER PORTIONS:

Eucalyptus provides a substantial set of log information. The
information is stored in the eucalyptus log directory.  Typically it
is configured by the system administrator with log rotation. This
naturally would mean that the information is lost after a time period
specified by the log rotation configuration. There are two mechanisms
of avoiding this. The first method is to change the eucalyptus
configuration files in order to disable log rotation. However this has
the disadvantage that the directories may fill up and eucalyptus runs
out of space.  How to disable Eucalyptus log rotation is discussed in
the manaula at ... .  However we decided to go another route, buy
copying the Eucalyptus log files after a particular period of time and
place them onto our analysis server and also a backup server. To set
this mechanism up, a Eucalyptus system administrator simply can
install our tools in a predefined directory and call a command that
copies the log files. Ideally This is integrated into a cron script so
that the process is done on regular basis.

To switch on eucalyptus in debug mode 'EUCADEBUG'  you will have to do the
following

    TODO Hyungro


Create A Log Backup
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


This section explains how to make a log backup of eucalyptus using our
tools.  The Eucalyptus Cluster Controller (CC) generates a log file
named ``cc.log``. In many production environments this log file is
stored in rotating fashion so that you have a number attached with the
log file, while keeping the number of log files to a small set as not
to overwhelm the server on which EUcalyptus runs with data.
Naturally for a metric analysis tool such a deployment is not ideal,
as we will lose data soon. 

To collect all data, we have written a small tool that looks into the
log files renames them with time stamps and copies them over onto
another machine. This process is best set up via a cronscript, but
could also be performed by hand. As we rename that files based on data
entries from the file, we can invoke the command as many times as we
want. If the data is already copied, the file is not transferred.

Note that in our example the backup directory could be a remote location.

1. Log into the management node of eucalyptus that provides access to the log files

2. Create crontab::

      #Hourly
      0 * * * * fg-euca-gather-log-files -i <directory of log files> -o <directory of backup>

A more detailed description is provided as part of the
`fg-euca-gather-log-files <./man/fg-euca-gather-log-files.html>`_
manual page.


Parse the Log Backup 
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Once we collected log files into the backup directory via the
`fg-euca-gather-log-files`` command, we need to parse them into a
convenient database that is easier for us to query. The database
configuration is stored in a file called ``~/.futuregrid/futuregrid.cfg`` and
includes hostname, id, password, and port number, thus you need to
store it securely. The file includes the following::

    [EucaLogDB]
    host=<yourhostname>
    port=<portnumber>
    user=<username>
    passwd=<password>
    db=<dbname>

.. warning:: TODO
   it is illogical to have an entry EucaLogDB, why not "cloud-db",
   also you may want tothink about using a yaml file so we can
   integrate this better with cloudmesh


To invoke the parsing all you have to do is specify
the backup directory. The ``-i`` flag indicates we insert new data
into existing data::

        fg-parser -i <directory of the backup>

OpenStack
----------------------------------------------------------------------

TODO: Hyungro

In ``~/.futuregrid/futuregrid.cfg`` please add::

    [NovaDB]
    host=<your openstack database host - mysql>
    port=<port number>
    user=<username>
    passwd=<password>
    novadb=<nova database name which includes instances table>
    keystonedb=<nova keystone database name which includes user table> 



Nimbus
----------------------------------------------------------------------

TODO: Hyungro


Generate Results
======================================================================

Now you can use the convenient fg-metric shell to create results. The
reason why we have developed a shell is to allow us to issue
consecutive commands as is typically needed in a production
environment. Here we show an example on how to analyze and create
reports for the year 2012::

        $ fg-metric
        fg-metric> analyze -Y 2012
        fg-metric> createreport -d 2012 

..

.. warning:: TODO
    the command create report will be renamed to "create report" note
    the space. It is also unintitive to have a -d option without
    explanation while -Y is used in previous. I suggest to add
    additional -Y option and say this will create automatically
    directory with that year ....  Than you can point out that if you
    like different directory name you can use -d option

As our metric system can use scripts either via piper or named files,
you can store more complex queries into a file and start the metric
framework with them::

        cat examples/example2.txt | fg-metric

or with file flag::

        fg-metric -f examples/example2.txt

Commands
======================================================================

.. csv-table:: List of commands
   :header: Command, Description
   :widths: 15, 50

   `fg-cleanup-db <./man/fg-cleanup-db.html>`_ ,     erases the content of the database
   `fg-parser <./man/fg-parser.html>`_ ,    parses eucalyptus log entries and includes them into the database
   `fg-euca-gather-log-files <./man/fg-euca-gather-log-files.html>`_ , gathers all eucalyptus log files into a single directory from the eucalyptus log file directory. This script can be called from cron repeatedly in order to avoid that log data is lost by using log file rotation in eucalyptus.
     `fg-metric <./man/fg-metric.html>`_, a shell to interact with the metric database. 




Create Production Web pages using Sphinx
======================================================================

.. warning::
   TODO Hyungro, fix all ?? and make suer contents in this section is ok

We provide a simple producton service that uses sphinx to render the
information associated with a cloud deployment. We have done this in
order o provide a very simple framework that you can expand while not
needing to invest any time in learning a web framework. To do this you
must use the development version of the cloud metric framework as
discussed in section ??. 


Next please execute:: 

   cd cloud-metric/doc
   make force

If you met all the prerequisits, you will find the index file in::

   cloud-metric*/doc/build/html/index.html

.. warning::
   TODO Hyungro, I do not think that thsi at all works, you are not describing
   what you do with results


..


live example of the data is available at

*   `http://portal.futuregrid.org/metrics/html/results.html <http://portal.futuregrid.org/metrics/html/results.html>`_

Create Production Web pages using Flask
======================================================================

.. warning::
   TODO Hyungro

Create PDF reports
======================================================================

.. warning::
   TODO Hyungro
