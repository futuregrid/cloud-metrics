Metrics 
==============

.. sidebar:: 
   Metrics 

  .. contents:: Table of Contents
     :depth: 3

Cloud Metrics supports a convenient shell to aide in the cloud usage
data analysis. It is advisable that users use the shell in case you
like to conduct multiple analysis steps.  The shell is designed to
read a user's input, calculate metrics data, and then provide the
results in an appropriate format such as a standard output, JSON, JPG,
PNG, and html with javascript charting libraries embedded

.. There are currently eight different metrics to deliver system utilization, user activities and statistics. These statistical data are collected from log files which contain trackable information and from administrative command tools like euca2ools. The metrics system has simple operations to measure specific items such as virtual machine (VM) instances, registered VM images, virtual system resources, etc and there are count, average, sum, max, and min functions. In this section, you can find descriptions, instructions, and examples for the metrics.

Starting the cloud metric shell
----------------------------------------------------------------------

To activate the metric shell please execute the command::

 $ fg-metric

Once you do this you can issue some of the metric shell commands. Here
is a simple example that analyzes the runtime metric for a machine
india on which openstack is installed and prints a chart::

 fg-metric> set nodename india
 fg-metric> set platform openstack
 fg-metric> set metric runtime
 fg-metric> analyze
 fg-metric> chart 

The  "set" Command
-------------------------------------------------------------------------------

Before performing an analysis, several settings need to be specified
with the ``set`` command. This command allows to associate
one or more values with a key::

  fg-metric> set $key $value[ $value2 ...]

Set the date range
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To analyze data between these two dates please set the date range::
 
  fg-metric> set date 2012-01-01T00:00:00 2012-12-31T23:59:59


Set the metric
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
To specify  which metric item will be calculated please set it as follows::

  fg-metric> set metric runtime

  (multiple metrics)
  fg-metric> set metric runtime count

We are supporting the following metrics:

::
 
 fg-metric> set metric help
 Possible commands
 =================
  set metric count
  set metric runtime
  set metric countusers
  set metric cores
  set metric runtimeusers
  set metric memories
  set metric disks

Set the hostname
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
As our metric system can handle multiple coulds, it is important to
set for which host the calculations are to be specified. Please set it
ass follows where the name india is your machine that holds the IaaS::

  fg-metric> set hostname india


Set the cloud service
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To specify which cloud service will be included please use the
following command::

  fg-metric> set platform openstack

The "help" command
----------------------------------------------------------------------


The ``help`` command is useful to obtain a simple help message for the
available commoand::

  fg-metric> help

  Documented commands (type help <topic>):
  ========================================
  _load           clear           edit     l     pause    run      shell
  _relative_load  cmdenvironment  get      li    py       save     shortcuts
  analyze         csv             hi       list  r        set      show
  chart           ed              history  load  refresh  setconf  showconf

  Undocumented commands:
  ======================
  EOF  eof  exit  help  q  quit

.. note:: TODO: document the undocumented commands and include new output here once done.

To find out more details about an available shell command, simply type
in help followed by the command::

  fg-metric> help set
  Set a function with parameter(s)

  fg-metric> set help

  Possible commands
  =================
  set date $from $to
  set metric $name
  set platform $name
  set nodename $name

