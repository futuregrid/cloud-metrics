============
count_images
============


Commands
========

count_images
------------

Description
~~~~~~~~~~~
count_images generates a bar chart about virtual machine image count per users or accounts. The image count is 
calulated by the euca-describe-images Eucalyptus cmd2ools. It provides a current status when it is executed.

**Note**
        Why we count images?
                It is a simple approach to show how many virtual machine images are currently registered by users or accounts.

**Note**
        What is an Account?
                | Accounts are the primary unit for resource usage accounting. Each account is a separate name space and is 
                | identified by its UUID (Universal Unique Identifier). Tasks performed at the account level can only be done by the 
                | users in the eucalyptus account [1]. For example, .fg82. has .281408815495. account id and all users in .fg82. 
                | group can use this account id for the image management.

**Note**
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

Dictionary for metrics
----------------------
