TODO
===========

.. sidebar:: 
   Metrics 

  .. contents:: Table of Contents
     :depth: 3

List
----------------------------------------------------------------------

.. todolist::


Observations
----------------------------------------------------------------------

.. todo:: integrate fg-=cleanup into fg-metric shell

There is little need to have a second command to cleanup the table, this
should become a plugin to the shell and be called with

fg-metric database .....

with the parameters from fg-clean-table


Examples
----------------------------------------------------------------------

what is here cmd? 

Show machine image counts for Eucalyptus
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. todo:: Hyungro, its unclear to me where this code is and how i
              can access it through the shell

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


Showing only image numbers owned by the userid specified::
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    (Cmd) count_image -u jdiaz
    jdiaz   7
   
Displaying details about images::
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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

Displaying summary values about images
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
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

 

