About
=====

We are developing an open source code that allows to analyze the log
files for various cloud infrastructure tools. At this time, we are
focusing on the development of a tool to analyze eucalyptus log
data. It will include

* a framework to explore the data via a shell 
* a framework to display the data
* a mechanism to replace the charting library
* a web framework (currently based on sphinx and flask)

Goals
------

Our gols include to enable the following capabilities

* integration of multiple centers
* integration of multiple cloud deployments within each center
* integraton of OpenStack
* Integration of HPC services
* integration of Nimbus
* integration of OpenNebula

We are also collaborating with the TAS project that developd
XDMod. ONce this project has open sourced their code we intend to
leverage from their user interface. However, at this time the metics
we collect are not yet integrated. Hence we can not yet use XDMod. We
anticipate that modifications to XDMod will be conducted over the
next year to accomplish this goal.


Contributors
------------

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


Joining the Development Team
----------------------------

If you like to join the development efforts, please e-mail us. We can
than discuss how best you can contribute. You may have enhanced our
code already or used it in your system. If so, please let us know.

Related Activities
--------------------

Inca
      Inca does monitoring at specific time intervals. The information
      about clouds on FG is available at
      https://portal.futuregrid.org/monitoring/cloud


Nimbus
    Nimbus provides their own metric framework. For FG you can see it
    at http://inca.futuregrid.org/nimbus-stats/.
    This front page is not very pretty, but lists in its pu data the
    following metrics for each machine:

     * requests made by user
     * minutes used by user

     * requests made by week
     * minutes used by user

     In the ussgae data we find for the week of the year the following
     information for each machine

     * minutes used by week

