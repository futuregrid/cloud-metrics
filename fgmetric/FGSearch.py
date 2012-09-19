from datetime import *

class FGSearch:

    name = None
    from_date = None
    to_date = None
    day_count = None
    period = None
    selected = []
    metric = {}
    groupby = None
    groupby2 = None
    #groupby3 ...

    project = None
    nodename = None
    platform = None
    userid = None
    username = None

    calc = None # count, avg, min, max, sum
    column = None

    result = None

    def __init__(self):
        self.name = None
        self.keys_to_select = { 'uidentifier', 't_start', 't_end', 'duration', 'serviceTag', 'ownerId', 'ccvm_mem', 'ccvm_cores', 'ccvm_disk' }

    def set_metric(self, name):
        self.name = name
        self.set_default_options()

    def set_period(self, name):
        self.period = name

    def set_username(self, name):
        self.username = name

    def set_platform(self, name):
        self.platform = name

    def set_nodename(self, name):
        self.nodename = name

    def set_groupby(self, name):
        self.groupby = name

    def set_date(self, dates):
        """Set search/analyze period

            Args:
                from_date (str): first date of calculation. '%Y-%m-%dT%H:%M:%S' is only allowed.
                to_date (str): end date of calculation.
            Returns:
                n/a
            Raises:
                n/a

        """
        if len(dates) < 2:
            return

        from_date = dates[0]
        to_date = dates[1]

        try:
            self.from_date = datetime.strptime(from_date, '%Y-%m-%dT%H:%M:%S')
            self.to_date = datetime.strptime(to_date, '%Y-%m-%dT%H:%M:%S')
            self.day_count = (self.to_date - self.from_date).days + 1
        except:
            print "from and to are not specified."
            pass

    def set_period(self, name):
        self.period = name

    def get_filter(self, name=None):
        if name and name in self:
            return self.name
        else:
            return self

    def _is_in_date(self, instance):
        if instance["t_end"] < self.from_date or instance["t_start"] > self.to_date:
           return False
        return True

    def _is_filtered(self, instance):
        if self.username and self.username != instance["ownerId"]:
            return False
        if self.nodename and self.nodename != instance["hostname"]:
            return False
        if self.platform and self.platform != instance["cloudplatform.platform"]:
            return False
        return True

    def set_search_date(self, from_date, to_date):
        self.set_date(from_date, to_date)

    def select(self, instance):
        return self.get(instance, self.keys_to_select)

    def get(self, instance, keys):
        self.result = dict((key, instance[key]) for key in keys)
        return self.result

    def get_metric(self):
        return self.metric

    def collect(self, instance):
        metric = self.name
        res = self.select(instance)
        #index = res['uidentifier']

        #if not index in self.selected:
        self.selected.append(res)
        self.update_metric(res)

    def update_metric(self, selected):
        metric = self.name
        index = selected[self.groupby]
        new = self.get_column(selected)

        if not index in self.metric:
            self.metric[index] = { metric: new }
        else:
            old = self.metric[index][metric]
            self.metric[index][metric] = self.calculate(old, new)

        ''' two issues still I have
        1) how to handle 2 groupby s, one nested dict needed
        2) get_column will get an error due to missing groupby columns. should I change it back to use instance?
        '''

    def set_default_options(self):
        metric = self.name
        if not metric: 
            return

        if metric == "count":
            self.calc = "count"
            self.groupby = "ownerId"
        else if metric == "runtime":
            self.calc = "sum"
            self.column = "duration"
            self.groupby = "ownerId"
        else if metric == "ccvm_cores" or metric == "cpu":
            self.calc = "sum"
            self.column = "ccvm_cores"
            self.groupby = "instance.cloudplatform"
            self.groupby2 = "date"
        else if metric == "ccvm_mem" or metric == "mem":
            self.calc = "sum"
            self.column = "ccvm_mem"
            self.groupby = "instance.cloudplatform"
            self.groupby2 = "date"
        else if metric == "ccvm_disks" or metric == "disk":
            self.calc = "sum"
            self.column = "ccvm_mem"
            self.groupby = "instance.cloudplatform"
            self.groupby2 = "date"

    def get_cloumn(self, selected):
        if self.column in selected:
            return selected[self.column]
        else:
            return 1

    def calculate(self, old, new):
        if self.calc == "count":
            return int(old) + 1
        else if self.calc == "sum":
            return old + new
        else if self.calc == "avg":
            return old + new / 2
        else if self.calc == "min":
            return min(old, new)
        else if self.calc == "max":
            return max(old, new)
