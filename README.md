Report_eucalyptus_on_sierra
===========================

Prerequisite
------------
- phantomjs
- futuregrid/cloud-metrics

How to create report?
---------------------
``make report``

open pdf file under _build/latex directory

How to modify pages?
--------------------

Edit sierra.rst file

It is restructuredText file to be generated in a html or pdf file using Python Sphinx

How to modify command?
----------------------

Edit data.txt or report_euca_sierra_201207to12.txt

The file has the list of commands to generate charts that included in the report.
