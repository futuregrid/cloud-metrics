#!/usr/bin/env python

#import argparse

from futuregrid.eucalyptus.analyzer.FGParser import Instances

from pygooglechart import PieChart3D
from pygooglechart import StackedHorizontalBarChart
from pygooglechart import Axis

import os
import pprint
import optparse
from cmd2 import Cmd
from cmd2 import make_option
from cmd2 import options
from cmd2 import Cmd2TestCase
from datetime import *

import unittest, sys
import calendar


class CmdLineAnalyzeEucaData(Cmd):
    #multilineCommands = ['None']
    #Cmd.shortcuts.update({'&': 'speak'})
    #maxrepeats = 3
    #Cmd.settable.append('maxrepeats')

    instances = {}
    users = {}
    pp = pprint.PrettyPrinter(indent=0)
    charttype = "pie"

    echo = True
    timing = True


    def calculate_user_stats (self, from_date="all", to_date="all"):
        """calculates some elementary statusticks about the instances per user: count, min time, max time, avg time, total time"""

        # handle parameters

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

        print self.instances.count()
        for i in self.instances.get():
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



    def display_user_stats(self, type="pie", filename="chart.png"):
        """ filename = display, filename = url, filename = real filename"""
        """displays the number of VMs a user is running"""
        """ types supported pie, bar"""

        values = []
        label_values = []

        #        print self.users

        
        max_v = 0
        for name in self.users:
            number = self.users[name]['count']
            values.append(number)
            label_values.append(name + ":" + str(number))
            max_v = max(max_v, number)

        # print values
        # print label_values

        if type == "pie": 
            chart = PieChart3D(500, 200)
            chart.set_pie_labels(label_values)
        if type == "bar":
            chart = StackedHorizontalBarChart(500,200,
                                            x_range=(0, max_v))
            # the labels seem wrong, not sure why i have to call reverse
            chart.set_axis_labels('y', reversed(label_values))
            # setting the x axis labels
            left_axis = range(0, max_v + 1, 1)
            left_axis[0] = ''
            chart.set_axis_labels(Axis.BOTTOM, left_axis)

            chart.set_bar_width(10)
            chart.set_colours(['00ff00', 'ff0000'])

        # Add some data
        chart.add_data(values)

        # Assign the labels to the pie data

        if filename == "display":
            #os.system ("open -a /Applications/Safari.app " + '"' + url + '"')
            os.system ("open " + filename)
        elif filename == "url":
            url = chart.get_url()
            print url
        else:
            chart.download(filename)


    def preloop(self):
        self.do_loaddb("")
        
    def postloop(self):
        print "BYE ..."
        

    def do_charttype (self, arg):
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
        os.system("pause")

    def do_dump(self, arg):
        # prints the data from all instances
        # if we specify key, prints it from an instance with a given instance id
        self.instances.dump()

    def do_printlist(self, arg):
        print "\n... list\n"
        # lists all instance ids id's
        # takes as additional parameters fields to be printed
        self.instances.print_list(arg)

    def do_clear(self, arg):
        if arg == "users":
            self.users = {}
        elif arg == "instances":
            self.instances = {}

    @options([
        make_option('-f', '--start', default="all", type="string", help="start time of the interval YYYYMMDDThh:mm:ss"),
        make_option('-t', '--end',  default="all",  type="string", help="end time of the interval YYYYMMDDThh:mm:ss"),
        make_option('-M', '--month', type="string", help="month of the interval MM"),
        make_option('-Y', '--year', type="string", help="year of the interval YYYY"),
        ])
    def do_analyze (self, arg, opts=None):

        print ">", opts.month
        print ">", opts.year

        if opts.year:
            analyze_year = opts.year
            if opts.month:
                analyze_month = opts.month
        else:
            if opts.month:
                now = datetime.now()
                analyze_year = str(now.year)  
                analyze_month = str(opts.month) 

        
        if (opts.year != None) or (opts.month != None):
            from_date = "%s-%s-01T00:00:00" % (analyze_year,
                                               analyze_month)
                # TODO: this misses one second
            to_date =   "%s-%s-%sT23:59:59" % (analyze_year,
                                               analyze_month,
                                               str(calendar.monthrange(int(analyze_year), int(analyze_month))[1]))
        else:
            from_date = opts.start
            to_date = opts.end


            
        print "analyze [" + from_date + ", " + to_date + "]" 

        self.instances.refresh()
        print "now calculating"
        self.calculate_user_stats (from_date=from_date, to_date=to_date)

    def do_printusers(self, arg):
        print self.pp.pprint(self.users)
            
    def do_timing (self, arg):
        self.timing = True

    def do_echo (self, arg):
        self.echo = True

    def do_open(self,arg):
        os.system ("open " + arg)
        
    @options([
        make_option('-t', '--type', type="string", help="pie, bar, motion"),
        make_option('-f', '--filename', type="string", help="the filename to which we store the graph")
        ])
    def do_graph(self, arg, opts=None):
        if opts.type==None:
            graph_type = self.charttype
        else:
            graph_type=opts.type
        if opts.filename==None:
            display_type = "display"
        else:
            display_type = opts.filename

        self.display_user_stats(graph_type,filename=display_type)

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
