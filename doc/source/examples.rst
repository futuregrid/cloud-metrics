Yet more Examples 
============================

that may have to be merged into metrics section

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

Create a summary analysis for multiple month
--------------------------------------------

Assume you like to create a nice html page directory with the analysis
of the data contained. This can be done as follows. Assume the
following contents is in the file analyze.txt::

    clear users
    analyze -M 01 -Y 2012
    createreport -d 2012-01 -t Running_instances_per_user_of_Eucalyptus_in_India
    
    clear users
    analyze -M 02 -Y 2012
    createreport -d 2012-01 -t Running_instances_per_user_of_Eucalyptus_in_India
  
    createreports 2012-01 2012-02

This page creates a beautiful report page with links to the generated
graphs contained in the directories specified. All index files in the
directories are printed before the images in the directory are
included. The resulting report is an html report.

To start the script, simply use::

    cat analyze.txt | fg-metric

This will produce a nice directory tree with all the data needed for a
display.

Show machine image counts for Eucalyptus
----------------------------------------

Based on Jonathan's code, we are able to get image counts via cmd2 tools.
It's established on 'euca-describe-images' command::

        (Cmd) count_images
        ...
        sazh72  1
        debian-rm1984   1
        pegasus-images  3
        wchen-server-stage-1    2
        ...

There are additional options which might be useful,

1. showing only image numbers owned by the userid specified::

    (Cmd) count_image -u jdiaz
    jdiaz   7
   
2. displaying details about images::

        (Cmd) count_images -u jdiaz -d
        jdiaz   7
        IMAGE   emi-1CA015A7    centos-image-bucket/centos.5-3.x86-64.img.manifest.xml  taklwu  available       public          x86_64  machine eki-78EF12D2    eri-5BB61255    instance-store
        IMAGE   emi-DBC4106B    ubuntu-0904-saga-1.5.2/image.manifest.xml       luckow  available       public          x86_64  machine eki-78EF12D2    eri-5BB61255    instance-store
        IMAGE   emi-F840162A    myubuntubucket/ubuntufloeserver.img.manifest.xml        sreedharnat1    available       public          x86_64  machine eki-78EF12D2    eri-5BB61255    instance-store
        IMAGE   eki-7A031340    mybucket/vmlinuz-2.6.28-11-generic.manifest.xml ajyounge        available       public          x86_64  kernel                  instance-store
        IMAGE   emi-E5D514DA    jdiaz/ubuntunattyjdiaz3595279807.img_0.manifest.xml     javidiaz        available       public          x86_64  machine eki-78EF12D2    eri-5BB61255    instance-store
        IMAGE   emi-46861248    jdiaz/centos6jdiaz2698814667.img.manifest.xml   javidiaz        available       public          x86_64  machine eki-78EF12D2    eri-5BB61255    instance-store
        IMAGE   emi-431F1230    jdiaz/centos6jdiaz2710350825.img.manifest.xml   javidiaz        available       public          x86_64  machine eki-78EF12D2    eri-5BB61255    instance-store
        IMAGE   emi-0E0E165E    ajyounge/ubuntu-twister-memcached.img.manifest.xml      ajyounge        available       public          x86_64  machine eki-78EF12D2    eri-5BB61255    instance-store
        IMAGE   emi-A5B6148A    ajyounge/ubuntu-lucid-minimal.img.manifest.xml  ajyounge        available       public          x86_64  machine eki-78EF12D2    eri-5BB61255    instance-store
        IMAGE   emi-4A051306    ajyounge/ubuntu-lucid-mpj.img.manifest.xml      ajyounge        available       public          x86_64  machine eki-78EF12D2    eri-5BB61255    instance-store
        IMAGE   emi-48141244    ajyounge/ajyounge-1563160039.img.manifest.xml   ajyounge        available       public          x86_64  machine eki-78EF12D2    eri-5BB61255    instance-store
        IMAGE   emi-FC6A1197    ajyounge/ubuntu-natty.img.manifest.xml  ajyounge        available       public          x86_64  machine eki-78EF12D2    eri-5BB61255    instance-store

3. displaying summary values about images.
    e.g. total image counts, total user counts, average image counts 
    per user, and maximum image counts and userid::

        (Cmd) count_images -s
        ...
        = Summary =
        Total image counts:     128
        Total user counts:      71
        Average image counts per user:  1.80281690141
        Maximum image counts and userid:        ajyounge has 12
        ==========

 
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



Yet another set of Examples Scripts copied from somewhere
--------------------------------------------------------------------------------

Please find a small set of example scripts. Example 2 is most
interesting as it produces output for multiple month on VM ussage and
wallclock time associated with the users

* `example1.txt <../../../examples/example1.txt>`_
* `example2.txt <../../../examples/example2.txt>`_
* `test.txt <../../../examples/test.txt>`_
