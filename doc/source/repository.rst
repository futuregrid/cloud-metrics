Directory Structure
======================================================================

We have designed a directory layout as follows:

.. blockdiag::

          blockdiag {
          cloud-metrics -> data;
          cloud-metrics -> doc;
          cloud-metrics -> doc-old;
          cloud-metrics -> draft;
          cloud-metrics -> misc;
          cloud-metrics -> examples;
          cloud-metrics -> fghpc;
          cloud-metrics -> fgmetric;
          cloud-metrics -> fgmonitor;
          cloud-metrics -> fgweb;
          cloud-metrics -> fgws;
          cloud-metrics -> lighttpd;
          cloud-metrics -> results;  
          cloud-metrics -> todo;
          cloud-metrics -> www;

                  group {
                  label="png files";
                  data
                  }
                  group {
                  label="Documentation";
                  doc 
                  }
                  group {
                  label="outdated documentation";
                  doc-old
                  }
                  group {
                  label="Software development plans";
                  draft
                  }
                  group {
                  label="miscellaneous files";
                  misc
                  }
                  group {
                  label="Examples for CloudMetrics CLI";
                  examples
                  }
                  group {
                  label="HPC Real-time monitoring";
                  fghpc
                  }
                  group {
                  label="Main development";
                  fgmetric
                  }
                  group {
                  label="Real-time monitoring";
                  fgmonitor
                  }
                  group {
                  label="CherryPy of CloudMetrics";
                  fgweb
                  }
                  group {
                  label="Flask WSGI service";
                  fgws
                  }
                  group {
                  label="lighttpd";
                  lighttpd
                  }
                  group {
                  label="Sphinx for statistics";
                  results
                  }
                  group {
                  label="outdated";
                  todo
                  }
                  group {
                  label="outdated";
                  www
                  }
           }


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
