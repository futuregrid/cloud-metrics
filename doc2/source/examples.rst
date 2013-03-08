Examples
============================

.. sidebar:: 
   . 

  .. contents:: Table of Contents
     :depth: 3


..


 
Create a summary table for the month of January
----------------------------------------------------------------------


The following will create a table with data produced for the month of January::

    > fg-metric
    fg> clear users
    fg> analyze -M 01
    fg> table --type users --separator ,  --caption Testing_the_csv_table
    fg> quit

Naturally you could store this script in a file and pipe to fg-metric
in case you have more complex or repetitive analysis to do. 

How to create a summary analysis for multiple month
----------------------------------------------------------------------

Assume you like to create a nice html page directory with the analysis
of the data contained. This can be done as follows. Assume the following 
contents is in the file analyze.txt::

    clear users
    analyze -M 01 -Y 2012
    createreport -d 2012-01 -t Running_instances_per_user_of_Eucalyptus_in_India
    
    clear users
    analyze -M 02 -Y 2012
    createreport -d 2012-01 -t Running_instances_per_user_of_Eucalyptus_in_India
  
    createreports 2012-01 2012-02

This page creates a beautiful report page with links to the generated
graphs contained in the directories specified. All index files in
the directories are printed before the images in the directory are
included. The resulting report is an html report.

To start the script, simply use::

    cat analyze.txt | fg-metric

This will produce a nice directory tree with all the data needed for a
display.



Examples
----------------------------------------------------------------------

`example.txt <./examples/example1.txt>`_
* ????

[example2.txt](./examples/example2.txt)
* ????

[test.txt](./examples/test.txt)
* ????


WHY ARE YOU USING md syntax, but we use rst ?



