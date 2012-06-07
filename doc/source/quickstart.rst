Quickstart
==========

Backing up Eucalyptus log data
------------------------------

 TBD

Creating Results
----------------

 We assume you have a valid pthon version (2.7.2) and all the needed
 libraries on the system where you run the code. We also assume you
 have installed a results database and pupulated it with data from log
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

   TODO




