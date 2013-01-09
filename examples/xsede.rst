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
.. image:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-runtimecountcountusers-%(service)s-%(hostname)s-monthlyAll.png
Figure 1: Average Usage Data (Wall hour, Launched VMs, Users)

Summary (Daily)
^^^^^^^^^^^^^^^^^^^
.. image:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-countusers-%(service)s-%(hostname)s-dailyAll.png
Figure 2: Users count

.. image:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-count-%(service)s-%(hostname)s-dailyAll.png
Figure 3: VMs count

.. image:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-runtime-%(service)s-%(hostname)s-dailyAll.png
Figure 4: Wall Hours

Distribution
------------

.. image:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-count-%(service)s-%(hostname)s-walltimeAll.png
Figure 5: VM count by Wall Hours

.. image:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-count-%(service)s-%(hostname)s-projectAll.png
Figure 6: VMs count by Project

.. csv-table:: VMs count by Project
        :file: ../../%(output_directory)s/%(from_dateT)s-%(to_dateT)s-count-%(service)s-%(hostname)s-projectAll.csv

.. image:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-count-%(service)s-%(hostname)s-projectleaderAll.png
Figure 7: VMs count by Project Leader

.. csv-table:: VMs count by Project Leader
        :file: ../../%(output_directory)s/%(from_dateT)s-%(to_dateT)s-count-%(service)s-%(hostname)s-projectleaderAll.csv

.. image:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-count-%(service)s-%(hostname)s-institutionAll.png
Figure 8: VMs count by Institution 

.. csv-table:: VMs count by Institution
        :file: ../../%(output_directory)s/%(from_dateT)s-%(to_dateT)s-count-%(service)s-%(hostname)s-institutionAll.csv

.. image:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-runtime-%(service)s-%(hostname)s-projectleaderAll.png
Figure 9: Wall Hours by Project Leader

System information
-------------------

.. image:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-count-%(service)s-%(hostname)s-serviceTag.png
Figure 10: VMs count by systems in Cluster 

.. image:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-runtime-%(service)s-%(hostname)s-serviceTag.png
Figure 11: Wall Hours by systems in Cluster 
