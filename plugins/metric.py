###### DEFAULT MODULES #####################################
import textwrap
from docopt import docopt
import inspect
import sys
import importlib
from cmd3.cyberaide.decorators import command
############################################################

# IMPORT PLUGIN MODULE #####################################
from fgmetric.shell.FGMetricAPI import FGMetricAPI
############################################################

class metric:

    def activate_metric(self):
        self.cmetrics = FGMetricAPI()

    @command
    def do_set(self, line, args):
        """
        Usage:
                set date    START_DATE END_DATE
                set metric  NAME [runtime|count|countuser]
                set [node|nodename|hostname]    NAME
                set [cloud|platform]            NAME
                set period  NAME [monthly|quarterly|weekly|daily]

        Set value for analysis

        Arguments:
            date        set date
            START_DATE  start date to analyze 
            END_DATE    end date to analyze
            metric      set metric
            node        set nodename
            NAME        value
            cloud       set cloud service [openstack|eucalyptus|nimbus]

        """
        print(args)
        #print(vars(self.cmetrics))
        #print(vars(self.cmetrics.search))
        if args["date"]:
            self.cmetrics.set_date(args["START_DATE"], args["END_DATE"])
        elif args["metric"]:
            self.cmetrics.set_metric(args["NAME"])
        elif args["cloud"] or args["platform"]:
            self.cmetrics.set_cloud(args["NAME"])
        elif args["node"] or args["nodename"] or args["hostname"]:
            self.cmetrics.set_hostname(args["NAME"])
        elif args["period"]:
            self.cmetrics.set_period(args["NAME"])

    ######################################################################
    # analyze commands
    ######################################################################

    @command
    def do_analyze(self, args, arguments):
        """
        Usage:
               analyze OWNERID METRIC --start START --end END 
               analyze METRIC --period [monthly|quarterly|weekly|daily]
               analyze METRIC --month MONTH
               analyze METRIC --year YEAR
               analyze

        Analyze the metric data

        Arguments:
            OWNERID    The portal id of cloud users
            METRIC     The metric to be analyzed ... what values does it have? ...
            START      The start time n the format YYYY-MM-DDThh:mm:ss
            END        The end time n the format YYYY-MM-DDThh:mm:ss
            MONTH      The month in 01,02, ..., 12
            YEAR       The year to analyze

        Options:
          --start     specifies the time when to start the analysis
          --end       specified the time when to end the analysis
          --year      the year
          --month     the month
          --period    the period

        """
        #print(arguments)
        #TEST ONLY
        if arguments["OWNERID"]:
            self.cmetrics.set_user(arguments['OWNERID'])
        if arguments["START"] and arguments["END"]:
            self.cmetrics.set_date(arguments["START"], arguments["END"])
        if arguments["METRIC"]:
            self.cmetrics.set_metric(arguments["METRIC"])
        #self.cmetrics.set_cloud(None) #TEST
        #self.cmetrics.set_hostname(None) #TEST
        self.cmetrics.set_period(self._get_period_name(arguments)) #TEST arguments["
        res = self.cmetrics.get_stats()
        print res

    def _get_period_name(self, arguments):
        if arguments["monthly"]:
            return "monthly"
        elif arguments["quarterly"]:
            return "quarterly"
        elif arguments["weekly"]:
            return "weekly"
        elif arguments["daily"]:
            return "daily"
        return None

    ######################################################################
    # CVS commands
    ######################################################################

    @command
    def do_table(self, args, arguments):
        """
        Usage:
               table FILENAME
               table --file FILENAME

        Export the data in cvs format to a file. Former cvs command

        Arguments:
            FILENAME   The filename

        Options:
          --filet     specifies the filename

        """
        print(arguments)

    ######################################################################
    # chart
    ######################################################################

    @command
    def do_chart(self, args, arguments):
        """
        Usage:
               chart [--dir DIR] --type (bar|line|column|pie|motion)
	             [--api (highchart|google|jquery|sparkline)] [FILENAME]

        Creates a chart of a given type

        Arguments:
            DIR       The directory into which the chart is written
	    FILENAME  The filename in which the chart is written.
	    
        Options:
          --dir        The directory
	  --type       The type of the chart
	  --api        The chart api library
	  
        """
        print(arguments)


    ######################################################################
    # count images
    ######################################################################

    @command
    def do_count_images(self, line, opts=None):
        """
        Usage:
               count_images [--detail | --summary] --user USER 

	Count bucket images per user (development level). It is
        virtual machine image counts grouped by users or accounts
        based on euca2ools.  It shows that which user or account
        currently owns how many virtual machine images on the system.
        This metric is based on the euca2ool command.
	euca-describe-images. that a eucalyptus user can see a list
        of machine images.

        Arguments:
            USER       The user
	    
        Options:
          --user       Show only images from the specified userid.
	  --detail     Show details of the image (What would that be?)
	  --summary    show summary about the image (default)    
	  
        """
        print(arguments)
