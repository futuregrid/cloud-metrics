Welcome to Cloud Metrics's documentation!
=========================================

.. sidebar:: Table of Contents

    .. toctree::
       :maxdepth: 2

       installation
       details
       examples
       rest
       metrics
       ubmod
       lighttpd
       modules
       todo

.. warning:: TODO Hyungro, please include nice image here

Cloud metrics is an open source code project that allows to analyze
the log files for various cloud infrastructure tools. At this time, we
are focusing on the development of a tool to analyze eucalyptus log
data. It will include

* a framework to explore the data via a shell 
* a framework to display the data
* a mechanism to replace the charting library
* a web framework (currently based on sphinx and flask)

Our gols include to enable the following capabilities

* integration of multiple centers
* integration of multiple cloud deployments within each center
* integraton of OpenStack
* Integration of HPC services
* integration of Nimbus
* integration of OpenNebula

Relevant data will be uploaded into a
database.  We have several convenient mechanisms to deal with the
data.  We can create summary of the data and can export in a variety
of formats. This summary is especially important for administrators
who like to find out what is happening on their clouds, but also for
users to see with who they compete for resources. The output format
includes png, googlecharts, and cvs tables.  As part of our analysis
we are also developing an interactive shell that can be used to query
data directly from our database. Some simple example illustrate our
usage of the shell. 

.. 
   We are also collaborating with the TAS project that developd
   XDMod. Once this project has open sourced their code we intend to
   leverage from their user interface. However, at this time the
   metics we collect are not yet integrated. Hence we can not yet use
   XDMod. We anticipate that modifications to XDMod will be conducted
   over the next year to accomplish this goal.


Authors in Alphabetical Order
--------------------------------------

* Lee, Hyungro (lee212@indiana.edu)   
* von Laszewski, Gregor (laszewski@gmail.com)
* Wang, Fugang (kevinwangfg@gmail.com)

Please contact laszewski@gmail.com for mor information. Please insert
the prefix: "METRICS: " in the subject of email messages.

The contribution impact is recorded at

* https://github.com/futuregrid/futuregrid-cloud-metrics/graphs
* https://github.com/futuregrid/cloud-metrics/contributors

The original database integration was contributed by Fugang Wang and
was not tracked.

If you like to join the development efforts, please e-mail us. We can
than discuss how best you can contribute. You may have enhanced our
code already or used it in your system. If so, please let us know.

If you run into problems when using the cloud metric framework, please use our 
help form at `https://portal.futuregrid.org/help <https://portal.futuregrid.org/help>`_.


Production Deployment
--------------------

`Cloud Metrics <https://portal.futuregrid.org/metrics>`_ is our main
monitoring system for clouds on FuturegGrid. In addition we also
deployed other monitoring systems such as `Inca <https://portal.futuregrid.org/monitoring/cloud>`_ which does
monitoring at specific time intervals, and `Nimbus
<http://inca.futuregrid.org/nimbus-stats/>`_ which offers a less
sophisticated and less comprehensive set of monitoring tools than our
framework provides. However we integrate the data from Nimbus in our
framework


..
    Indices and tables
    ==================

    * :ref:`genindex`
    * :ref:`modindex`
    * :ref:`search`

