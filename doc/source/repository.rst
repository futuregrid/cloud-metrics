Directory Structure
======================================================================

We have designed a directory layout as follows:

.. blockdiag::

          blockdiag {
          cloud-metrics -> data;
          cloud-metrics -> doc;
          cloud-metrics -> doc-old;
          cloud-metrics -> draft;
          cloud-metrics -> etc;
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
                  label="";
                  etc
                  }
                  group {
                  label="";
                  examples
                  }
                  group {
                  label="";
                  fghpc
                  }
                  group {
                  label="";
                  fgmetric
                  }
                  group {
                  label="";
                  fgmonitor
                  }
                  group {
                  label="";
                  fgweb
                  }
                  group {
                  label="";
                  fgws
                  }
                  group {
                  label="";
                  lighttpd
                  }
                  group {
                  label="";
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

