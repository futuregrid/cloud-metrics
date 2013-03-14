Directory Structure
======================================================================

We have designed a directory layout as follows:


.. csv-table:: Main directory structure of cloud metric 
   :header: Directory, Description
   :widths: 10, 50
                  
                  data, png files
                  doc , Documentation
                  doc-old, outdated documentation
                  draft, Software development plans
                  misc, miscellaneous files
                  examples, Examples for CloudMetrics CLI
                  fghpc, HPC Real-time monitoring
                  fgmetric, Main development
                  fgmonitor, Real-time monitoring
                  fgweb, CherryPy of CloudMetrics
                  fgws, Flask WSGI service
                  lighttpd, lighttpd
                  results, Sphinx for statistics
                  todo, outdated
		  deprecated, outdated


File contents
=============

::

  | FGAnalyzer.py - old version of metric analyzer
  | FGCollectFiles.py - log backup tool
  | FGConverter.py - data converting tool from Nimbus, Openstack to Cloud Metrics
  | FGEucaMetricsDB.py - old version of metrics db
  | FGHighcharts.py - Highcharts API
  | FGInstall.py - Initializer of Cloud Metrics (db configuration, etc)
  | FGLogParser.py - Eucalyptus log parser
  | FGMetricsCli.py - fg-metric-cli command tool
  | FGNovaDB.py - outdated OpenStack API
  | FGParser.py - old version of VM instance class
  | FGSearch.py - New version of 
  | FGTimeZone.py - TimeZone helper for managing timestamp in logs
  | FGCharts.py - Chart library API
  | FGConstants.py - Constants class
  | FGDatabase.py - New version of database class
  | FGGoogleMotionChart.py - Old version of Google Chart API
  | FGHighchartsTemplate.py - outdated Highcharts API
  | FGInstances.py - New version of VM instance class
  | FGMetricsAPI.py - New version of Metrics API class
  | FGMetrics.py - New version of main class of Cloud Metrics
  | FGNovaMetric.py - outdated OpenStack class for metric
  | FGPygooglechart.py - outdated python google chart API
  | FGTester.py - outdated Tester
  | FGUtility.py - Utility libraries
