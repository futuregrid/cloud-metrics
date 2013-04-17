.. =================================================================================================
.. MAIN TEMPLATE

.. This will be iterated by services and hosts when they are specified.
.. For example, if nimbus, hotel, alamo, foxtrot, sierra specified, this MAIN TEMPLATE will be generated
.. in 4 different rst files

.. Hyungro Lee (lee212@indiana.edu)
.. 01/11/2013
.. FutureGrid project
.. =================================================================================================

.. Usage Report for %(service)s on %(hostname)s
Usage Report %(hostname)s
================================================================

- Period: %(tmpl_period)s
- Hostname: %(hostname)s.futuregrid.org
- Services: %(service_name)s
- Metrics: VMs count, Users count, Wall time (hours), Distribution by wall time, project, project leader, and institution, and systems

Histogram
---------

Summary (Monthly)
^^^^^^^^^^^^^^^^^^^^^

.. Summary chart for services on systesms
.. ================================================================================================================
.. 1) WALL HOURS / VM COUNT / COUNT USERS (MIXED)
.. ================================================================================================================

.. image:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-runtimecountcountusers-%(service)s-%(hostname)s-monthlyAll.png
   :alt: Average Monthly Usage Data (Wall time, Launched VMs, Users)
   
| Figure 1: Average monthly usage data (wall time (hour), launched VMs, users)
| This mixed chart represents average monthly usage as to wall time (hour), the number of VM instances and active users.

- Period: %(tmpl_period)s
- Cloud(IaaS): %(service_name)s
- Hostname: %(hostname)s
- Metric:
   - Runtime (Wall time hours): Sum of time elapsed from launch to termination of VM instances
   - Count (VM count): The number of launched VM instances
   - User count (Active): The number of users who launched VMs

.. +-------------+-------------------------------------+
.. | Metric      | Description                         |
.. +=============+=====================================+
.. | Wall Hour   | Terminated time - Launched time     |
.. +-------------+-------------------------------------+
.. | count       | The number of launched VM instances |
.. +-------------+-------------------------------------+
.. | user count  | The number of users who launched VMs|
.. +-------------+-------------------------------------+

Summary (Daily)
^^^^^^^^^^^^^^^^^^^

.. ================================================================================================================
.. 2) USERS COUNT (Daily)
.. ================================================================================================================

.. image:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-countusers-%(service)s-%(hostname)s-dailyAll.png
   :alt: Users count (daily)
   :align: left

| Figure 2: Users count
| This time series chart represents daily active user count for cloud services and shows historical changes during the period.

- Period: %(tmpl_period)s
- Cloud(IaaS): %(service_name)s
- Hostname: %(hostname)s


.. ================================================================================================================
.. 3) VM COUNT (DAILY)
.. ================================================================================================================

.. image:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-count-%(service)s-%(hostname)s-dailyAll.png
   :alt: VMs count (daily)

| Figure 3: VMs count
| This time series chart represents the number of daily launched VM instances for cloud services and shows historical changes during the period.

- Period: %(tmpl_period)s
- Cloud(IaaS): %(service_name)s
- Hostname: %(hostname)s


.. ================================================================================================================
.. 4) WALL TIME (HOURS, DAILY)
.. ================================================================================================================

.. image:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-runtime-%(service)s-%(hostname)s-dailyAll.png
   :alt: Wall time (hours, daily)

| Figure 4: Wall time (hours)
| This time series chart represents daily wall time (hours) for cloud services and shows historical changes during the period.

- Period: %(tmpl_period)s
- Cloud(IaaS): %(service_name)s
- Hostname: %(hostname)s


Distribution
------------

.. ================================================================================================================
.. 5) VM COUNT BY WALL TIME
.. ================================================================================================================

.. image:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-count-%(service)s-%(hostname)s-walltimeAll.png
   :alt: VM count by wall time

| Figure 5: VM count by wall time
| This chart illustrates usage patterns of VM instances in terms of running wall time.

- Period: %(tmpl_period)s
- Cloud(IaaS): %(service_name)s
- Hostname: %(hostname)s


.. ================================================================================================================
.. 6) VMs count by Project
.. ================================================================================================================

.. image:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-count-%(service)s-%(hostname)s-projectAll.png
   :alt: VMs count by project

| Figure 6: VMs count by project
| This chart illustrates the proportion of launched VM instances by project groups. The same data in tabular form follows.

- Period: %(tmpl_period)s
- Cloud(IaaS): %(service_name)s
- Hostname: %(hostname)s

.. csv-table:: VMs count by project
   :file: ../../%(output_directory)s/%(from_dateT)s-%(to_dateT)s-count-%(service)s-%(hostname)s-projectAll.csv
   :header-rows: 1

.. ================================================================================================================
.. 7) VM COUNT BY PL
.. ================================================================================================================

.. image:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-count-%(service)s-%(hostname)s-projectleaderAll.png
   :alt: VMs count by project leader

| Figure 7: VMs count by project leader
| This chart also illustrates the proportion of launched VM instances by project Leader. The same data in tabular form follows.

- Period: %(tmpl_period)s
- Cloud(IaaS): %(service_name)s
- Hostname: %(hostname)s

.. csv-table:: VMs count by project leader
   :file: ../../%(output_directory)s/%(from_dateT)s-%(to_dateT)s-count-%(service)s-%(hostname)s-projectleaderAll.csv
   :header-rows: 1

.. ================================================================================================================
.. 8) VM COUNT BY INSTITUTION
.. ================================================================================================================

.. image:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-count-%(service)s-%(hostname)s-institutionAll.png
   :alt: VMs count by institution 

| Figure 8: VMs count by institution 
| This chart illustrates the proportion of launched VM instances by Institution. The same data in tabular form follows.

- Period: %(tmpl_period)s
- Cloud(IaaS): %(service_name)s
- Hostname: %(hostname)s

.. csv-table:: VMs count by institution
   :file: ../../%(output_directory)s/%(from_dateT)s-%(to_dateT)s-count-%(service)s-%(hostname)s-institutionAll.csv
   :header-rows: 1

.. ================================================================================================================
.. 9) WALL HOURS BY PL
.. ================================================================================================================

.. image:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-runtime-%(service)s-%(hostname)s-projectleaderAll.png
   :alt: Wall time (hours) by project leader

| Figure 9: Wall time (hours) by project leader
| This chart illustrates proportionate total run times by project leader.

- Period: %(tmpl_period)s
- Cloud(IaaS): %(service_name)s
- Hostname: %(hostname)s


System information
-------------------
System information shows utilization distribution as to VMs count and wall time. Each cluster represents a compute node.

.. ================================================================================================================
.. 10) VM COUNT BY NODES
.. ================================================================================================================

.. image:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-count-%(service)s-%(hostname)s-serviceTag.png
   :alt: VMs count by systems in Cluster (%(hostname)s)

| Figure 10: VMs count by systems (compute nodes) in Cluster (%(hostname)s)
| This column chart represents VMs count among systems.

- Period: %(tmpl_period)s
- Cloud(IaaS): %(service_name)s
- Hostname: %(hostname)s


.. ================================================================================================================
.. 11) wall time BY NODES
.. ================================================================================================================

.. image:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-runtime-%(service)s-%(hostname)s-serviceTag.png
   :alt: Wall time (hours) by systems in Cluster (%(hostname)s)

| Figure 11: Wall time (hours) by systems (compute nodes) in Cluster (%(hostname)s)
| This column chart represents wall time among systems.

- Period: %(tmpl_period)s
- Cloud(IaaS): %(service_name)s
- Hostname: %(hostname)s

