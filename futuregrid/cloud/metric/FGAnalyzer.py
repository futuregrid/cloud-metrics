"""
.. module:: FGAnalyzer
   :platform: Unix
   :synopsis: An analyzer of system utilization for the cloud based on the database collected by log files.
              It calculates metrics data and generates graph images like PNG files and html files with javascript.

.. moduleauthor:: Gregor von laszewski, Hyungro Lee <lee212@indiana.edu>


"""

from pygooglechart import PieChart3D, StackedHorizontalBarChart, SimpleLineChart, Axis
import math
import os
import pprint
import optparse
from cmd2 import Cmd, make_option, options, Cmd2TestCase
from datetime import *
import unittest, sys
import calendar
import re

from futuregrid.cloud.metric.FGParser import Instances
from futuregrid.cloud.metric.FGGoogleMotionChart import FGGoogleMotionChart
from futuregrid.cloud.metric.FGPygooglechart import FGPyGoogleChart
from futuregrid.cloud.metric.FGUtility import FGUtility
from futuregrid.cloud.metric.FGHighcharts import FGHighcharts
from futuregrid.cloud.metric.FGNovaMetric import FGNovaMetric
from futuregrid.cloud.metric.FGCharts import FGCharts
from futuregrid.cloud.metric.FGStats import FGStats

