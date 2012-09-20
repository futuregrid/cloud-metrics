from datetime import *

class FGSearch:

    '''
    name = None
    from_date = None
    to_date = None
    day_count = None
    period = None
    selected = []
    metric = {}
    groupby = None
    sub_groupby = None
    #groupby3 ...

    project = None
    nodename = None
    platform = None
    userid = None
    username = None

    calc = None # count, avg, min, max, sum
    column = None
    sub_column = None
    '''

    def __init__(self):
        self.init_options()
        self.init_suboptions()
        self.init_stats()
        self.keys_to_select = { 'uidentifier', 't_start', 't_end', 'duration', 'serviceTag', 'ownerId', 'ccvm', 'hostname', 'cloudplatform.platform'} #_mem', 'ccvm_cores', 'ccvm_disk' }

    def init_options(self):
        self.from_date = None
        self.from_date = None
        self.day_count = None
        self.project = None
        self.nodename = None
        self.platform = None
        self.userid = None
        self.username = None

    def init_suboptions(self):
        self.calc = None
        self.groupby = None
        self.sub_groupby = None
        self.column = None
        self.sub_column = None

        self.groups = None
 
    def init_stats(self):
        self.name = None
        self.selected = []
        self.metric = {}
        self.metrics = {}

    def set_metric(self, name):
        self.init_stats()
        self.name = name
        self.init_suboptions()
        self.set_default_suboptions()

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

    def set_subgroupby(self, name):
        self.sub_groupby = name

    def set_groups(self, glist):
        self.groups = glist

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
        return dict((key, instance[key]) for key in keys)

    def get_val(self, _dict, keys):
        return list(_dict[key] for key in keys)

    def get_metric(self):
        return self.metric

    def collect(self, instance):
        metric = self.name
        selected = self.select(instance)
        self.selected.append(selected)
        #self.update_metric(selected)
        #return selected
        glist = self.get_val(selected, self.groups)
        value = self.get_column(selected)
        self.update_metrics(glist, self.metric, self.name, value)
        return True

    def update_metrics(self, glist, mdict, key, value):
        if len(glist) == 0:
            new = value
            old = None
            if key in mdict:
                old = mdict[key]
            mdict[key] = self.calculate(old, new)
            return mdict[key]

        group = glist.pop(0)
        if not group in mdict:
            mdict[group] = {}
        return self.update_metrics(glist, mdict[group], key, value)

    def update_metric(self, selected):
        metric = self.name
        index = selected[self.groupby]
        new = self.get_column(selected)
        old = None

        if index in self.metric:
            old = self.metric[index][metric]
        self.metric[index][metric] = self.calculate(old, new)

        ''' two issues still I have
        1) how to handle 2 groupby s, one nested dict needed
        2) get_column will get an error due to missing groupby columns. should I change it back to use instance?
        '''

    def set_default_suboptions(self):
        metric = self.name
        if not metric: 
            return

        if metric == "count":
            self.calc = "count"
            self.groupby = "ownerId"
        elif metric == "runtime":
            self.calc = "sum"
            self.column = "duration"
            self.groupby = "ownerId"
        elif metric == "ccvm_cores" or metric == "cpu":
            self.calc = "sum"
            self.column = "ccvm"
            self.column2 = "cores"
            self.groupby = "instance.cloudplatform"
            self.sub_groupby = "date"
        elif metric == "ccvm_mem" or metric == "mem":
            self.calc = "sum"
            self.column = "ccvm"
            self.column2 = "mem"
            self.groupby = "instance.cloudplatform"
            self.sub_groupby = "date"
        elif metric == "ccvm_disks" or metric == "disk":
            self.calc = "sum"
            self.column = "ccvm"
            self.column2 = "disk"
            self.groupby = "instance.cloudplatform"
            self.sub_groupby = "date"

    def get_column(self, selected):
        if self.column in selected:
            return selected[self.column]
        else:
            return 1

    def calculate(self, old, new):
        if self.calc == "count":
            return (old or 0) + 1
        elif self.calc == "sum":
            return (old or 0) + new
        elif self.calc == "avg":
            return (old or 0) + new / 2
        elif self.calc == "min":
            return min(old or new, new)
        elif self.calc == "max":
            return max(old or new, new)

    def clear(self):
        self.__init__()
