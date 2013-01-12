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


Summary (Daily)
^^^^^^^^^^^^^^^^^^^
.. figure:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-countusers-%(service)s-%(hostname)s-dailyAll.png
   :alt: Users count (daily)

   Figure 2: The count of users

   This time series chart represents daily active user counts for cloud services and shows historical changes during the period.

.. figure:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-count-%(service)s-%(hostname)s-dailyAll.png
   :alt: VMs count (daily)

   Figure 3: VMs count

   This time series chart represents the number of daily launched VM instances for cloud services and shows historical changes during the period.

.. figure:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-runtime-%(service)s-%(hostname)s-dailyAll.png
   :alt: Wall Hours (daily)

   Figure 4: Wall Hours

   This time series chart represents daily Wall Hours for cloud services and shows historical changes during the period.

Distribution
------------

.. figure:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-count-%(service)s-%(hostname)s-walltimeAll.png
   :alt: VM count by Wall Hours

   Figure 5: VM count by Wall Hours

   This column chart represents VM counts that are group by Wall Hours in 8 different sections. This helps to understand usage pattern of VM instances in terms of running hours.

.. figure:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-count-%(service)s-%(hostname)s-projectAll.png
   :alt: VMs count by Project

   Figure 6: VMs count by Project

   This pie chart illustrates propotion of Launched VM instances by Project groups. To represent certain information, the table follows.

.. csv-table:: VMs count by Project
   :file: ../../%(output_directory)s/%(from_dateT)s-%(to_dateT)s-count-%(service)s-%(hostname)s-projectAll.csv

.. figure:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-count-%(service)s-%(hostname)s-projectleaderAll.png
   :alt: VMs count by Project Leader

   Figure 7: VMs count by Project Leader
   
   This pie chart also illustrates propotion of Launched VM instances by Project Leader. To represent certain information, the table follows.

.. csv-table:: VMs count by Project Leader
   :file: ../../%(output_directory)s/%(from_dateT)s-%(to_dateT)s-count-%(service)s-%(hostname)s-projectleaderAll.csv

.. figure:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-count-%(service)s-%(hostname)s-institutionAll.png
   :alt: VMs count by Institution 

   Figure 8: VMs count by Institution 
   
   This pie chart illustrates propotion of Launched VM instances by Institution. To represent certain information, the table follows.

.. csv-table:: VMs count by Institution
   :file: ../../%(output_directory)s/%(from_dateT)s-%(to_dateT)s-count-%(service)s-%(hostname)s-institutionAll.csv

.. figure:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-runtime-%(service)s-%(hostname)s-projectleaderAll.png
   :alt: Wall Hours by Project Leader

   Figure 9: Wall Hours by Project Leader

   This bar chart shows comparisons among Project Leaders and helps understanding lengths propotional to the values.

System information
-------------------
Each cluster consists of physical hardwares and the charts below show utilization distribution in terms of VM count and Wall Hours

.. figure:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-count-%(service)s-%(hostname)s-serviceTag.png
   :alt: VMs count by systems in Cluster 

   Figure 10: VMs count by systems (nodes) in Cluster 

   This column chart represents VM count among systems (nodes).

.. figure:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-runtime-%(service)s-%(hostname)s-serviceTag.png
   :alt: Wall Hours by systems in Cluster 

   Figure 11: Wall Hours by systems in Cluster 

   This column chart represents Wall Hours among systems (nodes).
