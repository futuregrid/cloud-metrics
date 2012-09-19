from cmd2 import Cmd
import pprint
from fgmetric.FGSearch import FGSearch
from fgmetric.FGInstances import FGInstances
from fgmetric.FGNovaMetric import FGNovaMetric

class FGMetrics(Cmd):
    ''' This class name should be back to FGAnalyzer '''

    ''' This is a development version '''

    instances = None
    users = None
    nova = None
    search = None

    def __init__(self):
        Cmd.__init__(self)
        self.prompt = "fg-metric] "
        self.intro = "Welcome to FutureGrid Cloud Metrics!"
        self.search = FGSearch()

    def initialize(self, arg="all"):
        """Clear all instance data and user data on the memory"""
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

    def load_db(self):
        """Read the statistical data from database (MySQL, etc)"""
        
        print "\r... loading database"
        self.users = {}
        self.instances = FGInstances()
        self.nova = FGNovaMetric()
        # Get data from the database
        self.instances.read_from_db()
        # Get also userinfo data from the database
        self.instances.read_userinfo_from_db()
        # Get also nova data from the database
        self.nova.read_from_db()
        print "\r... database loaded"

    def display_filter_setting(self):
        pprint.pprint(vars(self.search.get_filter()))

    def get_measure(self):

        total_counts = self.instances.count()

        print "Calculating metrics in " + str(total_counts) + " records...\n"

        for i in range(0, total_counts):
            instance = self.instances.get_data(i)
            if not self.search._is_in_date(instance):
                continue;
            if not self.search._is_filtered(instance):
                continue;

            res = self.search.collect(instance)

        self.search.get_metric()

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

    def do_load_db(self, args):
        self.load_db()

    def do_analyze(self, args):
       
        self.display_filter_setting()
        self.get_measure()
        #self.create_charts()

    def do_set (self, line, opts=None):
        """Set a function with parameter(s)"""

        args = line.split()
        cmd = args[0]
        params = args[1:]
        function = "set_" + cmd

        if len(args) == 2:
            params = args[1]

        try:
            func = getattr(self.search, function)
            func(params)

            print "Search option for '" + cmd + "' is set as : " + "" . join(params)
        except:
            print "Search option for '" + cmd + "' isn't set as : " + "" . join(params)
            pass

    def do_show (self, args):
        '''show search options set by a user'''
        self.display_filter_setting()

    def preloop(self):
        self.load_db()
        self.initialize()

    def postloop(self):
        print "Bye ..."

def main():
    app = FGMetrics()
    app.cmdloop()

if __name__ == "__main__":
    main()
