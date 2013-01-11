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
.. figure:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-runtimecountcountusers-%(service)s-%(hostname)s-monthlyAll.png
   :alt: Average Monthly Usage Data (Wall hour, Launched VMs, Users)
   
   Figure 1: Average Monthly Usage Data (Wall hour, Launched VMs, Users)

   This chart represents average monthly usage as to Wall Hour (runtime), Count and the number of Users for VM instances.

   +-------------+-------------------------------------+
   | Metric      | Description                         |
   +=============+=====================================+
   | Wall Hour   | Terminated time - Launched time     |
   +-------------+-------------------------------------+
   | count       | The number of launched VM instances |
   +-------------+-------------------------------------+
   | user count  | The number of users who launched VMs|
   +-------------+-------------------------------------+


Summary (Daily)
^^^^^^^^^^^^^^^^^^^
.. figure:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-countusers-%(service)s-%(hostname)s-dailyAll.png
   :alt: Users count (daily)

   Figure 2: The count of users

   This chart represents daily active user counts for services.

.. figure:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-count-%(service)s-%(hostname)s-dailyAll.png
Figure 3: VMs count

.. figure:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-runtime-%(service)s-%(hostname)s-dailyAll.png
Figure 4: Wall Hours

Distribution
------------

.. figure:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-count-%(service)s-%(hostname)s-walltimeAll.png
Figure 5: VM count by Wall Hours

.. figure:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-count-%(service)s-%(hostname)s-projectAll.png
Figure 6: VMs count by Project

.. csv-table:: VMs count by Project
        :file: ../../%(output_directory)s/%(from_dateT)s-%(to_dateT)s-count-%(service)s-%(hostname)s-projectAll.csv

.. figure:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-count-%(service)s-%(hostname)s-projectleaderAll.png
Figure 7: VMs count by Project Leader

.. csv-table:: VMs count by Project Leader
        :file: ../../%(output_directory)s/%(from_dateT)s-%(to_dateT)s-count-%(service)s-%(hostname)s-projectleaderAll.csv

.. figure:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-count-%(service)s-%(hostname)s-institutionAll.png
Figure 8: VMs count by Institution 

.. csv-table:: VMs count by Institution
        :file: ../../%(output_directory)s/%(from_dateT)s-%(to_dateT)s-count-%(service)s-%(hostname)s-institutionAll.csv

.. figure:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-runtime-%(service)s-%(hostname)s-projectleaderAll.png
Figure 9: Wall Hours by Project Leader

System information
-------------------

.. figure:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-count-%(service)s-%(hostname)s-serviceTag.png
Figure 10: VMs count by systems in Cluster 

.. figure:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-runtime-%(service)s-%(hostname)s-serviceTag.png
Figure 11: Wall Hours by systems in Cluster 
