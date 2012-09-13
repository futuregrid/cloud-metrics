Details
=======


Shell to analyze data
---------------------

 The purpose of our framework is to identify and analyze data from
 various production clouds. Relevant data will be uploaded into a
 database.  We have several convenient mechanisms to deal with the
 data.  We can create summary of the data and can export in a variety
 of formats. This summary is especially important for administrators
 who like to find out what is happening on their clouds, but also for
 users to see with who they compete for resources. The output format
 includes png, googlecharts, and cvs tables.  As part of our analysis
 we are also developing an interactive shell that can be used to query
 data directly from our database. Some simple example illustrate our
 usage of the shell.

 The following picture gives an overview on which components are
 communicating with each other to gather and display the data

 .. graphviz::

   digraph foo {
      graph [rankdir=LR];
      "Log Cloud A" -> "Backup";
      "Log Cloud B" -> "Backup";
      "          ...      " -> "Backup";
      "Log Cloud N" -> "Backup";
      "Backup" -> "Database";
      "Database" -> "Shell";
      "Database" -> "Portal";
      "Portal" -> "Portal User";
      "Shell" -> "Shell User";
   }

 1. various clouds produce many log files
 2. the log files will be moved to a backup directory
 3. the log files that have been recently moved will be inspected and
     their contents will be added to the database
 4. the database is queried by a fg-metric commandwhich is a simple
     shell that allows to quey for some very elementary iformation. It also
     allows to generate graphics for this information and place them in
     a web server
 5. For our portal we havechosen not to use an interactive portal that
     interacts with the database on demand, but to just provide a static
     directory tree in sphinx that will be refreshed from ime to time.
     (This is sufficient for our current use case

 To show some commands of the shell we have provided a small set of
 examples.
 
Examples
--------

Create a summary table for the month of January
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 The following will create a table with data produced for the month of January::

    > fg-metric
    fg> clear users
    fg> analyze -M 01
    fg> table --type users --separator ,  --caption Testing_the_csv_table
    fg> quit

 Naturally you could store this script in a file and pipe to fg-metric
 in case you have more complex or repetitive analysis to do. 

Create a summary analysis for multiple month
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 Assume you like to create a nice html page directory with the
 analysis of the data contained. This can be done as follows. Assume
 the following contents is in the file analyze.txt::

    clear users
    analyze -M 01 -Y 2012
    createreport -d 2012-01 -t Running_instances_per_user_of_Eucalyptus_in_India
    
    clear users
    analyze -M 02 -Y 2012
    createreport -d 2012-01 -t Running_instances_per_user_of_Eucalyptus_in_India
  
    createreports 2012-01 2012-02

 This page creates a beautiful report page with links to the generated
 graphs contained in the directories specified. All index files in the
 directories are printed before the images in the directory are
 included. The resulting report is an html report.

 To start the script, simply use::

    cat analyze.txt | fg-metric

 This will produce a nice directory tree with all the data needed for a
 display.

Show machine image counts for Eucalyptus
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 Based on Jonathan's code, we are able to get image counts via cmd2 tools.
 It's established on 'euca-describe-images' command::

        (Cmd) count_images
        ...
        sazh72  1
        debian-rm1984   1
        pegasus-images  3
        wchen-server-stage-1    2
        ...

 There are additional options which might be useful,

 1) showing only image numbers owned by the userid specified::

    (Cmd) count_image -u jdiaz
    jdiaz   7
   
 2) displaying details about images::

        (Cmd) count_images -u jdiaz -d
        jdiaz   7
        IMAGE   emi-1CA015A7    centos-image-bucket/centos.5-3.x86-64.img.manifest.xml  taklwu  available       public          x86_64  machine eki-78EF12D2    eri-5BB61255    instance-store
        IMAGE   emi-DBC4106B    ubuntu-0904-saga-1.5.2/image.manifest.xml       luckow  available       public          x86_64  machine eki-78EF12D2    eri-5BB61255    instance-store
        IMAGE   emi-F840162A    myubuntubucket/ubuntufloeserver.img.manifest.xml        sreedharnat1    available       public          x86_64  machine eki-78EF12D2    eri-5BB61255    instance-store
        IMAGE   eki-7A031340    mybucket/vmlinuz-2.6.28-11-generic.manifest.xml ajyounge        available       public          x86_64  kernel                  instance-store
        IMAGE   emi-E5D514DA    jdiaz/ubuntunattyjdiaz3595279807.img_0.manifest.xml     javidiaz        available       public          x86_64  machine eki-78EF12D2    eri-5BB61255    instance-store
        IMAGE   emi-46861248    jdiaz/centos6jdiaz2698814667.img.manifest.xml   javidiaz        available       public          x86_64  machine eki-78EF12D2    eri-5BB61255    instance-store
        IMAGE   emi-431F1230    jdiaz/centos6jdiaz2710350825.img.manifest.xml   javidiaz        available       public          x86_64  machine eki-78EF12D2    eri-5BB61255    instance-store
        IMAGE   emi-0E0E165E    ajyounge/ubuntu-twister-memcached.img.manifest.xml      ajyounge        available       public          x86_64  machine eki-78EF12D2    eri-5BB61255    instance-store
        IMAGE   emi-A5B6148A    ajyounge/ubuntu-lucid-minimal.img.manifest.xml  ajyounge        available       public          x86_64  machine eki-78EF12D2    eri-5BB61255    instance-store
        IMAGE   emi-4A051306    ajyounge/ubuntu-lucid-mpj.img.manifest.xml      ajyounge        available       public          x86_64  machine eki-78EF12D2    eri-5BB61255    instance-store
        IMAGE   emi-48141244    ajyounge/ajyounge-1563160039.img.manifest.xml   ajyounge        available       public          x86_64  machine eki-78EF12D2    eri-5BB61255    instance-store
        IMAGE   emi-FC6A1197    ajyounge/ubuntu-natty.img.manifest.xml  ajyounge        available       public          x86_64  machine eki-78EF12D2    eri-5BB61255    instance-store

 3) displaying summary values about images.
    e.g. total image counts, total user counts, average image counts 
    per user, and maximum image counts and userid::

        (Cmd) count_images -s
        ...
        = Summary =
        Total image counts:     128
        Total user counts:      71
        Average image counts per user:  1.80281690141
        Maximum image counts and userid:        ajyounge has 12
        ==========

