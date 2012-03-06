#!/usr/bin/env python
#THIS DOCUMENT IS TO BE COMPLETED, JUST A START

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

import unittest, sys

def display_user_stats(users, type="pie", filename="chart.png"):
    """ filename = display, filename = url, filename = real filename"""
    """displays the number of VMs a user is running"""
    """ types supported pie, bar"""
    
    values = []
    label_values = []

    max_v = 0
    for name in users:
        print name
        count = users[name]['count']
        print count
        values.append(count)
        label_values.append(name + ":" + str(count))
        max_v = max(max_v, count)

    print values
    print label_values

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


class CmdLineAnalyzeEucaData(Cmd):
    #multilineCommands = ['None']
    #Cmd.shortcuts.update({'&': 'speak'})
    #maxrepeats = 3
    #Cmd.settable.append('maxrepeats')

    instances = None
    users = None
    pp = pprint.PrettyPrinter(indent=0)
    charttype = "pie"

    echo = True
    timing = True

    def preloop(self):
        self.do_loaddb("")
        
    def postloop(self):
        print "BYE FORM GREGOR"
        

    def do_charttype (self, arg):
        if (arg != "pie") and (arg != "bar") and (arg != "motion"):
            print "Error: charttype " + arg + " not supported."
        else:
            print "Setting chart type to " + arg
            self.charttype = arg
        
    
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

    def do_clear(slef, arg):
        if arg == "users":
            self.users = {}
        elif arg == "instances":
            self.instances = {}

    @options([
        make_option('-f', '--start', type="string", help="start time of the interval YYYYMMDD"),
        make_option('-t', '--end', type="string", help="end time of the interval YYYYMMDD"),
        ])
    def do_analyze (self, arg, opts=None):

        to_date="all"
        if opts.start == "" or opts.start == None:
            from_date="all"
        else:
            from_date = opts.start
            
        if opts.end == "" or opts.end == None:
            to_date="all"
        else:
            to_date = opts.end

        print "analyze [" + from_date + ", " + to_date + "]" 
            
        self.instances.calculate_delta ()
        self.instances.calculate_user_stats (self.users, from_date=from_date, to_date=to_date)

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

        display_user_stats(self.users, graph_type,filename=display_type)


parser = optparse.OptionParser()
parser.add_option('-t', '--test', dest='unittests', action='store_true', default=False, help='Run unit test suite')
(callopts, callargs) = parser.parse_args()
if callopts.unittests:
    sys.argv = [sys.argv[0]]  # the --test argument upsets unittest.main()
    unittest.main()
else:
    app = CmdLineAnalyzeEucaData()
    app.cmdloop()


