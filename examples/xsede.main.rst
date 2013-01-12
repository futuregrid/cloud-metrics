.. =================================================================================================
.. MAIN TEMPLATE

.. This will be iterated by services and hosts when they are specified.
.. For example, if nimbus, hotel, alamo, foxtrot, sierra specified, this MAIN TEMPLATE will be generated
.. in 4 different rst files

.. Hyungro Lee (lee212@indiana.edu)
.. 01/11/2013
.. FutureGrid project
.. =================================================================================================

Usage Half-Yearly Report for %(service)s on %(hostname)s
================================================================

- Period: %(from_date)s to %(to_date)s
- Hostname: %(hostname)s.futuregrid.org
- Services: %(service_name)s
- Metrics: VMs count, Users count, Wall hours, Distribution by Wall Hours, Project, Project Leader, and Institution, and Systems

Histogram
---------

Summary (Monthly)
^^^^^^^^^^^^^^^^^^^^^

.. Summary chart for services on systesms
.. ================================================================================================================
.. 1) WALL HOURS / VM COUNT / COUNT USERS (MIXED)
.. ================================================================================================================

.. figure:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-runtimecountcountusers-%(service)s-%(hostname)s-monthlyAll.png
   :alt: Average Monthly Usage Data (Wall hour, Launched VMs, Users)
   :align: left
   
   Average Monthly Usage Data (Wall hour, Launched VMs, Users)

   This mixed chart represents average monthly usage as to Wall Hour (runtime), Count and the number of Users for VM instances.

   +-------------+-------------------------------------+
   | Metric      | Description                         |
   +=============+=====================================+
   | Wall Hour   | Terminated time - Launched time     |
   +-------------+-------------------------------------+
   | count       | The number of launched VM instances |
   +-------------+-------------------------------------+
   | user count  | The number of users who launched VMs|
   +-------------+-------------------------------------+

|
|
|
|
|

Summary (Daily)
^^^^^^^^^^^^^^^^^^^

.. ================================================================================================================
.. 2) USERS COUNT (Daily)
.. ================================================================================================================

.. figure:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-countusers-%(service)s-%(hostname)s-dailyAll.png
   :alt: Users count (daily)
   :align: left

   The count of users

   This time series chart represents daily active user counts for cloud services and shows historical changes during the period.

|
|
|
|
|
|
|
|
|
|


.. ================================================================================================================
.. 3) VM COUNT (DAILY)
.. ================================================================================================================

.. figure:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-count-%(service)s-%(hostname)s-dailyAll.png
   :alt: VMs count (daily)
   :align: left

   VMs count

   This time series chart represents the number of daily launched VM instances for cloud services and shows historical changes during the period.

|
|
|
|
|
|
|
|
|





.. ================================================================================================================
.. 4) WALL HOURS (DAILY)
.. ================================================================================================================

.. figure:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-runtime-%(service)s-%(hostname)s-dailyAll.png
   :alt: Wall Hours (daily)
   :align: left

   Wall Hours

   This time series chart represents daily Wall Hours for cloud services and shows historical changes during the period.

|
|
|
|
|
|
|
|
|
|

Distribution
------------


.. ================================================================================================================
.. 5) VM COUNT BY WALL HOURS 
.. ================================================================================================================

.. figure:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-count-%(service)s-%(hostname)s-walltimeAll.png
   :alt: VM count by Wall Hours
   :align: left

   VM count by Wall Hours

   This column chart represents VM counts that are group by Wall Hours in 8 different sections. This helps to understand usage pattern of VM instances in terms of running hours.
|
|
|
|
|
|
|
|
|
|
.. ================================================================================================================
.. 6) VMs count by Project
.. ================================================================================================================

.. figure:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-count-%(service)s-%(hostname)s-projectAll.png
   :alt: VMs count by Project
   :align: left

   VMs count by Project

   This pie chart illustrates propotion of Launched VM instances by Project groups. To represent certain information, the table follows.

   .. csv-table:: VMs count by Project
      :file: ../../%(output_directory)s/%(from_dateT)s-%(to_dateT)s-count-%(service)s-%(hostname)s-projectAll.csv
|
|
|
|
|
|
|
|
|
|

.. ================================================================================================================
.. 7) VM COUNT BY PL
.. ================================================================================================================

.. figure:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-count-%(service)s-%(hostname)s-projectleaderAll.png
   :alt: VMs count by Project Leader
   :align: left

   VMs count by Project Leader
   
   This pie chart also illustrates propotion of Launched VM instances by Project Leader. To represent certain information, the table follows.

.. csv-table:: VMs count by Project Leader
   :file: ../../%(output_directory)s/%(from_dateT)s-%(to_dateT)s-count-%(service)s-%(hostname)s-projectleaderAll.csv

.. ================================================================================================================
.. 8) VM COUNT BY INSTITUTION
.. ================================================================================================================

.. figure:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-count-%(service)s-%(hostname)s-institutionAll.png
   :alt: VMs count by Institution 
   :align: left

   VMs count by Institution 
   
   This pie chart illustrates propotion of Launched VM instances by Institution. To represent certain information, the table follows.

.. csv-table:: VMs count by Institution
   :file: ../../%(output_directory)s/%(from_dateT)s-%(to_dateT)s-count-%(service)s-%(hostname)s-institutionAll.csv

.. ================================================================================================================
.. 9) WALL HOURS BY PL
.. ================================================================================================================

.. figure:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-runtime-%(service)s-%(hostname)s-projectleaderAll.png
   :alt: Wall Hours by Project Leader
   :align: left

   Wall Hours by Project Leader

   This bar chart shows comparisons among Project Leaders and helps understanding lengths propotional to the values.

System information
-------------------
Each cluster consists of physical hardwares and the charts below show utilization distribution in terms of VM count and Wall Hours

.. ================================================================================================================
.. 10) VM COUNT BY NODES
.. ================================================================================================================

.. figure:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-count-%(service)s-%(hostname)s-serviceTag.png
   :alt: VMs count by systems in Cluster 
   :align: left

   VMs count by systems (nodes) in Cluster 

   This column chart represents VM count among systems (nodes).

.. ================================================================================================================
.. 11) VM COUNT BY NODES
.. ================================================================================================================

.. figure:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-runtime-%(service)s-%(hostname)s-serviceTag.png
   :alt: Wall Hours by systems in Cluster 
   :align: left

   Wall Hours by systems in Cluster 

   This column chart represents Wall Hours among systems (nodes).
