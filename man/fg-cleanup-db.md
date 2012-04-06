NAME
====

 **fg-cleanup-table** - delete database records of MySQL

SYNOPSIS
========

 **fg-cleanup-table** [OPTION]...

DESCRIPTION
===========
Delete table records in which -t table name and -d database name are spe
cified. Default table name is 'instance' and database name is 'euca'. My
SQL user and password information are from the configuration file. Condi
tions can be specified by -w where_condition option.

**-t tbl_name**
deletes rows from tbl_name

-d db_name
a database name of a table specified by -t tbl_name

-w where_condition (optional)
specifies the conditions that identify which rows to delete

-C, --conf filename
configuraton file of the database to be used. The configuration file has the 
following format
 	   
    [EucaLogDB]
    host=HOST
    port=PORT
    user=USER
    passwd=PASS
    db=DB
 	   
if this parameter is not specified and a database is used the default
location for this file is in
 	   
    ~/.futuregrid/futuregrid.cfg

EXAMPLES
========

Delete all records in a default table and database with default configuration fi
le

    $ fg-cleanup-table

Delete all records in a specific table

    $ fg-cleanup-table -t table_name

Delete all records in a specific table and a specific database

    $ fg-cleanup-table -t table_name -d db_name

Delete records with a different configuration file (~/futuregrid.cfg)

    $ fg-cleanup-table --conf ~/futuregrid.cfg

Delete records with where clause

    $ fg-cleanup-table -w "instanceId = i-534109B6"

AUTHOR
======

Written by H. Lee, Fugang Wang and Gregor von Laszewski.

REPORTING BUGS
==============

Report fg-cleanup-table bugs to laszewski@gmail.com
Github home page: <https://github.com/futuregrid/futuregrid-cloud-metrics>

COPYRIGHT
=========

SEE ALSO
========
