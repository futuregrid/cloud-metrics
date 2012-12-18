from datetime import *
from fgmetric.FGUtility import dotdict
from math import ceil
from pprint import pprint
from fgmetric.FGUtility import FGUtility

class FGSearch:

    '''
    metric = None
    from_date = None
    to_date = None
    day_count = None
    period = None
    selected = []
    metric = {}
    #groupby3 ...

    project = None
    nodename = None
    platform = None
    userid = None
    username = None

    calc = None # count, avg, min, max, sum
    '''

    def __init__(self):
        self.init_options()
        self.init_suboptions()
        self.init_stats()
        self.keys_to_select = { 'uidentifier', 't_start', 't_end', 'duration', 'serviceTag', 'ownerId', 'ccvm', 'hostname', 'cloudplatform.platform', 'trace'} #_mem', 'ccvm_cores', 'ccvm_disk' }
        self.init_names()

    def init_options(self):
        self.from_date = None
        self.to_date = None
        self.day_count = 0
        self.project = None
        self.nodename = None
        self.platform = None
        self.userid = None
        self.username = None

    def init_suboptions(self):
        self.calc = None
        self.columns = None
        self.period = None

        self.groups = ["All"]
 
    def init_stats(self):
        self.metric = None
        self.selected = []
        self.selected_idx = 0
        self.stats = {}

    def init_names(self):
        self.names = dotdict({"metric": dotdict({"count":"count", 
                                                "runtime":"runtime", 
                                                "cores":["cpu", "ccvm_cores", "core", "cores"], 
                                                "memories":["mem", "ccvm_mem", "memory", "memories"], 
                                                "disks":["disk", "ccvm_disk", "disks"]}),
                            "calc":dotdict({"count":"count", 
                                            "summation":"sum", 
                                            "average":"avg", 
                                            "minimum":"min", 
                                            "maximum":"max" })
            })

    def set_metric(self, name):
        #self.init_stats()
        self.metric = name
        #self.init_suboptions()
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

    def set_groups(self, glist):
        try:
            glist = glist.split()
        except:
            pass

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
            self.day_count = (self.to_date - self.from_date).days
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

    def _is_searching_all(self):
        if not self.from_date and not self.to_date:
            return True
        return False

    def _is_in_date(self, instance):

        if self._is_searching_all():
            return True
        if (instance["t_start"] > self.to_date) or (instance["t_end"] and instance["t_end"] < self.from_date):
            return False
        #Newly added for exception
        if instance["trace"]["extant"]["stop"] and instance["trace"]["extant"]["stop"] < self.from_date:
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

    def get_vals(self, _dict, keys):
        ''' Same as get_val but handles non-exist keys '''
        lis = []
        if not keys:
            return lis

        for key in keys:
            if key in _dict:
                lis.append(_dict[key])
            else:
                lis.append(key)
        return lis

    def get_metric(self):
        return self.stats

    def collect(self, instance):
        #metric = self.metric
        selected = self.select(instance)
        self.appendi(selected)
        glist = self.get_vals(selected, self.groups)
        value = self.get_metricfactor(self.columns, selected)
        self.update_metrics(glist, self.stats, self.metric, value)
        return True

    def update_metrics(self, glist, mdict, key, value):
        if len(glist) == 0:
            new = value
            if key in mdict:
                old = mdict[key]["Total"]
            else:
                old = None
                mdict[key] = { "Total" : None }
            mdict[key]["Total"] = self.calculate(old, new)
            ############################
            # Add daily dict temporarily
            try:
                period_func = getattr(self, "_divide_into_" + str(self.period))
                period_func(mdict[key], value)
            except:
                pass
            # ##########################
            return mdict[key]

        group = glist.pop(0)
        if not group in mdict:
            mdict[group] = {}
        return self.update_metrics(glist, mdict[group], key, value)

    def update_metric(self, selected):
        metric = self.metric
        index = selected[self.groupby]
        new = self.get_metricfactor(self.columns, selected)
        old = None

        if index in self.stats:
            old = self.stats[index][metric]
        self.stats[index][metric] = self.calculate(old, new)

        ''' two issues still I have
        1) how to handle 2 groupby s, one nested dict needed
        2) get_metricfactor will get an error due to missing groupby columns. should I change it back to use instance?
        '''

    def _divide_into_None(self, mdict, value):
        return

    def _divide_into_daily(self, mdict, val):
        selected = self.get_recentlyselected()
        t_start = selected['t_start']
        t_end = selected['t_end']
        #self.start_date
        #self.to_date
        #self.stats
        #val = mdict[self.metric]

        if not self.period in mdict:
            mdict[self.period] = {}

        for single_date in (self.from_date + timedelta(n) for n in range(self.day_count)):
            res = self.calculate_daily(t_start, t_end, single_date, val)
            if single_date in mdict[self.period]:
                mdict[self.period][single_date] += res
            else:
                mdict[self.period][single_date] = res

            ''' this is where I need to put calculation of daily basis metrics.
            what I need to do is following:
            1) create [date] = value
            ...
            how?
            1.1) t_start is older than single date?
            
            Search period        |----------------------|
            possible instance
            a.        |----|
            b.        |--------------|
            c.        |---------------------------------|
            d.        |------------------------------------------|
            e.                   |-----------|
            f.                   |----------------------|
            g.                   |-------------------------------|
            h.                               |-----|
            i.                               |----------|
            j.                               |-------------------|
            k.                                             |-----|
            9 possible ways to count
            But a. and k. are not the cases because this function is supposed to be executed after checking is_in_date function,
            which means we assume the instance is in the search date.

            2) Then calculate (old, new) ? for sum,avg, etc?

            3)

            '''
        return

    def calculate_daily(self, t_start, t_end, single_date, value):
        metric = self.metric

        single_start = single_date
        if single_start != self.from_date:
            single_start = datetime.combine(single_date.date(), datetime.strptime("00:00:00", "%H:%M:%S").time())

        single_end = datetime.combine(single_start + timedelta(days=1), datetime.strptime("00:00:00", "%H:%M:%S").time())
        if single_end > self.to_date:
            single_end = self.to_date

        if t_start > single_end or t_end < single_start:
            return 0

        # temporarily added for the exception
        selected = self.get_recentlyselected()
        if selected["trace"]["extant"]["stop"]:
            if selected["trace"]["extant"]["stop"] > datetime(1970, 1, 1) and selected["trace"]["extant"]["stop"] < single_start:
                return 0

        if metric == self.names.metric.runtime:
            if t_start < single_start:
                start_time =  single_start
            else:
                start_time = t_start

            if t_end > single_end:
                end_time = single_end
            else:
                end_time = t_end

            # temporarily added
            if t_end == datetime(3000, 1, 1):
                if selected["trace"]["extant"]["stop"]:
                    if selected["trace"]["extant"]["stop"] > datetime(1970, 1, 1) and selected["trace"]["extant"]["stop"] < single_end:
                        end_time = selected["trace"]["extant"]["stop"]

            td = end_time - start_time
            res = td.seconds#int(ceil(float(td.seconds) / 60 / 60))
            return res
        elif metric == self.names.metric.count:
            return 1
        elif metric in self.names.metric.cores or self.names.metric.memories or self.names.metric.disks:
            return value

    def set_default_suboptions(self):
        metric = self.metric
        if not metric: 
            return

        if metric == self.names.metric.count:
            self.calc = "count"
        elif metric == self.names.metric.runtime:
            self.calc = "sum"
            self.columns = ["duration"]
            self.groups = ["ownerId"]
        elif metric in self.names.metric.cores:
            self.calc = "sum"
            self.columns = ["ccvm", "cores"]
            self.groups = ["instance.cloudPlatformIdRef"]
            self.period = "daily"
        elif metric in self.names.metric.memories:
            self.calc = "sum"
            self.columns = ["ccvm", "mem"]
            self.groups = ["instance.cloudPlatformIdRef"]
            self.period = "daily"
        elif metric in self.names.metric.disks:
            self.calc = "sum"
            self.columns = ["ccvm", "disk"]
            self.groups = ["instance.cloudPlatformIdRef"]
            self.period = "daily"

    def get_metricfactor(self, columns, selected):
        if columns is None:
            return 1
        if len(columns) == 0:
            return selected
        return self.get_metricfactor(columns[1:], selected[columns[0]])

    def calculate(self, old, new):
        if self.calc == self.names.calc.count:
            return (old or 0) + 1
        elif self.calc == self.names.calc.summation:
            return (old or 0) + new
        elif self.calc == self.names.calc.average:
            return (old or 0) + new / 2
        elif self.calc == self.names.calc.minimum:
            return min(old or new, new)
        elif self.calc == self.names.calc.maximum:
            return max(old or new, new)

    def appendi(self, selected):
        self.selected.append(selected)
        self.selected_idx = len(self.selected)

    def get_recentlyselected(self):
        if self.selected_idx == 0:
            return
        return self.selected[self.selected_idx - 1]

    def show_None(self, param=None):
        self.show_filter()

    def show_filter(self):
        pprint(vars(self.get_filter()))

    def clear(self):
        self.__init__()
