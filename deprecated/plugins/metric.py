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
from fgmetric.charts.FGCharts import FGCharts
############################################################

class metric:

    def activate_metric(self):
        self.cmetrics = FGMetricAPI()
        self.chart = FGCharts()

    @command
    def do_set(self, line, args):
        """
        Usage:
                set date    START_DATE END_DATE
                set metric  (runtime|count|countusers)
                set (node|nodename|hostname) NODE_NAME
                set (cloud|platform) CLOUD_NAME
                set period  (monthly|quarterly|weekly|daily)

        Set value for analysis

        Arguments:
            START_DATE  start date to analyze 
            END_DATE    end date to analyze
            NODE_NAME   set hostname
            CLOUD_NAME  set cloud service [openstack|eucalyptus|nimbus]

        """
        print(args)
        #print(vars(self.cmetrics))
        #print(vars(self.cmetrics.search))
        if args["date"]:
            self.cmetrics.set_date(args["START_DATE"], args["END_DATE"])
        elif args["metric"]:
            self.cmetrics.set_metric(self._get_keyname(args, "runtime|count|countusers"))
        elif args["cloud"] or args["platform"]:
            self.cmetrics.set_cloud(args["CLOUD_NAME"])
        elif args["node"] or args["nodename"] or args["hostname"]:
            self.cmetrics.set_hostname(args["NODE_NAME"])
        elif args["period"]:
            self.cmetrics.set_period(self._get_keyname(args, "monthly|quarterly|weekly|daily"))

    def _get_keyname(self, args, slist):
        for i in slist.split("|"):
            if args[i]:
                return i
        return None

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
        if arguments["--period"]:
            self.cmetrics.set_period(self._get_keyname(arguments, "monthly|quarterly|weekly|daily")) #TEST arguments["
        res = self.cmetrics.get_stats()
        print res

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
    def do_chart(self, line, args):
        """
        Create a chart of a given type

        Usage:
            chart -t (bar|line|column|pie|motion|line-time-series) [-d DIR | --directory=DIR]
            chart --type (bar|line|column|pie|motion|line-time-series) [-d DIR | --directory=DIR]
	    chart --api (highcharts|google|jquery|sparkline)

        Options:
          -d DIR --directory=DIR  The directory [default: ./]
	  
        """
        print(args)
        if args["--api"]:
            api = self._get_keyname(args, "highcharts|google|jquery|sparkline")
        else:
            api = "highcharts"
        self.chart.set_chart_api(api)
        if args["-t"] or args["--type"]:
           self.chart.set_type(self._get_keyname(args, "bar|line|column|pie|motion|line-time-series"))
        if args["--directory"]:
           self.chart.set_output_path(args["--directory"])
        self.chart.set_filename( "TEST." + self.chart.output_type)
        self.chart.set_series(self.cmetrics.get_series())
        self.chart.set_title("TEST")
        self.chart.display()
        #self.chart.set_title_beta(', '.join(self.search.metric), self.search.period, self.search.groupby)
        #self.chart.set_subtitle("source: " + str(self.search.get_platform_names()) + " on " + str(self.search.get_node_names()))
        #self.chart.set_yaxis(self.search.timetype or "")

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
