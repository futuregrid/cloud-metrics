from os.path import split
from cmd2 import Cmd, options, make_option
import sys
import optparse
import csv
import subprocess
from datetime import datetime
from calendar import monthrange
from pprint import pprint
from fgmetric.FGSearch import FGSearch
from fgmetric.FGInstances import FGInstances
from fgmetric.FGCharts import FGCharts
from fgmetric.FGDatabase import FGDatabase
from fgmetric.FGUtility import FGUtility

from bson import json_util
import json
import argparse
from pprint import pprint
from datetime import datetime, timedelta
from fgmetric.FGMetricsAPI import FGMetricsAPI

class FGMetrics(Cmd):

    instances = None
    search = None

    def __init__(self):
        Cmd.__init__(self)
        self.prompt = "fg-metric> "
        self.intro = "Welcome to FutureGrid Cloud Metrics!"

    def initialize(self, arg="all"):
        """Clear all instance data and user data on the memory"""
        self.search = FGSearch()
        self.chart = FGCharts()
        self.instances = FGInstances()
        self.instances.db.conf()
        self.instances.db.connect()

    def init_objects(self):
        self.search.__init__()
        self.chart.__init__()

    def load_db(self, option=None):
        """Read the statistical data from database (MySQL, etc)"""
       
        print "\rloading database ..."
        # Get data from the database
        self.instances.read_from_db()
        # Get also userinfo data from the database
        self.instances.read_userinfo_from_db()
        self.instances.read_projectinfo_from_db()
        print "\r... loaded"

    def show_dbinfo(self, param=None):
        pprint(vars(self.instances.db), indent=2)

    def show_filter_setting(self, param=None):
        pprint(vars(self.search.get_filter()))
        #res = vars(self.search.get_filter()).copy()
        #del res["selected"]
        #pprint(res)

    def measure(self):

        total_counts = self.instances.count()
        print "Calculating metrics in " + str(total_counts) + " records...\n"

        cnt = cnt2 = cnt3 = 0
        for i in range(0, total_counts):
            try:
                instance = self.instances.get_data(i, self.search._is_userinfo_needed())[0]
                cnt += 1
                if not self.search._is_in_date(instance):
                    continue;
                cnt2 += 1
                if not self.search._is_filtered(instance):
                    continue;
                cnt3 += 1
                res = self.search.collect(instance)

            except:
                #print sys.exc_info()
                pass#raise

        print self.search.get_metric()
        #print cnt, cnt2, cnt3

        '''
        I am where to create a dict/list for data of charts.
        what I need to do is
        1) choose which column that I need to collect. This should be done by the 'metric' filter
        2) get value from the instance
        3) create data structure for the result
        4) if it has a groupby(s), create multi-dimentional dict/list to save the value in a depth
           e.g. res[groupby1][groupby2] = 
           e.g. res = { groupby1 : { groupby2: val1, ... } }

        5) fill missing date? for chart format? this should be done by in a chart module
        6) convert the result data structure to chart formatted data
        '''

    def set_configfile(self, filename):
        self.instances.db.set_conf(filename)
        self.instances.db.update_conf()

        print filename + " loaded."
        print "refresh db may required."

    def create_csvfile(self, data, dirname="./", filename="default.csv"):

        try:
            writer = csv.writer(open(dirname + filename, 'wb'), delimiter=",",
                    quotechar="\"", quoting=csv.QUOTE_NONNUMERIC)#QUOTE_MINIMAL)
            for row in data:
                writer.writerow(row)

            msg = filename + " is created"
        except:
            msg = filename + " is not created"
            print sys.exc_info()
            pass

        print msg

    @options([
        make_option('-f', '--start_date', type="string", help="start time to analyze (type. YYYY-MM-DDThh:mm:ss)"),
        make_option('-t', '--end_date', type="string", help="end time to analyze (type. YYYY-MM-DDThh:mm:ss)"),
        make_option('-M', '--month', type="int", help="month to analyze (type. MM)"),
        make_option('-Y', '--year', type="int", help="year to analyze (type. YYYY)"),
        make_option('-m', '--metric', type="string", help="item name to measure (e.g. runtime, count)"),
        make_option('-P', '--period', type="string", help="search period (monthly, daily)")
        ])
    def do_analyze(self, line, opts=None):
        """Run analysis for cloud usage data. Parameters are not required if they are set.
        Usage 1: (analyze between $from_date and $to_date for $name metric)
            set date $from_date $to_date
            set metric $name
            analyze

        Usage 2:
            analyze -f $from_date -t $to_date -m $name

        Usage 3: (analyze $name metric in a selected year. -M $month option can be include)
            analyze -Y $year -m $name
        """
        """
        
        Typically, set platform ***, set nodename ***, set date ***  *** are required prior to this command
        Once analysis is finised, 'chart' command is usually following to generate results in a chart html file.

            Args:
                line(str): input line
            Returns:
                n/a
            Raises:
                n/a

        """
        try:
            self.set_parameters(opts)
            self.search.check_vailidity()
            self.search.init_stats()
            self.show_filter_setting()
            self.measure()
        except ValueError as e:
            print e
        except:
            print sys.exc_info()

    @options([
        make_option('-o', '--output', type="string", dest="filepath", help="filepath to export a csv file")
        ])
    def do_csv(self, line, opts=None):
        """Export statistics as a csv file"""
        try:
            data = self.search.get_csv()
            if not opts.filepath:
                filedir = "./"
                filename = self.search.get_filename() + "." + "csv"
            else:
                filedir, filename = split(opts.filepath)

            self.create_csvfile(data, filedir, filename)
        except:
            print "no dataset is available to export."
            print "please perform 'analyze' first to export data"
            print

    @options([
        make_option('-o', '--directory', type="string", dest="DIR", help="change to directory DIR"),
        make_option('-t', '--type', type="string", dest="ctype", default="column", help="chart e.g. bar, line, column, pie, and motion"),
        make_option('-a', '--api', type="string", dest="api", default="highcharts", help="chart api e.g. highchart, google, jquery sparkline")
        ])
    def do_chart(self, line, opts=None):
        ''' Generate html typed chart file based on the statistics from analyze command '''
        self.chart.set_chart_api(opts.api)
        self.chart.set_type(opts.ctype)
        self.chart.set_output_path(opts.DIR)
        self.chart.set_filename(self.search.get_filename() + "." + self.chart.output_type)

        self.chart.set_subtitle("source: " + str(self.search.get_platform_names()) + " on " + str(self.search.get_node_names()))
        self.chart.set_yaxis(self.search.timetype or "")
        self.chart.display()

    @options([
        make_option('-u', '--user', type="string", help="Show only image numbers owned by the userid specified."),
        make_option('-d', '--detail', action="store_true", default=False, help="Show details about images"),
        make_option('-s', '--summary', action="store_true", default=False, help="Show summary values about images")
        ])
    def count_images(self, arg, opts=None):
        """Count bucket images per user (development level)

            It is virtual machine image counts grouped by users or accounts based on euca2ools. 
            It shows that which user or account currently owns how many virtual machine images on the system. 
            This metric is based on the euca2ool command .euca-describe-images. that a eucalyptus user can see
            a list of machine images. 
        """
        bucket_dict = {}
        details = {}
        detail = {}
        max_user = ["", 0]
        bin_path = subprocess.check_output(["which", "euca-describe-images"])
        eucabin = bin_path.split("\n")
        output = subprocess.check_output(["python2.7", eucabin[0]])
        # Split the output by end-of-line chars.
        lines = output.split("\n")
        chart_labels = []

        # Loop through lines. The image path is the third item.
        # Split by "/" to get bucket and key.
        for line in lines:
            if line:
                try:
                    values = line.split()
                    bucket, key = values[2].split("/")
                    # replace bucket with accountId - hrlee
                    # No reason to gather bucket name. Instead, accountid would be meaningful.
                    bucket = values[3] + "(" + values[3] + ")"
                    count = bucket_dict.get(bucket, 0)
                    detail[count] = line 
                    details[bucket] = detail
                    bucket_dict[bucket] = count + 1
                    if bucket_dict[bucket] > max_user[1]:
                        max_user[0] = bucket
                        max_user[1] = bucket_dict[bucket]
                except:
                    continue

        for key, value in bucket_dict.items():
            if opts.user:
                if opts.user != key:
                    continue
            print("\t".join([key, str(value)]))
            chart_labels.append( key + ":" + str(value))

        # show detail information of image owned by a specific user from -u, --user option
        if opts.user and opts.detail:
            for key, value in details[opts.user].items():
                print (value)

        # Show summary of images. i.e. number of total images, number of users, average numbers of images, and maximum numbers of images.
        if opts.summary:
            total_image_count = str(len(lines) - 1) # Except (-1) last \n line count
            total_user_count = str(len(bucket_dict))
            print ""
            print "= Summary ="
            print "Total image counts:\t" + total_image_count
            print "Total user counts:\t" + total_user_count
            print "Average image counts per user:\t" + str(float(total_image_count) / float(total_user_count))
            print "Maximum image counts and userid:\t" + max_user[0] + " has " +  str(max_user[1])
            print "=========="

    def do_refresh(self, line, opts=None):
        """Refresh component (same as 'load')

        Usage example:
        fg-metric] refresh db"""
        self.do_load(line, opts)

    def do_load(self, line, opts=None):
        """Load component

        Usage example:
        fg-metric] load db"""
        self.call_attr(line, "load_")

    def do_showconf(self, line, opts=None):
        """Display current settings

        Usage example:
        fg-metric] showconf dbinfo
        fg-metric] showconf filter_setting"""
        self.call_attr(line, "show_")

    def do_show (self, line, opts=None):
        '''show search options set by a user'''
        self.call_attr(line, "show_", "self.search")

    def do_get(self, line, opts=None):
        """Show current settings

        Usage example:
        fg-metric] get filter"""
        self.call_attr(line, "get_", "self.search")

    def do_setconf(self, line, opts=None):
        """Set a configuration"""
        self.call_attr(line, "set_")

    def do_set(self, line, opts=None):
        """Set a function with parameter(s)"""
        self.call_attr(line, "set_", "self.search")

    def do_count(self, line, opts=None):
        """Set a function with parameter(s)"""
        self.call_attr(line, "count_")

    def call_attr(self, line, prefix="_", obj_name="self"):

        try:
            args = line.split()
            cmd = args[0]

            if len(args) == 1:
                params = ""
            elif len(args) == 2:
                params = args[1]
            else:
                params = args[1:]
        except:
            cmd = None
            params = ""

        function = prefix + str(cmd)

        try:
            func = getattr(eval(obj_name), function)
            if callable(func):
                func(params)
                print function + " is called .(" + "".join(params) + ")"
        except:
            print sys.exc_info()
            pass

    def set_parameters(self, opts):
        """Set search options from opt parse variables

        What variables are set:
            a. dates
            b. metric
            c. period

        Setting prioirity
        1. start_date, end_date
        2. year, month
        3. set date $from $to (set by prior to analyze command)

        For example, 
        if opts.start_date and opts.end_date are given, opts.year and opts.month will be ignored.

            Args:
                opts.start_date
                opts.end_date
                opts.year
                opts.month
                opts.period
                opts.metric
        
        """

        if opts.year or opts.month:
            now = datetime.now()
            from_date = datetime(opts.year or now.year, opts.month or 1, 1)
            to_date = datetime(opts.year or now.year, opts.month or 12, monthrange(opts.year or now.year, opts.month or 12)[1])
            self.search.set_date([from_date, to_date])
        if opts.start_date and opts.end_date:
            self.search.set_date([opts.start_date, opts.end_date])
        if opts.period:
            self.search.set_period(opts.period)
        if opts.metric:
            self.search.set_metric(opts.metric)

    def help_analyze(self):
        print "Run analysis for cloud usage data"

    def do_clear(self, line):
        """Clear settings for analysis. (e.g. nodename, platform, date will be cleared)"""
        self.init_objects()

    def preloop(self):
        self.initialize()
        self.load_db()

    def postloop(self):
        print "Bye ..."

