PDF Report 
===========================

PDF Report generates Cloud Usage Reports with Sphinx PDF generation with latex and Restructured Text. PDF Report allows you to automate document generation in a PDF format.

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

Add Ons to be included
-----------------------

1) command to create a report by resource and period

report -resource sierra -service eucalyptus -from ??:??:?? -to ??:??:?? 

report -summary -resource sierra india -service eucalyptus openstack -from ??:??:?? -to ??:??:?? 
report -summary -resource sierra -service openstack -from ??:??:?? -to ??:??:?? 
report -summary -resource sierra -service eucalyptus -from ??:??:?? -to ??:??:?? 


possibly add format to the command 

-format pdf
-format sphinx
-format html       ?
