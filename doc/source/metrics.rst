Metrics
=======
There are currently eight different metrics to deliver system utilization, a user activity and statistics. These statistical data are collected from log files which contain trackable information and from administrative command tools like euca2ools. The metrics system has simple operations to measure specific items such as used VM instances, registered bucket VM images, used virtual system resources, etc and there are count, average, sum, max, and min functions. In this section, there are descriptions, instructions, examples and manuals for the metrics.

Current metrics
---------------
1. The number of VM instances used by a user
        It is virtual machine instance counts grouped by users or accounts based on log files of eucalyptus. It shows a user's activity and a system utilization by counting launched VM instances during a certain period.
        
2. The total runtime of VM instance used by a user
        It is the total running time for virtual machine instances grouped by users or accounts based on log files of eucalyptus. It shows the amount of resources used by users and a system utilization by adding up the total lifetime of instances during a certain period.

3. A count of VM images owned by a user (euca-describe-images)
        It is virtual machine image counts grouped by users or accounts based on euca2ools. It shows that which user or account currently owns how many virtual machine images on the system. This metric is based on the euca2ool command *euca-describe-images* that a eucalyptus user can see a list of machine images. For example in Eucalyptus 3.0, the euca-describe-images generates information like below.
         ::

         $ euca-describe-images
         IMAGE emi-0E19393A jdiaz/ubuntuprecisejdiaz2122518911.img.manifest.xml 281408815495 available public i386 machine eki-226638E6 eri-32DE3771 instance-store
         IMAGE eri-4E163AA8 ramdik/initrd.img-2.6.28-11-generic.manifest.xml 000000000001 available public i386 ramdisk instance-store

4. The total number of VM instances used in a system
        It is 
5. Total runtime of VM instances used in a system
6. Total CPU cores of VM instances used in a system
7. Total memories of VM instances used in a system
8. Total disks of VM instances used in a system

Examples
--------

Dictionary for metrics
----------------------

Commands
========

count_images
------------

Description
~~~~~~~~~~~
count_images generates a bar chart about virtual machine image counts per users or accounts. The image counts are 

calulated by the euca-describe-images Eucalyptus cmd2ools. It provides a current status when it is executed.

Note
~~~~
Why we count images?
It is a simple approach to show how many virtual machine images are currently registered by users or accounts.

Note
~~~~
What is an Account?
Accounts are the primary unit for resource usage accounting. Each account is a separate name space and is 

identified by its UUID (Universal Unique Identifier). Tasks performed at the account level can only be done by the 

users in the eucalyptus account [1]. For example, .fg82. has .281408815495. account id and all users in .fg82. 

group can use this account id for the image management.

Note
~~~~
Is there any prerequisite condition to run this new metric?
In order to execute euca2ools e.g. euca-describe-images, a user should read config and credentials from the config file i.e. eucarc. If a user already set up euca2ools properly, there should be no problem to have the new metric.

Syntax
~~~~~~

Options
~~~~~~~

Common options
~~~~~~~~~~~~~~

Output
~~~~~~

Graph
~~~~~
bar chart

Examples
~~~~~~~~