To ask for help for a parameter you can do this as follows (here we
give an example for finding mor out about the set data command::

  fg-metric> set date help
  Usage: set date from_date(YYYY-MM-DDTHH:MM:SS) to_date(YYYY-MM-DDTHH:MM:SS). 
  (e.g. set date 2012-01-01T00:00:00 2012-12-31T23:59:59)

The "analyze" command
----------------------------------------------------------------------

.. note:: TODO Hyungro

Once you conducted an analyze, cloud metrics supports several output
options such as stdout, JSON, csv, jpg, png, html that can be created
with the help of various commands such as chart and csv which we
describe next.

.. note:: TODO Hyungro, what about the other commands? I do not think they are listed here.

The "chart" command
----------------------------------------------------------------------

``chart`` is a command to create a chart html file with different
chart types (e.g. bar, line, column, etc.).  To help understanding of
data, a type of charts should be selected carefully. Relationships
between data and chart type refer to proper representation.

Assume, the data is:

* historical representation of quantity, then the type of chart should
  be => a line chart with x-axis as date and y-axis as quantity.
  - daily metrics 

* just quantities of different groups, then the type of chart should be => a pie chart
  - comparison across cloud services, locations, projects.

Example usage of the ``chart`` command::

  fg-metric> ...(skipped)...
  fg-metric> analyze
  fg-metric> chart -t pie-basic --directory $directory_name

The "csv" command
----------------------------------------------------------------------

``csv`` ia a command to export statistics as a comma-separated values (csv) file.

Example usage of ``csv`` command::

  fg-metric> ...(skipped)...
  fg-metric> analyze
  fg-metric> csv
  2012-01-01T00:00:00-2013-01-01T00:00:00-runtime-openstack-india-dailyAll.csv is created

  (or)
  fg-metric> csv -o test/result.csv
  test/result.csv is created

Examples of using the metric shell
----------------------------------------------------------------------

We show now some examples to highlight how easy it is to generate
statistics with the metric shell.

Daily active user count
^^^^^^^^^^^^^^^^^^^^^^^

This example shows you how to retrieve data for a certain time period.
``set period daily`` provides statistics grouped by date. For example,
if the date settings cover 30 days, the statistics will have 30 record
sets instead of a single record.  The chart type can be selected with
``chart -t`` option. ``line-time-series`` is one of the types in
highcharts. For more details of the types, see here: 
`Highchart Demo <http://www.highcharts.com/demo/>`_. In our example we
create a chart that represents for each day the number of users using
a cloud services in a histogram over the specified period (see Figure
1). Using the script::

 clear
 set nodename %(hostname)s
 set platform %(service)s
 set date %(from_dateT)s %(to_dateT)s
 set period daily
 set metric countusers
 analyze
 chart -t line-time-series --directory %(output_directory)s

will result in the following image:

.. figure:: _static/examples/daily_active_user_count.png
   :scale: 70 %
   :alt: Daily active user count

   Figure 1. The count of active users. 

VMs count by Project
^^^^^^^^^^^^^^^^^^^^^

This example represents data in percentages for different project
groups. In this example, we use ``groupby`` instead of ``period`` in
the previous example. It will result in a pie chart showing the
fractions  of Launched VM instances by Project groups (Figure
2). Using the script::

 clear
 set nodename %(hostname)s
 set platform %(service)s
 set date %(from_dateT)s %(to_dateT)s
 set groupby project
 set metric count
 analyze
 chart -t pie-basic --directory %(output_directory)s

will result in the following image:

.. figure:: _static/examples/vms_count_by_project.png
   :scale: 70 %
   :alt: VMs count by Project

   Figure 2. VMs count by Project. 

Three metrics in a single chart
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example represents multiple data in a single chart with multiple
axes. ``combo-multi-axes`` allows to depict three metrics in a single
chart.    Here we show a chart that includes average monthly usage as
to Wall Hour (runtime), Count and the number of Users for VM instances
(Figure 3). Using the script::

 clear
 set nodename %(hostname)s
 set platform %(service)s
 set date %(from_dateT)s %(to_dateT)s
 set period monthly
 set metric runtime count countusers
 set timetype hour
 analyze
 chart -t combo-multi-axes --directory %(output_directory)s

will result in the following image:


.. figure:: _static/examples/three_metrics_in_a_single_chart.png
   :scale: 70 %
   :alt: Average Monthly Usage Data (Wall hour, Launched VMs, Users)

   Figure 3. Average Monthly Usage Data (Wall hour, Launched VMs, Users)



