Metrics on CLI
==============

.. sidebar:: 
   Metrics 

  .. contents:: Table of Contents
     :depth: 3

Cloud Metrics supports Command Line Interface (CLI), interactive shells for cloud usage data analysis. It is designed to read a user's input, calculate metrics, and then provide the results in an appropriate format such as a standard output (STDOUT), JSON, JPG, PNG, and html with javascript charting libraries.

.. There are currently eight different metrics to deliver system utilization, user activities and statistics. These statistical data are collected from log files which contain trackable information and from administrative command tools like euca2ools. The metrics system has simple operations to measure specific items such as virtual machine (VM) instances, registered VM images, virtual system resources, etc and there are count, average, sum, max, and min functions. In this section, you can find descriptions, instructions, and examples for the metrics.

Usage
-----

::

 $ fg-metric-beta
 fg-metric] set nodename india
 fg-metric] set platform openstack
 fg-metric] set metric runtime
 fg-metric] analyze
 fg-metric] chart 

Settings
---------

Before to perform analysis, several settings can be specified to narrow results. ``set`` is a main command for settings and it comes with two parameters: ``key`` and ``value`` at least.

``fg-metric] set $key $value[ $value2 ...]``

1. Set date
  Analyze data between these two dates.

::
 
  fg-metric] set date 2012-01-01T00:00:00 2012-12-31T23:59:59

2. Set metric
  Specify which metric item will be calculated.

::

  fg-metric] set metric runtime

  (multiple metrics)
  fg-metric] set metric runtime count

3. Set hostname
  Specify which machine will be included.

::

  fg-metric] set hostname india

4. Set cloud service
  Specify which cloud service will be included.

::

  fg-metric] set platform openstack


``help`` command is useful to understand how to use them.

* Example 1. help

::

  fg-metric] help

  Documented commands (type help <topic>):
  ========================================
  _load           clear           edit     l     pause    run      shell
  _relative_load  cmdenvironment  get      li    py       save     shortcuts
  analyze         csv             hi       list  r        set      show
  chart           ed              history  load  refresh  setconf  showconf

  Undocumented commands:
  ======================
  EOF  eof  exit  help  q  quit

* Example 2. help for a command

::

  fg-metric] help set
  Set a function with parameter(s)

  fg-metric] set help

  Possible commands
  =================
  set date $from $to
  set metric $name
  set platform $name
  set nodename $name

* Example 3. help for a command parameter

::

  fg-metric] set date help
  Usage: set date from_date(YYYY-MM-DDTHH:MM:SS) to_date(YYYY-MM-DDTHH:MM:SS). 
  (e.g. set date 2012-01-01T00:00:00 2012-12-31T23:59:59)

Results
-----------------------------------------------------------------
Cloud Metrics supports several output options such as stdout, JSON, csv, jpg, png, html.

Chart library
^^^^^^^^^^^^^
``chart`` is a command to create a chart html file with different chart types (e.g. bar, line, column, etc.).
To help understanding of data, a type of charts should be selected carefully. Relationships between data and chart type refer to proper representation.

Let's say, the data is:

* historical representation of quantity, then the type of chart should be => a line chart with x-axis as date and y-axis as quantity.
  - daily metrics 
* just quantities of different groups, then the type of chart should be => a pie chart
  - comparison across cloud services, locations, projects.

Example usage of ``chart`` command

::

  fg-metric] ...(skipped)...
  fg-metric] analyze
  fg-metric] chart -t pie-basic --directory $directory_name

CSV file
^^^^^^^^
``csv`` ia a command to export statistics as a comma-separated values (csv) file.

Example usage of ``csv`` command

::

  fg-metric] ...(skipped)...
  fg-metric] analyze
  fg-metric] csv
  2012-01-01T00:00:00-2013-01-01T00:00:00-runtime-openstack-india-dailyAll.csv is created

  (or)
  fg-metric] csv -o test/result.csv
  test/result.csv is created

Examples of using metrics
-------------------------

Some examples would be helpful to understand as how to generate statistics.

Daily active user count
^^^^^^^^^^^^^^^^^^^^^^^

This example shows you how to represent data in a certain time period.
``set period daily`` provides statistics grouped by date. For example, if the date settings cover 30 days, the statistics will have 30 record sets instead of a single record.
Chart type can be selected by ``chart -t`` option. ``line-time-series`` is one of the types in highcharts. For more details of the types, see here: `Highchart Demo <http://www.highcharts.com/demo/>`_.

::

 clear
 set nodename %(hostname)s
 set platform %(service)s
 set date %(from_dateT)s %(to_dateT)s
 set period daily
 set metric countusers
 analyze
 chart -t line-time-series --directory %(output_directory)s

Result html page

.. figure:: _static/examples/daily_active_user_count.png
   :scale: 70 %
   :alt: Daily active user count

   Figure 1. The count of active users

   This time series chart represents daily active user counts for cloud services and shows historical changes during the period.

VMs count by Project
^^^^^^^^^^^^^^^^^^^^^

This example represents data in percentages for different project groups. In this example, we use ``groupby`` instead of ``period`` in the previous example.

::

 clear
 set nodename %(hostname)s
 set platform %(service)s
 set date %(from_dateT)s %(to_dateT)s
 set groupby project
 set metric count
 analyze
 chart -t pie-basic --directory %(output_directory)s

Result html page

.. figure:: _static/examples/vms_count_by_project.png
   :scale: 70 %
   :alt: VMs count by Project

   Figure 2. VMs count by Project

   This pie chart illustrates propotion of Launched VM instances by Project groups. To represent certain information, the table follows.

Three metrics in a single chart
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example represents multiple data in a single chart with multiple axes. ``combo-multi-axes`` allows to depict three metrics in a single chart.

::

 clear
 set nodename %(hostname)s
 set platform %(service)s
 set date %(from_dateT)s %(to_dateT)s
 set period monthly
 set metric runtime count countusers
 set timetype hour
 analyze
 chart -t combo-multi-axes --directory %(output_directory)s

Result html page

.. figure:: _static/examples/three_metrics_in_a_single_chart.png
   :scale: 70 %
   :alt: Average Monthly Usage Data (Wall hour, Launched VMs, Users)

   Figure 3. Average Monthly Usage Data (Wall hour, Launched VMs, Users)

   This mixed chart represents average monthly usage as to Wall Hour (runtime), Count and the number of Users for VM instances.