class CmdLineAnalyzeEucaData(Cmd):
    '''This class analyzes utilization data to make a report
    
    It uses the extended python cmd package to support command-line iterpreter (CLI) programs.

    .. note::
        
        Examples of this class are in the examples/ directory from the root repository of /futuregrid-cloud-metrics/
    
    '''
    
    instances = {}
    users = {}
    pp = pprint.PrettyPrinter(indent=0)
    charttype = "pie"
    from_date = ""
    to_date = ""
    day_count = 0
    echo = True
    timing = True

    userid = None
    user_stats = None
    sys_stats = None
    sys_stat_new = None # sys_stats will be converted to this

    platform = None
    nodename = None
    metric = None

    nova = None

    chart = None
    output_format = None

    def calculate_stats (self, from_date="all", to_date="all"):
        """Calculate user-based statstics about VM instances per user: count, min time, max time, avg time, total time
        
        Args:
            from_date (str): date to start calculation. Types are 'all' or '%Y-%m-%dT%H:%M:%S'
            to_date (str): end date to finish calculation.
        Returns:
            n/a
        Raises:
            n/a

        """

        process_all = False
        if (type(from_date).__name__ == "str"):
            process_all = (from_date == "all")
            if not process_all:
                date_from = datetime.strptime(from_date, '%Y-%m-%dT%H:%M:%S')
                date_to   = datetime.strptime(to_date, '%Y-%m-%dT%H:%M:%S')

        if (type(from_date).__name__ == "None"):
            process_all = True

        if (type(from_date).__name__ == "datetime"):
            date_from = from_date
            date_to = to_date
            process_all = False

        for i in range(0, int(self.instances.count())):
            values = self.instances.getdata(i)
            process_entry = process_all
            
            if not process_all:
                #process_entry = (values['ts'] >= date_from) and (values['ts'] < date_to)
                process_entry = (values['t_end'] >= date_from) and (values['t_start'] <= date_to)

            if process_entry:

                # If a nodename is set, stats is only for the compute cluster node specified
                #if self.nodename and self.nodename != values['euca_hostname']:
                if self.nodename and self.nodename != values['hostname']:
                    continue

                if self.platform and self.platform != values["cloudplatform.platform"]:
                    continue

                name = values["ownerId"]
                t_delta = float(values["duration"])
                try:
                    self.users[name]["count"] += 1
                    # number of instances
                except:
                #          count,sum,min,max,avg
                    self.users[name] = {'count' : 1,
                                        'runtime' : 0.0,
                                        'min' : t_delta,
                                        'max' : t_delta,
                                        'avg' : 0.0
                                        }

                self.users[name]['runtime'] += t_delta  # sum of time 
                self.users[name]['min'] = min (t_delta, self.users[name]['min'])
                self.users[name]['max'] = max (t_delta, self.users[name]['max'])

                for name in self.users:
                    self.users[name]['avg'] = float(self.users[name]['runtime']) / float(self.users[name]['count'])

    def set_date(self, from_date, to_date):
        """Set search/analyze period
        
        Args:
            from_date (str): date to start calculation. '%Y-%m-%dT%H:%M:%S' is only allowed.
            to_date (str): end date to finish calculation.
        Returns:
            n/a
        Raises:
            n/a

        """

        try:
            self.from_date = datetime.strptime(from_date, '%Y-%m-%dT%H:%M:%S')
            self.to_date = datetime.strptime(to_date, '%Y-%m-%dT%H:%M:%S')
            self.day_count = (self.to_date - self.from_date).days + 1
        except:
            print "from and to date not specified." 
            pass

    def get_user_stats(self, username, metric, period="daily"):
        """ Call a private function """
        self.metric = metric
        return self._get_stats(metric, period, username)

    def get_sys_stats(self, metric, period="daily"):
        """ Call a private function """
        self.metric = metric
        return self._get_stats(metric, period)

    def _get_stats(self, metric, period="daily", username=""):
        """Return the list of calculated data
        
        Args:
            metric (str): a metric name to be analyzed (i.e. runtime, count, ccvm_cores, ccvm_mem, ccvm_disk)
            period (str): a search term (i.e. weekly, daily)
            username (str): a ownerid to be analyzed
        Returns:
            a list of numerical values of a metric for the search period range from the start date to the end date.
            Each element of the list indicates a statistical value for a day or a week depends on the period specified.
            For example, in the list of [0, 2, 5, ... 1], the 1st value (0) indicates a first day or a first week of the
            search period.
        Raises:
            n/a

        """

        merged_res = []
        # instance based data
        for i in range(0, int(self.instances.count())):
            instance = self.instances.getdata(i)
            if username and username != instance["ownerId"] :
                continue
            #if self.nodename and self.nodename != instance["euca_hostname"] :
            if self.nodename and self.nodename != instance['hostname']:
                continue
            if self.platform and self.platform != instance["cloudplatform.platform"]:
                continue

            self._count_node(instance)
            merged_res = self._daily_stats(instance, metric, merged_res, "sum") # or "avg"

        if period == "weekly":
            merged_res = self.convert_stats_from_daily_to_weekly(merged_res)
        return merged_res

    def _count_node(self, instance):
        """Count nodes

        Args:
            instance(dict): instance 

        Returns:
            n/a 
        Raises:
            n/a

        """
        
        if self.metric != "count_node":
            return

        #sys_stat = self.stats.get('count_node')
        sys_stat = self.sys_stat_new['total']['count_node']
        if instance["t_start"] < self.from_date or instance["t_start"] > self.to_date:
            return
        try:
            m = re.search(r'http://(.*):8775/axis2/services/EucalyptusNC', str(instance["serviceTag"]), re.M|re.I)
            nodename = str(m.group(1))

            if nodename in sys_stat:
                sys_stat[nodename] = int(sys_stat[nodename]) + 1
            else:
                sys_stat[nodename] = 1
            self.sys_stat_new['total']['count_node'] = sys_stat
        except:
            print "total_stats is not calculated.", sys.exc_info()[0]
            return

    def convert_stats_from_daily_to_weekly(self, stats):
        """Convert a daily list of calculated data to a weekly list of data in case the period specified with 'weekly'

        Args:
            stats (list): a daily list of calculated data
        Returns:
            a shrinked list of data
        Raises:
            n/a
        """

        j = 0
        k = 0
        weekly_stats = [ 0 for n in range (0, (len(stats) / 7))]
        for i in range(0, len(stats)):
            j = j + 1
            weekly_stats[k] = weekly_stats[k] + stats[i]
            if j == 7:
                j = 0
                k = k + 1
        return weekly_stats

    def _daily_stats(self, instance, metric, current_stats, type="sum"):
        try:
            new_stats = self._daily_stat(instance, metric)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise
        res = self._merge_daily_stat(new_stats, current_stats, type)
        return res
    
    def _daily_stat(self, instance, metric):
        """Return a list of calculated data for the search period on a daily basis

        # This is going to be counting hours for daily
        # This logic is kind of messy but it should be changed/updated soon, Hopefully.

           Make a list filled with metric values in a daily basis.
           The size of the list is the date range of analyze. 
           e.g. [0 (1st), 0 (2nd), ... , 0 (31th)] list will be 
           returned when 'analyze -M 01' which is for January 2012
           is requested. 

        Args:
            instance(dict): Dictionary from the getdata() function of the class Instances. (instances.getdata())
            metric(str): runtime, count, ccvm_cores, ccvm_mem, and ccvm_disk are available

        Returns:
            a list of calculated data
            
        Raises:
            n/a
    
        """

        month = [ 0 for n in range(self.day_count) ]
        if instance["t_end"] < self.from_date or instance["t_start"] > self.to_date :
            return month
        if instance["t_start"] > self.from_date:
            offset = (instance["t_start"] - self.from_date).days
            ins_start = instance["t_start"]
        else:
            offset = 0
            ins_start = self.from_date

        day_count_ins = (instance["t_end"] - ins_start).days + 1
        i = 0

        for single_date in (ins_start + timedelta(n) for n in range(day_count_ins)):
            if single_date > self.to_date:
                break

            if metric == "runtime":
                first_second_of_a_day = datetime.combine(single_date.date(), datetime.strptime("00:00:00", "%H:%M:%S").time())
                last_second_of_a_day = first_second_of_a_day + timedelta(days=1)
                if i == 0: # First day of instance (same with instance["t_start"] and single_date)
                    td = last_second_of_a_day - single_date
                    hour = int(math.ceil(float(td.seconds) / 60 / 60))
                    month[offset + i] = hour
                elif i + 1 == day_count_ins: # Last day of instance (same day with instance["t_end"] and single_date)
                    td = instance["t_end"] - first_second_of_a_day
                    hour = int(math.ceil(float(td.seconds) / 60 / 60))
                    month[offset + i] = hour
                else: # days between first and last days of instance
                    month[offset + i] = 24 # hours
            elif metric == "count":
                month[offset + i] = 1
            elif metric == "ccvm_cores":
                month[offset + i] = int(instance["ccvm"]["cores"])
            elif metric == "ccvm_mem":
                month[offset + i] = int(instance["ccvm"]["mem"])
            elif metric == "ccvm_disk":
                month[offset + i] = int(instance["ccvm"]["disk"])
            i += 1

        if metric == "runtime":
            if day_count_ins == 1:
                td = instance["t_end"] - ins_start
                hour = int(math.ceil(float(td.seconds) / 60 / 60))
                month[offset] = hour
        elif metric == "count" and day_count_ins == 1:
            month[offset] = 1
        elif metric == "ccvm_cores" and day_count_ins == 1:
            month[offset] = int(instance["ccvm"]["cores"])
        elif metric == "ccvm_mem" and day_count_ins == 1:
            month[offset] = int(instance["ccvm"]["mem"])
        elif metric == "ccvm_disk" and day_count_ins == 1:
            month[offset] = int(instance["ccvm"]["disk"])

        return month

    def _merge_daily_stat(self, new, current, type="sum"):
        """Merge daily_historam lists 
            
            E.g. [1,2,3] + [2,3,4]
            expect => [ 1+2, 2+3, 3+4] = [ 3, 5, 7]

            Args:
                new(list): The new list for the stats
                current(list): The exist list of the stats
                type(str): The operation name of the merging which is one of sum (summation) or avg (average).
            Returns:
                a merged list from the new and current arguments
            Raises:
            n/a
        """

        if len(current) == 0:
            current = [0 for n in range(self.day_count) ]

        if type == "avg":
            divide = 2.0
        else:
            divide = 1.0

        array = [new, current]
        return [(sum(a)/divide) for a in zip(*array)]

    def line_chart(self, chart_data, output):
        """Create python Google Chart (line type) in a PNG file format"""
        self._create_chart(chart_data, output, chart_type = "line")
       
    def bar_chart(self, chart_data, output):
        """Create python Google Chart (bar type) in a PNG file format"""
        self._create_chart(chart_data, output, chart_type = "bar")

    def _create_chart(self, chart_data, output, chart_type = "line"):
        """Create python Google Chart in a PNG file format"""

        try:
            maxY = int(round(max(chart_data) / 10) * 10)
            chart = FGPyGoogleChart(chart_type, maxY)
            chart.set_data(chart_data)
            topY = maxY + 1
            chart.set_yaxis([ str(x) for x in range(0, topY, int(math.ceil(topY / 4)))])
    #        chart.set_xaxis([ str(x)+"d" for x in range(0, self.day_count + 1, ((self.day_count + 1) / 9))])
            chart.set_xaxis([ str(x) for x in range(1, len(chart_data) + 1)])
            chart.set_output_path(output)
            chart.set_filename(chart_type + "chart.png")
            chart.display()
            print chart.filepath + "/" + chart.filename + " created."
        except:
            print "chart is not created.", sys.exc_info()[0]
            pass

    def create_highcharts(self, chart_data, output, chart_type = "column"):
        """Create highcharts in a javascript html file format"""
        try:
            highchart = FGHighcharts(chart_type)
            highchart.set_data(chart_data)
            if self.nodename:
                data_name = self.nodename
            else:
                data_name = "all"
            highchart.set_data_name(data_name)
            highchart.set_subtitle("source : " + data_name)
            highchart.set_output_path(output)
            if self.metric == "count_node":
                title = "Total VMs count per a node cluster"
                highchart.set_xaxis(highchart.get_data(0))
                highchart.set_yaxis(self.metric)
            elif not self.metric: # This from user stats. display_stats
                highchart.set_xaxis(highchart.get_data(0))
                highchart.set_yaxis("")
                title = ""
            else:
                highchart.set_yaxis(self.metric)
                highchart.set_xaxis([ d.strftime("%Y-%m-%d") + " ~ " + (d + timedelta(6)).strftime("%Y-%m-%d") for d in (self.from_date + timedelta(n) for n in range(0, self.day_count, 7))])
                if self.metric == "runtime":
                    tmp = " (hour) "
                else:
                    tmp = ""
                title = "Total " + self.metric + tmp + " of VM instances"

            if chart_type == "master-detail":
                highchart.set_from_date(self.from_date)
                highchart.set_to_date(self.to_date)
                highchart.set_height(400)
                highchart.set_detail_date()
            highchart.set_title(title)
            highchart.set_filename(chart_type + "highcharts.html")
            highchart.set_tooltip("")
            highchart.display()
            print highchart.filepath + "/" + highchart.filename + " created."
        except:
            print "highcharts is not created.", sys.exc_info()[0]
            pass

    def create_csvfile(self, list_of_data, filepath):
        import csv

        try:
            filename = "text.csv"
            FGUtility.ensure_dir(filepath)
            writer = csv.writer(open(filepath + "/" + filename, 'wb'), delimiter=",",
                    quotechar="|", quoting=csv.QUOTE_MINIMAL)
            for row in list_of_data:
                writer.writerow(row)

            msg = filename + " is created"
        except:
            msg = filename + " not is created"
            pass

        print msg

    def display_stats(self, metric="count", type="pie", filepath="chart.png"):
        """Create Python Google Chart
           This should be merged to _create_chart()
        
            It displays the number of VMs per user

            Args:
                metric(str): metric name to display (e.g. count, )
                type(str): chart type (e.g. pie, bar)
                filepath(str): A location the output will be saved. It includes a directory path and a filename.
                               (other options are available e.g. display; open a browser, url; )
            Returns:
                n/a
            Raises:
                n/a
        """

        values = []
        label_values = []
        max_v = 0

        list_for_highchart = []
        list_for_csv = []
        list_for_csv.append(["owner id", "user name", "value for metric"])

        if self.platform and (self.platform == "nova" or self.platform == "openstack"):
            user_list = self.nova.users
        else:
            user_list = self.users

        for name in user_list:
            number = user_list[name][metric]
            # Temporary lines for converting sec to min 
            if metric != "count":
                number = int (math.ceil(number / 60 / 60))
            values.append(number)
            label = self.convert_ownerId_str(name) + ":" + str(number)
            label_values.append(label)
            list_for_highchart.append([label, number])
            list_for_csv.append([name, self.convert_ownerId_str(name), number])
            max_v = max(max_v, number)

        #self.generate_pygooglechart(type, label_values, max_v, values, filepath)
        if type == "highchart-column":
            self.create_highcharts(list_for_highchart, filepath + "/" + metric + "/", "bar")
        elif type == "csv":
            self.create_csvfile(list_for_csv, filepath + "/" + metric + "/")

    def generate_pygooglechart(self, chart_type, labels, max_value, values, filepath, width=500, height=200): 
        """Create Python Google Chart but this should be merged to _create_chart()"""

        if chart_type == "pie": 
            chart = PieChart3D(width, height)
            chart.set_pie_labels(labels)
        if chart_type == "bar":
            chart = StackedHorizontalBarChart(width, height, x_range=(0, max_value))
            chart.set_axis_labels('y', reversed(labels))
            # setting the x axis labels
            interval = int(max_value) / 10
            if interval < 1:
                interval = 1
            left_axis = range(0, int(max_value + 1), interval)
            left_axis[0] = ''
            chart.set_axis_labels(Axis.BOTTOM, left_axis)
            chart.set_bar_width(10)
            chart.set_colours(['00ff00', 'ff0000'])

        chart.add_data(values)

        if filepath == "display":
            os.system ("open " + filepath)
        elif filepath == "url":
            url = chart.get_url()
            print url
        else:
            FGUtility.ensure_dir(filepath)
            chart.download(filepath)

    def make_google_motion_chart(self, directory):
        """Create "FGGoogleMotionChart.html"

        * Should be obsolete due to the new way to display charts
        """

        filename = "FGGoogleMotionChart.html"
        filepath = directory + "/" + filename
        FGUtility.ensure_dir(filepath)
        test = FGGoogleMotionChart()
        self.set_fullname()
        output = test.display(self.users, str(self.from_date))
        f = open(filepath, "w")
        f.write(output)
        f.close()
        print filepath + " created"

    def convert_ownerId_str(self, id):
        """Convert a owner id to a user name
        
        * This should be working with retrieving ldap commands
        * Currently, this function is a test version
        """

        if self.platform and (self.platform == "nova" or self.platform == "openstack"):
            id = self.convert_nova_userid_to_username(id)

        for element in self.instances.userinfo_data:
            if element['ownerid'] == id:
                return element['first_name'] + " " + element['last_name']

        # Second try if it does not exist
        for element in self.instances.userinfo_data:
            if element['username'] == id:
                return element['first_name'] + " " + element['last_name']

        if id == "EJMBZFNPMDQ73AUDPOUS3":
            return "eucalyptus-admin"
        else: 
            return id

    def convert_accountId_str(self, id):
        """Convert an account id to a user name

        * This should be working with retrieving ldap commands
        * Currently, this function is a test version

        # Temporarily add here 
        # But it will be replaced by 'euare-accountlist|grep $accountid'
        # e.g. euare-accountlist|grep fg82
        # fg82    281408815495
        """

        ## TEST ONLY ~!!!!! ##
        if id == "458299102773" :
            return "eucalyptus"
        elif id == "281408815495" :
            return "fg82"
        elif id == "000000000001" :
            return "system"
        elif id == "081364875274" :
            return "fg168"
        elif id == "150119767462" :
            return "fg3"
        elif id == "355794507465" :
            return "fg201"
        else :
            return id

    def convert_nova_userid_to_username(self, id):
        """Convert a owner id to a user name
        
        * This should be working with retrieving ldap commands
        * Currently, this function is a test version
        """

        for element in self.nova.userinfo:
            if element['id'] == id:
                return element['name']

    def set_fullname(self):
        for uname in self.users:
            fullname = self.convert_ownerId_str(uname)
            self.users[uname]['fullname'] = fullname

    def realtime(self, cmd, param):

        users = {}
        metric = param[0]
        # Temporary for test
        #self.instances.clear()
        #self.instances.eucadb.change_table("instance_for_realtime")
        #self.instances.read_from_db()
        for i in range(0, int(self.instances.count())):
            values = self.instances.getdata(i)
            # TEMPORARY
            if values["date"] < datetime(2012, 7, 27):
                continue
            if values["state"] != "Extant":
                continue
            #if self.nodename and self.nodename != values['euca_hostname']:
            if self.nodename and self.nodename != values['hostname']:
                continue
            if self.platform and self.platform != values["cloudplatform.platform"]:
                continue

            ownerId = values["ownerId"]
            if ownerId in users:
                metric_val = users[ownerId][metric] + 1
            else:
                metric_val = 1
            users[ownerId] = { metric: metric_val }
        for user in users:
            output = self.convert_ownerId_str(user) + ", " + str(users[user][metric])
            print FGUtility.convertOutput(output, "realtime")

    def preloop(self):
        self.do_loaddb("")
        self.do_loadnovadb("")

        # Initialize values
        self.sys_stat_new = {'total' : ""}
        self.sys_stat_new['total'] = { 'count_node' : {}}

        self.stats = FGStats()
        self.chart = FGCharts()

    def postloop(self):
        print "BYE ..."

    # def do_server_start (self,arg):
    #     os.system('lighttpd -D -f lighttpd.conf &')


    # def do_server_stop (self,arg):
    #     os.system('killall lighttpd')

    def do_changecharttype (self, arg):
        """Change the default caht type. You can choese bar, pie, motion"""
        if (arg != "pie") and (arg != "bar") and (arg != "motion"):
            print "Error: charttype " + arg + " not supported."
        else:
            print "Setting chart type to " + arg
            self.charttype = arg

    @options([
        make_option('-t', '--type', type="string", help="users"),
        make_option('-s', '--seperator', type="string", help="seperator between attribute and value"),
        make_option('-c', '--caption', type="string", help="title of the table"),
        ])
    def do_table(self, arg, opts):
        """Print a table from the instance data"""
        print opts.caption
        if opts.seperator == "" or opts.seperator == None:
            seperator = "="
        else:
            seperator = opts.seperator
        if opts.caption != "" and opts.caption != None:
            print "# " + opts.caption
            print "# -----------------------------------------"
        if opts.type == "users":
            print arg
            for name in self.users:
                print "%s %s %s" % (name, seperator, self.users[name]['count'])
        else:
            print "Error: Printing <" + opts.type + "> is not supported"

    def do_loaddb(self, arg):
        """Read the statistical data from MySQL database"""
        
        print "\r... loading data from database"
        self.users = {}
        self.instances = Instances()
        # gets also data from the database
        self.instances.read_from_db()

        # Gets also userinfo data from the database
        self.instances.read_userinfo_from_db()

        print "\r... data loaded"

    def do_loadnovadb(self, arg):

        print "\r... loading data from nova database"
        self.nova = FGNovaMetric()
        # gets also data from the database
        self.nova.read_from_db()

        print "\r... data loaded"

    def do_pause(slef, arg):
        """Wait for a return to be typed in with the keyboard"""
        os.system("pause")

    def do_dump(self, arg):
        """Print the data from all instances."""
        # if we specify key, prints it from an instance with a given instance id
        self.instances.dump()

    def do_printlist(self, arg):
        """List all instance ids id's"""
        # takes as additional parameters fields to be printed

        print "\n... list\n"
        self.instances.print_list(arg)

    def do_clear(self, arg):
        """Clear all instance data and user data from the memory"""
        if arg == "users":
            self.users = {}
        elif arg == "instances":
            self.instances = {}
        elif arg == "all":
            self.users = {}
            self.from_date = ""
            self.to_date = ""
            self.day_count = 0
            self.userid = None
            self.user_stats = None
            self.sys_stats = None
            self.sys_stat_new = {'total' : ""}
            self.sys_stat_new['total'] = { 'count_node' : {}}
            self.metric = None
            self.nodename = None
            self.platform = None

            self.nova.clear_stats()

    @options([
        make_option('-f', '--start', default="all", type="string", help="start time of the interval (type. YYYY-MM-DDThh:mm:ss)"),
        make_option('-t', '--end',  default="all",  type="string", help="end time of the interval (type. YYYY-MM-DDThh:mm:ss)"),
        make_option('-M', '--month', type="string", help="month to analyze (type. MM)"),
        make_option('-Y', '--year', type="string", help="year to analyze (type. YYYY)"),
        make_option('-S', '--stats', dest="metric", type="string", help="item name to measure (e.g. runtime, vms)"),
        make_option('-P', '--period', dest="period", type="string", help="search period (weekly, daily)")
        ])
    def do_analyze (self, arg, opts=None):
        """Analyze utilization data

        This is main function to get statistical data

        """
        # Default set year and month by current date
        now = datetime.now()
        analyze_year = str(now.year)  
        analyze_s_month = "01"
        analyze_e_month = "12"

        if opts.year == analyze_year:
            analyze_e_month = str(now.month)
        if opts.year:
            analyze_year = opts.year
        if opts.month:
            analyze_s_month = opts.month
            analyze_e_month = opts.month

        if opts.year or opts.month:
            from_date = "%s-%s-01T00:00:00" % (analyze_year, analyze_s_month)
            to_date = "%s-%s-%sT23:59:59" % (analyze_year, analyze_e_month,
                    str(calendar.monthrange(int(analyze_year), int(analyze_e_month))[1]))
        else:
            from_date = opts.start
            to_date = opts.end

        print "analyze [" + from_date + ", " + to_date + "]" 
        self.set_date(from_date, to_date)
        self.stats.set_search_date(from_date, to_date)
        self.stats.set_metric(opts.metric)
        self.stats.set_period(opts.period)

        self.instances.refresh()
        print "now calculating"
        self.calculate_stats (from_date, to_date)

        # new way to calculate metrics
        # get_sys_stats return a list of daily values not specified by a user name
        # It can display daily/weekly/monthly graphs for system utilization
        self.sys_stats = self.get_sys_stats(opts.metric, opts.period)
        #print self.sys_stats

        self.nova.calculate_stats(self.from_date, self.to_date)

    def do_getdaterange(self, arg): 
        """Get Date range of the instances table in mysql db"""

        res = self.instances.getDateRange()
        print FGUtility.convertOutput(res[0], "first_date")
        print FGUtility.convertOutput(res[1], "last_date")
        #print self.instances.eucadb.read("", " order by date limit 1")
        #print self.instances.eucadb.read("", " order by date DESC limit 1")

    def do_printusers(self, arg):
        print self.pp.pprint(self.users)

    def do_timing (self, arg):
        self.timing = True

    def do_echo (self, arg):
        self.echo = True

    def do_open(self,arg):
        os.system ("open " + arg)

    @options([
        make_option('-t', '--type', default = charttype, type="string", help="pie, bar, motion"),
        make_option('-f', '--filepath', default = "chart.png", type="string", help="the filepath in which we store a chart")
        ])
    def do_creategraph(self, arg, opts=None):
        """Create PNG graphs (obsolete)"""
        graph_type =  opts.type
        filepath = opts.filepath
        print graph_type + " typed " + filepath + " file created"
        self.display_stats("all", "count", graph_type, filepath)

    @options([
        make_option('-d', '--directory', type="string", help="directory name which the chart html will be stored.")
        ])
    def do_createhtml(self, arg):
        """Create google motion chart (obsolete)"""
        self.make_google_motion_chart(opts.directory)

    @options([
        make_option('-d', '--directory', type="string", help="directory name which contains report graphs."),
#        make_option('-t', '--title', type="string", help="A report title in the index.html"),
        make_option('-f', '--format', type="string", help="A report format. There are 'pie', 'bar' and 'highchart-column' chart types or 'csv' format")
        ])
    def do_createreport(self, arg, opts=None):
        """Create PNG graphs which display statistics"""

        default_format = "highchart-column"
        self._set_format(opts.format)
        if not self.output_format:
            output_format = default_format
        else:
            output_format = self.output_format
        #self.display_stats("count", "pie", opts.directory + "/pie.count.png")
        #self.display_stats("count", "bar", opts.directory + "/bar.count.png")
        #self.display_stats("sum", "pie", opts.directory + "/pie.sum.png")
        #self.display_stats("sum", "bar", opts.directory + "/bar.sum.png")

        self.make_google_motion_chart(opts.directory)
        self.display_stats("count", output_format, opts.directory)
        self.display_stats("runtime", output_format, opts.directory)

    @options([
        make_option('-f', '--start', type="string", help="start time of the interval (type. YYYY-MM-DDThh:mm:ss)"),
        make_option('-t', '--end',  type="string", help="end time of the interval (type. YYYY-MM-DDThh:mm:ss)"),
        make_option('-M', '--month', default=datetime.now().month, type="string", help="month to analyze (type. MM)"),
        make_option('-Y', '--year', default=datetime.now().year, type="string", help="year to analyze (type. YYYY)"),
        ])
    def do_set_range (self, arg, opts=None):
        """Set search period (obsolete)"""

        if opts.start and opts.end:
            from_date = opts.start
            to_date = opts.end
        else:
            from_date = "%s-%s-01T00:00:00" % (opts.year, opts.month)
            to_date = "%s-%s-%sT23:59:59" % (opts.year, opts.month,
                    str(calendar.monthrange(int(opts.year), int(opts.month))[1]))

        print "Set date range to analyze: [" + from_date + ", " + to_date + "]" 
        self.set_date(from_date, to_date)

    def _search_range(self, param):
        """Set search period
            # E.g. cmd) set search_range 2011-11-01T00:00:00 2012-05-14T23:59:59
        """
        from_date = param[0]
        to_date = param[1]
        print "Set a date range to analyze: [" + from_date + ", " + to_date + "]" 
        self.set_date(from_date, to_date)

    def _set_nodename(self, param):
        """Set node name
            E.g. cmd) set nodename india
        """
        nodename = param[0]
        print "Set a nodename by to analyze: [" + nodename + "]"
        self.nodename = nodename

    def _set_platform(self, param):
        """Select platform (e.g. eucalyptus, openstack)
        """

        platform = param[0]
        print "Set a platform by to analyze: [" + platform + "]"
        self.platform = platform

    def _set_format(self, param):
        """Select output format (e.g. bar, pie, and highchart-column chart types or csv format)"""

        if not param:
            return

        if type(param) == type(str()):
            format = param
        else:
            format = param[0]

        print "A output format is set by :[" + format + "]"

        self.output_format = format

    def _set_chart(self, param):
        """Set chart options (e.g. type, name, etc)
        """

        function = "set_" + str(param[0])
        value = param[1]

        try:
            func = getattr(self.chart, function)
            func(value)

            print "Set a chart option (" + function + ") to : " + value
        except:
            pass

    @options([
        make_option('-u', '--user', type="string", help="user id to analyze"),
        make_option('-m', '--metric', default="runtime", type="string", help="metric name to display (runtime, vms)")
        ])
    def do_analyze_user(self, arg, opts=None):
        """Analyze user statistics"""

        if not opts.user:
            print "user id is required."
            return

        self.user_stats = self.get_user_stats(opts.user, opts.metric)
        self.userid = opts.user

        print self.user_stats

    @options([
        make_option('-o', '--output', type="string", help="Filepath in which we store a chart")
        ])
    def do_user_report(self, arg, opts=None):
        """Generate a user report through Google line chart """

        # set default output by Year-month typed string
        if not opts.output:
            opts.output = str(self.from_date.year) + "-" + str(self.from_date.month)

        # user_stats has a user's data analyzed by 'analyze_user' command.
        # user_report requires prior execution of 'analyze_user' command.
        self.line_chart(self.user_stats, opts.output)

        print
        print "This line chart displays statistics of a specific user's metric."
        print self.userid + " (userid) is selected to display 'instance runtime' of " + str(self.from_date.month) + "/" + str(self.from_date.year) + "."
        print "Y-axis indicates total running hours of instances."
        print "X-axis indicates date of the month."
        print

    @options([
        make_option('-o', '--output', type="string", help="Filepath in which we store a chart"),
        make_option('-A', '--all', action='store_true', default=False, help="report all period data")
        ])
    def do_sys_report(self, arg, opts=None):
        """Generate system reports such as usage of CPU, memories, and disks."""

        # Set output directory
        if not opts.output:
            opts.output = str(self.from_date.year) + "-" + str(self.from_date.month)

        '''
        self.chart.set_output_path(opts.output)

        # Display metric: count_node
        try:
            self.chart.set_xaxis(self.sys_stat_new['total']['count_node'].keys())
            self.chart.set_yaxis(self.sys_stat_new['total']['count_node'].values())
            self.chart.display()
        except:
            pass
        '''

        if 'count_node' in self.sys_stat_new['total'] and len(self.sys_stat_new['total']['count_node']) != 0:
            self.create_highcharts(self.sys_stat_new['total']['count_node'], opts.output, "column")
            return
           
        self.line_chart(self.sys_stats, opts.output)
        self.bar_chart(self.sys_stats, opts.output)
        self.create_highcharts(self.sys_stats, opts.output)

        if opts.all:
            self.create_highcharts(self.sys_stats, opts.output, "master-detail")

    def do_filled_line_example(self, arg, opts=None):
        """Example for python Google line chart"""
        chart = PyGoogleChart("line", 0)
        chart.filledLineExample()

    @options([
        make_option('-u', '--user', type="string", help="Show only image numbers owned by the userid specified."),
        make_option('-d', '--detail', action="store_true", default=False, help="Show details about images"),
        make_option('-s', '--summary', action="store_true", default=False, help="Show summary values about images")
        ])
    def do_count_images(self, arg, opts=None):
        """Count bucket images per user

            It is virtual machine image counts grouped by users or accounts based on euca2ools. 
            It shows that which user or account currently owns how many virtual machine images on the system. 
            This metric is based on the euca2ool command .euca-describe-images. that a eucalyptus user can see
            a list of machine images. 
        """
        import subprocess
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
                values = line.split()
                bucket, key = values[2].split("/")
                # replace bucket with accountId - hrlee
                # No reason to gather bucket name. Instead, accountid would be meaningful.
                bucket = values[3] + "(" + self.convert_accountId_str(values[3]) + ")"
                count = bucket_dict.get(bucket, 0)
                detail[count] = line 
                details[bucket] = detail
                bucket_dict[bucket] = count + 1
                if bucket_dict[bucket] > max_user[1]:
                    max_user[0] = bucket
                    max_user[1] = bucket_dict[bucket]

        for key, value in bucket_dict.items():
            if opts.user:
                if opts.user != key:
                    continue
            print("\t".join([key, str(value)]))
            chart_labels.append( key + ":" + str(value))

        # Generate pygooglchart
        chart_max_v = int(math.ceil(max(bucket_dict.values()) * 1.1))
        chart_type = "bar"
        chart_filepath = "image_counts.png"
        chart_values = bucket_dict.values()
        self.generate_pygooglechart(chart_type, chart_labels, chart_max_v, chart_values, chart_filepath)

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

    @options([
        make_option('-u', '--user', type="string", help="Specify user name")
        ])
    def do_user_stats(self, arg, opts=None):
        """Print user statistics

            It is supposed to provide a user's statistics for a search period
            Not yet implemented.

        Prototype for usage
        #(cmd) user_stats -u username
        #period: 01/01/2011 ~ 01/01/2012
        #instances:
        #    total instances launched: 14
        #    total seconds used: 3600
        #    average ccvms (cores/mems/disks): 2, 512, 5
        #    min/max ccvms: 1/2, 512/6000, 5/15

        """

        print "period:" +  self.from_date + " ~ " + self.to_date

        # instances stats
        print "instances:"

    def do_set (self, arg, opts=None):
        """Set a function with parameter(s)"""

        args = arg.split()
        cmd = args[0]
        param = args[1:]

        if cmd == "search_range":
            self._search_range(param)
        elif cmd == "nodename":
            self._set_nodename(param)
        elif cmd == "platform":
            self._set_platform(param)
        elif cmd == "chart":
            self._set_chart(param)
        elif cmd == "format":
            self._set_format(param)

    def do_show(self, arg, opts=None):
        """ Display realtime usage data"""

        args = arg.split()
        cmd = args[0]
        param = args[1:]

        self.realtime(cmd, param)