Eucalyptus 2.0
--------------

Data gathering
~~~~~~~~~~~~~~

 Eucalyptus provides a substantial set of log information. The
 information is stored in the eucalyptus log directory.
 Typically it is configured by the system administrator with log
 rotation. This naturally would mean that the information is lost
 after a time period specified by the log rotation
 configuration. There are two mechanisms of avoiding this. The first
 method is to change the eucalyptus configuration files in order to
 disable log rotation. However this has the disadvantage that the
 directories may fill up and eucalyptus runs out of space.  How to
 disable Eucalyptus log rotation is discussed in the manaula at ... .
 However we decided to go another route, buy copying the Eucalyptus
 log files after a particular period of time and place them onto our
 analysis server and also a backup server. To set this mechanism up, a
 Eucalyptus system administrator simply can install our tools in a
 predefined directory and call a command that copies the log
 files. Ideally This is integrated into a cron script so that the
 process is done on regular basis.

 To switch on eucalyptus in debug mode 'EUCADEBUG'  you will have to do the
 following

    TODO

 Here is how you set this up::

    pip install futuregrid.cloud.metric
    
 This will install several commands in the bin directory. Make sure
 that it is in your path

 Now you can call the command::

    fg-euca-gather-log-files

 A more detailed description is provided as part of the
 `fg-euca-gather-log-files <./man/fg-euca-gather-log-files.html>`_
 manual page
   
 which will copy all logfiles that has not yet been copied into our
 backup directory. The log files have a numerical value from 1 to 9 as
 a postfix Once this is done, our analysis scripts can be called from
 the commandline or a web page to create information about usage and
 utilization.

 To see more information about this command, please visit the manual
 page [fg-euca-gather-log-files](./man/fg-euca-gather-log-files.md)


Installation
------------

 You have various options to install this program. However it requiers
 the MYSQL python library which is on some platforms not that easy to install.

Prerequisite
------------

 Python version >= 2.7
 
 (Required Python packages)
 setuptools
 pygooglechart

Installation from pypi 
~~~~~~~~~~~~~~~~~~~~~~

 The programs are distributed in `pypi <http://pypi.python.org/pypi/futuregrid.cloud.metric/>`_ . It
 contains our current release version of the software.


Installation form the source in github
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 If you are adventures, you can work with our newest code checked into
 github. To obtain this code, please conduct the following steps.  We
 assume you have root privileges to execute "make force"::

    wget https://github.com/futuregrid/futuregrid-cloud-metrics/tarball/v2.1.1
    tar xvzf v2.1.1
    cd futuregrid-futuregrid-cloud-metrics-4635fc9
    make force 
    
 This will install the programs in::

    /usr/bin/
    
What to do if I do not have root privilege
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 If you do not have root privileges, you can also install the program
 via pythons virtualenv.


Commands
--------

 `fg-cleanup-db <./man/fg-cleanup-db.html>`_

     erases the content of the database

 `fg-parser <./man/fg-parser.html>`_

     parses eucalyptus log entries and includes them into the database


 `fg-euca-gather-log-files <./man/fg-euca-gather-log-files.html>`_

     gathers all eucalyptus log files into a single directory from the
     eucalyptus log file directory. This script can be called from
     cron repeatedly in order to avoid that log data is lost by using
     log file rotation in eucalyptus.

 `fg-metric <./man/fg-metric.html>`_

     a shell to interact with the metric database. 


Examples Scripts
----------------

 Please find a small set of example scripts. Example 2 is most
 interesting as it produces output for multiple month on VM ussage and 
 wallclock time associated with the users

 * `example1.txt <./examples/example1.txt>`_
 * `example2.txt <./examples/example2.txt>`_
 * `test.txt <./examples/test.txt>`_


FEATURE REQUESTS
----------------

 This project is under active development. In order for us to identify
 priorities please let us know what features you like us to add.  We
 will include a list here and identify based on resources and
 priorities how to integrate them.

