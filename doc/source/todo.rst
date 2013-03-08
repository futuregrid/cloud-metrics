**********************************************************************
REST: I FOUND THIS IN SOME OTHER FILE
**********************************************************************
Not sure if this is redundant or provides real additional
information. If it does, i suggest to include in main section.


Eucalyptus 2.0 Data Integration
======================================================================

To achieve analysis of eucalyptus data, we are using 'cc.log'
files. The needed information must be gathered while eucalyptus runs
in 'EUCADEBUG' mode. We assume the following directory layout::

    ./futurgrid/
    ./futurgrid/bin - includes all commands needed to run the log analyzing
    ./futurgrid/lib - includes libraries that may be called from the bin files
    ./futurgrid/etc - location of configuration files
    ./futurgrid/www - location of the www files
    
    
TODO
----------------------------------------------------------------------

define variables::

    FG_LOG_ANALYZER_WWW_OUTPUT - location where the www files for display are stored
    FG_TMP - location where temporary files are located that are analyzed
    FG_DATA - location where the permanent data is being stored 
    FG_HOME_LOG_ANALYZER - is set to the location of the "futuregrid" directory.
    EUCALYPTUS_LOG_DIR - location where the eucalyptus log dirs are stored

We recommend that the FutureGrid directory is included in the PATH of
the shell that will run the commands.


