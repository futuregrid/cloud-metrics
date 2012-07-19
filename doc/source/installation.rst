Installation Cloud Metrics 
==========================

Prerequisites
-------------
 We assume you have a valid python version (2.7.2 or higher) and all the needed
 libraries on the system where you run the code. We also assume you
 have installed a results database and populated it with data from log
 files.

 You will need the following tools and libraries:

        1. `python 2.7+ <http://www.python.org/download/>`_
        2. python modules

           - `setuptools <http://pypi.python.org/pypi/setuptools/0.6c11#downloads>`_

             ::

               wget http://pypi.python.org/packages/2.7/s/setuptools/setuptools-0.6c11-py2.7.egg#md5=fe1f997bc722265116870bc7919059ea
               sh setuptools-0.6c11-py2.7.egg --prefix=~

           - `cmd2 <http://pypi.python.org/pypi/cmd2/>`_
           - `mysql-python <http://pypi.python.org/pypi/MySQL-python/>`_
           - `pip <http://pypi.python.org/pypi/pip/#downloads>`_
           - `sphinx <http://pypi.python.org/pypi/Sphinx>`_
        3. sphinx extension

           - `sphinxcontrib-googlechart <http://pypi.python.org/pypi/sphinxcontrib-googlechart/>`_
           - `sphinxcontrib-issuetracker <http://pypi.python.org/pypi/sphinxcontrib-issuetracker>`_
           - `sphinx-contrib/autorun <https://bitbucket.org/birkenfeld/sphinx-contrib/src/bf0e1d56c6e3/autorun>`_
        4. `pygooglechart <http://pygooglechart.slowchop.com/>`_
        5. `mysql community server <http://dev.mysql.com/downloads/mysql/>`_

Configuration
-------------
Cloud Metrics has a configuration file to manage access information of databases.

The default file path and name look like::

           ~/.futuregrid/futuregrid.cfg

and the content has the following template::

    [EucaLogDB]
    host=<yourhostname>
    port=<portnumber>
    user=<username>
    passwd=<password>
    db=<dbname>

    [NovaDB]
    host=<your openstack database host - mysql>
    port=<port number>
    user=<username>
    passwd=<password>
    novadb=<nova database name which includes instances table>
    keystonedb=<nova keystone database name which includes user table> 

1. Download FG Cloud Metric
---------------------------
from github

We have a development version on github that you can install with::

        git clone https://github.com/futuregrid/futuregrid-cloud-metrics.git

2. Create Web pages using Sphinx
--------------------------------
 Now you are ready to create results in a sphinx web page::

   cd futuregrid-cloud-metric*/doc
   make force

 If you met all the prerequisits, you will find the index file in 

   futuregrid-cloud-metric*/doc/build/html/index.html

 live example of the data is available at

   `http://portal.futuregrid.org/metrics/html/results.html <http://portal.futuregrid.org/metrics/html/results.html>`_