#########################################################
# UNDER DEVELOPING
#########################################################
    def do_get(self, arg, opts=None):
        """Perform an action to obtain possession of"""

        try:
            args = arg.split()
            param = args[0]
            #param = args[1:]
        except:
            param = ""
            pass

        self.get_stats(param)

    def get_stats(self, param):
        """Provide statistics"""

        # check required fields
        if (not param) or (param == "metric"):
            print self.metric #is_exist(self.metric)
        print self.nodename
        print self.platform
        print self.from_date
        print self.to_date
        #is_exist(self.groupby)
        #is_exist(self.search_length_of_time)
        #is_exist(self.search_interval)

        #self.select_data_source("instance")

    def a(self):

        data = self.data_source
        result = []
        first_column = self.get_val("groupby")
        second_column = self.get_val("metric")
        third_column = self.get_val("search_interval")
        for i in range(len(data)):
            row = {first_column:first_value, second_column:second_value, third_column:third_value}
            result.append()

#####################################################################
# main
#####################################################################
def main():

    parser = optparse.OptionParser()
    parser.add_option('-t', '--test', dest='unittests', action='store_true', default=False, help='Run unit test suite')
    (callopts, callargs) = parser.parse_args()
    if callopts.unittests:
        sys.argv = [sys.argv[0]]  # the --test argument upsets unittest.main()
        unittest.main()
    else:
        app = CmdLineAnalyzeEucaData()
        app.cmdloop()

if __name__ == "__main__":
    main()
