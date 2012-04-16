#!/usr/bin/env python
'''FGAnalyser Module'''

from pygooglechart import PieChart3D, StackedHorizontalBarChart, SimpleLineChart, Axis
import os
import pprint
import optparse
from cmd2 import Cmd, make_option, options, Cmd2TestCase
from datetime import *

import unittest, sys
import calendar

from futuregrid.cloud.metric.FGParser import Instances
from futuregrid.cloud.metric.FGGoogleMotionChart import GoogleMotionChart
from futuregrid.cloud.metric.FGPygooglechart import PyGoogleChart
from futuregrid.cloud.metric.FGUtility import Utility
from futuregrid.cloud.metric.FGTemplate import HtmlTemplate

class CmdLineAnalyzeEucaData(Cmd):
    '''Cmd Shell Analyzer'''
    #multilineCommands = ['None']
    #Cmd.shortcuts.update({'&': 'speak'})
    #maxrepeats = 3
    #Cmd.settable.append('maxrepeats')
    
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

    def calculate_stats (self, from_date="all", to_date="all"):
        '''calculates some elementary statusticks about the instances per user: count, min time, max time, avg time, total time'''

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
                process_entry = (values['ts'] >= date_from) and (values['ts'] < date_to)

            if process_entry:
                name = values["ownerId"]
                t_delta = float(values["duration"])
                try:
                    self.users[name]["count"] += 1
                    # number of instances
                except:
                #          count,sum,min,max,avg
                    self.users[name] = {'count' : 1,
                                        'sum' : 0.0,
                                        'min' : t_delta,
                                        'max' : t_delta,
                                        'avg' : 0.0
                                        }

                self.users[name]['sum'] += t_delta  # sum of time 
                self.users[name]['min'] = min (t_delta, self.users[name]['min'])
                self.users[name]['max'] = min (t_delta, self.users[name]['max'])

                for name in self.users:
                    self.users[name]['avg'] = float(self.users[name]['sum']) / float(self.users[name]['count'])

    def set_date(self, from_date, to_date):
        try:
            self.from_date = datetime.strptime(from_date, '%Y-%m-%dT%H:%M:%S')
            self.to_date = datetime.strptime(to_date, '%Y-%m-%dT%H:%M:%S')
            self.day_count = (self.to_date - self.from_date).days + 1
        except:
            print "from and to date not specified." 
            pass

    def get_user_stats(self, username, metric, period="daily"):
      
        merged_res = []
        # instance based data
        for i in range(0, int(self.instances.count())):
            instance = self.instances.getdata(i)
            if instance["ownerId"] != username:
                continue
            res = self.daily_histogram(instance, metric)
            merged_res = self.merge_daily_histogram(res, merged_res, "sum") # Or "avg"
        return merged_res

    # This is going to be counting hours for daily
    # This logic is kind of messy, will be changed/updated though soon, Hopefully.
    def daily_histogram(self, instance, metric):
        ''' Make a list filled with metric values in a daily basis.
            The size of the list is the date range of analyze. 
            e.g. [0 (1st), 0 (2nd), ... , 0 (31th)] list will be 
            returned when 'analyze -M 01' which is for January 2012
            is requested. '''

        month = [ 0 for n in range(self.day_count) ]
        if instance["t_end"] < self.from_date or instance["t_start"] > self.to_date :
            #print "This instance data is out of analyzing range." + "(" + str(instance["t_start"]) + "," + str(instance["t_end"]) + ")"
            return month
        offset = (instance["t_start"] - self.from_date).days

        day_count_ins = (instance["t_end"] - instance["t_start"]).days + 1
        i = 0
        for single_date in (instance["t_start"] + timedelta(n) for n in range(day_count_ins)):
            if single_date > self.to_date:
                break
            if metric == "runtime":
                a = datetime.strptime("00:00:00", "%H:%M:%S")
                first_second_of_a_day = datetime.combine(single_date.date(), a.time())
                last_second_of_a_day = first_second_of_a_day + timedelta(days=1)
                if i == 0:
                    td = last_second_of_a_day - single_date
                    hour = td.seconds / 60 / 60
                    month[offset + i] = hour
                elif i + 1 == day_count_ins:
                    td = instance["t_end"] - first_second_of_a_day
                    hour = td.seconds / 60 / 60
                    month[offset + i] = hour
                else:
                    month[offset + i] = 24 # hours
            i += 1
        td = instance["t_end"] - instance["t_start"]

        if metric == "runtime":
            if day_count_ins == 1:
                td = instance["t_end"] - instance["t_start"]
                hour = td.seconds / 60 / 60
                month[offset] = hour
        return month

    def merge_daily_histogram(self, new, current, type="sum"):
        ''' merge daily_historam lists 
            e.g. [1,2,3] + [2,3,4]
            expect => [ 1+2, 2+3, 3+4] = [ 3, 5, 7]
        '''
        if len(current) == 0:
            current = [0 for n in range(self.day_count) ]

        if type == "avg":
            divide = 2.0
        else:
            divide = 1.0

        array = [new, current]
        return [(sum(a)/divide) for a in zip(*array)]

    def line_chart(self, output):
       
        maxY = int(round(max(self.user_stats) / 10) * 10)
        chart = PyGoogleChart("line", maxY)
        chart.set_data(self.user_stats)
        #chart.set_data(value2)
        
        # + 1 will add last value to the list. In here, the last value is 24
        chart.set_yaxis([ str(x)+"hr" for x in range(0, maxY + 1, (maxY / 4))])
        chart.set_xaxis([ str(x)+"d" for x in range(0, self.day_count + 1, 3)])
        chart.set_output_path(output)
        chart.set_filename(self.userid + "-" + "linechart.png")
        chart.display()
        print chart.filepath + "/" + chart.filename + " created."

    def display_stats(self, metric="count", type="pie", filepath="chart.png"):
        """ filepath = display, filepath = url, filepath = real filepath"""
        """displays the number of VMs a user is running"""
        """ types supported pie, bar"""

        values = []
        label_values = []
        max_v = 0

        for name in self.users:
            number = self.users[name][metric]
            # Temporary lines for converting sec to min 
            if metric != "count":
                number = int (number / 60)
            values.append(number)
            label_values.append(name + ":" + str(number))
            max_v = max(max_v, number)

        if type == "pie": 
            chart = PieChart3D(500, 200)
            chart.set_pie_labels(label_values)
        if type == "bar":
            chart = StackedHorizontalBarChart(500,200,
                                            x_range=(0, max_v))
            # the labels seem wrong, not sure why i have to call reverse
            chart.set_axis_labels('y', reversed(label_values))
            # setting the x axis labels
            interval = int(max_v) / 10
            left_axis = range(0, int(max_v + 1), interval)
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
            Utility.ensure_dir(filepath)
            chart.download(filepath)

    def make_index_html (self, output_dir, title):
        '''this command is in the worng file'''
        page_template = HtmlTemplate.index()
        now = datetime.now()
        now = "%s-%s-%s %s:%s:%s" %  (now.year, now.month, now.day, now.hour, now.minute, now.second)
        gmc = GoogleMotionChart()
        motion_chart = gmc.display(self.users, str(self.from_date))
        filename = output_dir+"/index.html"
        Utility.ensure_dir(filename)
        f = open(filename, "w")
        f.write(page_template % vars())
        f.close()
    
    def make_frame_html (self):
        '''this command is in the worng file'''
        page_template = HtmlTemplate.frame()
        filename = "index.html"
        f = open(filename, "w")
        f.write(page_template)
        f.close()

    def make_menu_html (self, directories):
        '''this command is in the worng file'''
        page_template = str("<b>Metrics</b><br><b>Monthly VM Ussage by User</b><ul>")
        for dirname in directories:
            page_template += "<li><a href=\"" + dirname + "/index.html\" target=right> VM usage by day " + dirname + "</a></li>\n"
        page_template += str("</ul>")
        filename = "menu.html"
        f = open(filename, "w")
        f.write(page_template)
        f.close()

    def make_google_motion_chart(self, directory):
        '''this command is in the worng file'''
        filename = "FGGoogleMotionChart.html"
        filepath = directory + "/" + filename
        Utility.ensure_dir(filepath)
        test = GoogleMotionChart()
        output = test.display(self.users, str(self.from_date))
        f = open(filepath, "w")
        f.write(output)
        f.close()
        print filepath + " created"

    def preloop(self):
        self.do_loaddb("")

    def postloop(self):
        print "BYE ..."

    # def do_server_start (self,arg):
    #     os.system('lighttpd -D -f lighttpd.conf &')


    # def do_server_stop (self,arg):
    #     os.system('killall lighttpd')

    def do_changecharttype (self, arg):
        '''changes the default caht type. You can choese bar, pie, motion'''
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
        '''prints a table from the instance data'''
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
        # configuration file
        # if no parameter is given config is read from ~/.futuregrid/futuregrid.cfg
        print "\r... loading data from database"
        self.users = {}
        self.instances = Instances()
        # gets also data from the database
        self.instances.read_from_db()
        print "\r... data loaded"

    def do_pause(slef, arg):
        '''Waits for a return to be typed in with the keyboard'''
        os.system("pause")

    def do_dump(self, arg):
        '''Prints the data from all instances.'''
        # if we specify key, prints it from an instance with a given instance id
        self.instances.dump()

    def do_printlist(self, arg):
        '''lists all instance ids id's'''
        # takes as additional parameters fields to be printed

        print "\n... list\n"
        self.instances.print_list(arg)

    def do_clear(self, arg):
        '''clears all instance data and user data from the memory'''
        if arg == "users":
            self.users = {}
        elif arg == "instances":
            self.instances = {}

    @options([
        make_option('-f', '--start', default="all", type="string", help="start time of the interval (type. YYYY-MM-DDThh:mm:ss)"),
        make_option('-t', '--end',  default="all",  type="string", help="end time of the interval (type. YYYY-MM-DDThh:mm:ss)"),
        make_option('-M', '--month', type="string", help="month to analyze (type. MM)"),
        make_option('-Y', '--year', type="string", help="year to analyze (type. YYYY)"),
        ])
    def do_analyze (self, arg, opts=None):

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

        self.instances.refresh()
        print "now calculating"
        self.calculate_stats (from_date, to_date)

    def do_getdaterange(self, arg): 
        '''Get Date range of the instances table in mysql db'''
        res = self.instances.getDateRange()
        print Utility.convertOutput(res[0], "first_date")
        print Utility.convertOutput(res[1], "last_date")
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
        graph_type =  opts.type
        filepath = opts.filepath
        print graph_type + " typed " + filepath + " file created"
        self.display_stats("all", "count", graph_type, filepath)

    @options([
        make_option('-d', '--directory', type="string", help="directory name which the chart html will be stored.")
        ])
    def do_createhtml(self, arg):
        self.make_google_motion_chart(opts.directory)

    @options([
        make_option('-d', '--directory', type="string", help="directory name which contains report graphs."),
        make_option('-t', '--title', type="string", help="A report title in the index.html")
        ])
    def do_createreport(self, arg, opts=None):
        self.display_stats("count", "pie", opts.directory + "/pie.count.png")
        self.display_stats("count", "bar", opts.directory + "/bar.count.png")
        self.display_stats("sum", "pie", opts.directory + "/pie.sum.png")
        self.display_stats("sum", "bar", opts.directory + "/bar.sum.png")

        #self.make_google_motion_chart(opts.directory)
        self.make_index_html(opts.directory, opts.title)

    def do_createreports(self, arg):
        self.make_frame_html()
        self.make_menu_html(arg.split())

    @options([
        make_option('-f', '--start', type="string", help="start time of the interval (type. YYYY-MM-DDThh:mm:ss)"),
        make_option('-t', '--end',  type="string", help="end time of the interval (type. YYYY-MM-DDThh:mm:ss)"),
        make_option('-M', '--month', default=datetime.now().month, type="string", help="month to analyze (type. MM)"),
        make_option('-Y', '--year', default=datetime.now().year, type="string", help="year to analyze (type. YYYY)"),
        ])
    def do_set_range (self, arg, opts=None):

        if opts.start and opts.end:
            from_date = opts.start
            to_date = opts.end
        else:
            from_date = "%s-%s-01T00:00:00" % (opts.year, opts.month)
            to_date = "%s-%s-%sT23:59:59" % (opts.year, opts.month,
                    str(calendar.monthrange(int(opts.year), int(opts.month))[1]))

        print "Set date range to analyze: [" + from_date + ", " + to_date + "]" 
        self.set_date(from_date, to_date)

    @options([
        make_option('-u', '--user', type="string", help="user id to analyze"),
        make_option('-m', '--metric', default="runtime", type="string", help="metric name to display (runtime, vms)")
        ])
    def do_analyze_user(self, arg, opts=None):
        if not opts.user:
            print "user id is required."
            return

        self.user_stats = self.get_user_stats(opts.user, opts.metric)
        self.userid = opts.user

    @options([
        make_option('-o', '--output', type="string", help="the filepath in which we store a chart")
        ])
    def do_user_report(self, arg, opts=None):
        # set default output by Year-month typed string
        if not opts.output:
            opts.output = str(self.from_date.year) + "-" + str(self.from_date.month)

        self.line_chart(opts.output)

        print
        print "This line chart displays statistics of a specific user's metric."
        print self.userid + " (userid) is selected to display 'instance runtime' of " + str(self.from_date.month) + "/" + str(self.from_date.year) + "."
        print "Y-axis indicates total running hours of instances."
        print "X-axis indicates date of the month."
        print

    def do_filled_line_example(self, arg, opts=None):
        chart = PyGoogleChart("line", 0)
        chart.filledLineExample()

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
