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
                  label="";
                  data
                  }
                  group {
                  label="Documentation";
                  doc 
                  }
                  group {
                  label="out-dated documentation";
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
                  label="Real-time monitoring for HPC";
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
                  label="CherryPy version of CloudMetrics";
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
                  label="Sphinx pages for statistics";
                  results
                  }
                  group {
                  label="";
                  todo
                  }
                  group {
                  label="";
                  www
                  }
           }