class FGMetricsParameters:
    """
    
    FGMetricCli
    -----------
    Command Line Interface for fg-metric.
   
    Usage: fg-metric-cli

    Description
    ===========
    As a cli version of fg-metric, this module provides usage data with search options.

    - Excutable name is fg-metric-cli (defined by setup.py).
    - FG Cloud Mesh would be one of the examples using fg-metric-cli.
    
    Basic data structure
    ====================

    { 
        "start_date"    :   start date of search    (datetime),
        "end_date"      :   end date of search      (datetime),
        "ownerid"       :   portal user id          (str),
        "metric"        :   selected metric name    (str),
        "period"        :   monthly, weekly, daily  (str),
        "clouds"        :   set of clouds           (list)
                            [ 
                                { "service"     :   cloud service name  (str),
                                 "hostname"     :   hostname (str),
                                 "stats"        :   value (int) }
                                 ...
                                 ]
    }

    Example 1. Get user statistics

    $ fg-metric-cli -u hrlee

    """

    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    development_status = (2, "Pre-alpha")

    def __init__(self):
        self.default_search_days = 180 # Search usage data for this number
        self.default_search_end = datetime.now() # Search starts from this date back to days within default_search_days
        self.api = FGMetricsAPI()
        self.set_default_options()

    def set_default_options(self):
        self.end_date = self.default_search_end
        self.start_date = self.end_date + timedelta(-self.default_search_days)
        self.metric = 'count runtime cores mem disks'

    def set_argparse(self):
        parser = argparse.ArgumentParser(description='Specify search options for usage statistics')
        parser.add_argument('-s', '--s_date', help="start date of search", default=self.start_date)
        parser.add_argument('-e', '--e_date', help="end date of search", default=self.end_date)
        parser.add_argument('-m', '--metric', help="metric name to search", default=self.metric)
        parser.add_argument('-lm', '--listmetrics', help="list of metric possible to search")
        parser.add_argument('-u', '--user', help='owerid (i.e. fg portal id) to search')
        parser.add_argument('-c', '--cloud', help='cloud name to search')
        parser.add_argument('-lc', '--listclouds', help='list of cloud services possible to search')
        parser.add_argument('-H', '--host', help='host name to search')
        parser.add_argument('-lh', '--listhost', help='list of hostnames possible to search')
        parser.add_argument('-p', '--period', help='search period')
        parser.add_argument('-lp', '--listperiod', help='list of search period')
        
        args = parser.parse_args()
        self.args = args

        self._set_vars()

    def _set_vars(self):
        self._set_api_vars()
        self._set_dict_vars()

    def _set_api_vars(self):
        args = self.args
        self.api.set_date(args.s_date, args.e_date)
        self.api.set_metric(args.metric)
        self.api.set_user(args.user)
        self.api.set_cloud(args.cloud)
        self.api.set_hostname(args.host)
        self.api.set_period(args.period)

    def _set_dict_vars(self):
        self.result = {
            "start_date"    :   self.start_date,
            "end_date"      :   self.end_date,
            "ownerid"       :   self.args.user,
            "metric"        :   self.args.metric.split(),
            "period"        :   self.args.period or "All",
            "clouds"        :   self.args.cloud or "All",
            "hostname"      :   self.args.host or "All"
        }

    def get_stats(self):
        self.stats = self.api.get_stats()

    def return_dict(self):
        self.result['stats'] = self.stats
        return json.dumps(self.result, default=json_util.default)

def main():

    app = FGMetrics()
    param = FGMetricsParameters()
    #param.set_argparse()

    parser = optparse.OptionParser()
    parser.add_option('--conf', help='Run unit test suite')
    (callopts, callargs) = parser.parse_args()
    if callopts.conf:
        app.set_configfile(callopts.conf)
        sys.argv = [sys.argv[0]]

    app.cmdloop()

if __name__ == "__main__":
    main()
