import re
import sys
import copy
from datetime import datetime, timedelta
from fgmetric.util.FGUtility import dotdict
from fgmetric.util.FGUtility import FGUtility

from math import ceil
from pprint import pprint
from collections import Counter, OrderedDict
from calendar import monthrange


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
    all_name = "All"

    def __init__(self):
        self.init_options()
        self.init_suboptions()
        self.init_internal_options()
        self.init_stats()
        self.keys_to_select = {
            'uidentifier', 't_start', 't_end', 'duration', 'serviceTag', 'ownerId',
            'ccvm', 'hostname', 'cloudplatform.platform', 'trace', 'state', 'date', 'cloudPlatformIdRef'}
        self.keys_to_select_extra = {
            'ProjectId', 'Title', 'Institution', 'ProjectLead', 'Discipline'}  # _mem', 'ccvm_cores', 'ccvm_disk' }
        self.init_names()
        self.userinfo_needed = False
        self.cache = True

    def init_options(self):
        self.from_date = None
        self.to_date = None
        self.day_count = 0
        self.months = None
        self.project = None
        self.nodename = None
        self.platform = None
        self.userid = None
        self.username = None
        self.metric = OrderedDict()
        self.selected_metric = None

    def init_internal_options(self):
        self.calc = None
        self.columns = None
        self.distinct = False
        self.all_nodenames = "India, Sierra, Alamo, Foxtrot, Hotel"  # This should be filled by retrieving db
        self.all_platforms = "Eucalyptus, OpenStack, Nimbus"  # This as well

    def init_suboptions(self):
        self.period = None  # "Total"
        self.groups = [self.all_name]
        self.groupby = None
        self.timetype = None
        self.time_conversion = 1

    def init_stats(self):
        self.selected = []
        self.stats = OrderedDict()  # {}
        self.stats_beta = {"system": None,
                           "service": None,
                           "period": None,
                           "from": None,
                           "to": None,
                           "metric": None,
                           "value": None}
        self.distinct_list = {}

    def init_names(self):
        self.names = dotdict({"metric": dotdict({"count": ["count"],
                                                "countusers": ["countusers"],
                                                "runtime": ["runtime"],
                                                "runtimeusers": ["runtimeusers"],
                                                "cores": ["cpu", "ccvm_cores", "core", "cores"],
                                                "memories": ["mem", "ccvm_mem", "memory", "memories"],
                                                "disks": ["disk", "ccvm_disk", "disks"]}),
                              "calc": dotdict({"count": "count",
                                               "summation": "sum",
                                               "average": "avg",
                                               "minimum": "min",
                                               "maximum": "max"}),
                              "period": dotdict({"daily": "daily",
                                                "monthly": "monthly"}),
                              "timetype": dotdict({"day": "day",
                                                   "hour": "hour",
                                                   "minute": "minute",
                                                   "second": "second"})
                              })

    def check_vailidity(self):
        """Check settings before performing analysis

        There are certain variables that have to be set before calculation.
        1) Date
        2) Metric
        3) (option) hostname
        4) (option) cloudservice

            Raises:
                ValueError
        """
        if not self.from_date or not self.to_date:
            raise ValueError(
                "Missing Dates: please 'set date $from $to' first")
        elif not self.metric:
            raise ValueError("Missing Metric: please 'set metric $name' first")
        else:
            pass

    def set_None(self, line):
        self.set_help(line)

    def set_help(self, line):
        """Display usage"""

        print
        print "Possible commands"
        print "================="
        print " set date $from $to"
        print " set metric $name"
        print " set platform $name"
        print " set nodename $name"
        print " set project $name"
        print " set period $name"
        print

    def help_period(self):
        """Display usage period"""

        print "Possible commands"
        print "================="
        for val in self.names['period'].keys():
            print " set period " + val
        print

    def help_metric(self):
        """Display usage metric"""

        print "Possible commands"
        print "================="
        for val in self.names['metric'].keys():
            print " set metric " + val
        print

    def help_timetype(self):
        """Display usage timetype"""

        print "Possible commands"
        print "================="
        for val in self.names['timetype'].keys():
            print " set timetype " + val
        print

    def set_metric(self, name):
        if name == "help":
            self.help_metric()
        else:
            try:
                metrics = name.split()
            except:
                metrics = name

            self.metric = metrics

    def set_period(self, name):
        if name == "help":
            self.help_period()
        else:
            self.period = name

    def set_username(self, name):
        self.username = name

    def set_cloud(self, name):
        self.set_platform(name)

    def set_cloudservice(self, name):
        self.set_platform(name)

    def set_platform(self, name):
        self.platform = name

    def set_hostname(self, name):
        self.set_nodename(name)

    def set_nodename(self, name):
        self.nodename = name

    def set_project(self, name):
        self.project = name
        self.userinfo_needed = self._is_userinfo_needed(True)

    def set_groupby(self, name):
        self.groupby = name

        self.userinfo_needed = self._is_userinfo_needed(True)

    def set_groups(self, glist):
        try:
            glist = glist.split()
        except:
            pass

        self.groups = glist
        self.userinfo_needed = self._is_userinfo_needed(True)

    def set_date(self, dates):
        """Set search/analyze period

            Args:
                dates (list): start_date and end_date are expected to search. '%Y-%m-%dT%H:%M:%S' is only allowed.
            Returns:
                n/a
            Raises:
                n/a

        """

        try:
            from_date = dates[0]
            to_date = dates[1]
            if isinstance(from_date, datetime):
                self.from_date = from_date
            else:
                self.from_date = datetime.strptime(
                    from_date, '%Y-%m-%dT%H:%M:%S')
            if isinstance(to_date, datetime):
                self.to_date = to_date
            else:
                self.to_date = datetime.strptime(to_date, '%Y-%m-%dT%H:%M:%S')
            self.day_count = (self.to_date - self.from_date).days

            # If dates are set, months are also set.
            self.set_months()
        except:
            print "Usage: set date from_date(YYYY-MM-DDTHH:MM:SS) to_date(YYYY-MM-DDTHH:MM:SS)."
            print "(e.g. set date 2012-01-01T00:00:00 2012-12-31T23:59:59)"
            print
            pass

    def set_timetype(self, typename):
        ''' set time type of data value to print out

            e.g. set datatype hour means output data will be converted from seconds to hours

            Args:
                typename(str): hour
            Returns:
                n/a
            Raises:
                n/a
        '''
        if typename == "help":
            self.help_timetype()
            return

        self.timetype = typename
        if typename == "day":
            self.time_conversion = 60 * 60 * 24
        elif typename == "hour":
            self.time_conversion = 60 * 60
        elif typename == "minute":
            self.time_conversion = 60
        elif typename == "second":
            self.time_conversion = 1

    def _is_in_month(self, month, from_date, to_date):
        """ return a set of common months between the two dates and months searched

            Args:
                from_date (datetime)
                to_date (datetime)
            Returns:
                set
            Raises:
                n/a
        """

        months = self.get_months_between_dates(from_date, to_date)
        return set([month]) & set(months)

    def get_filename(self):
        return self.from_date.strftime("%Y-%m-%dT%H:%M:%S") + "-" + self.to_date.strftime("%Y-%m-%dT%H:%M:%S") + "-" + str(''.join(self.metric)) + "-" + str(self.platform or "") + "-" + str(self.nodename or "") + "-" + str(self.period or "") + str(self.groupby or "") + str(''.join(self.groups))

    def get_months_between_dates(self, from_date, to_date):
        """ Get months between two dates

            Args:
                from_date (datetime)
                to_date (datetime)
            Returns:
                list
            Raises:
                n/a
        """

        start_month = from_date.month
        end_month = (to_date.year - from_date.year) * 12 + to_date.month + 1
        dates = [datetime(year=yr, month=mn, day=1)
                         for (yr, mn) in (((m - 1) / 12 + from_date.year, (m - 1) % 12 + 1)
                                          for m in range(start_month, end_month))]
        return dates

    def get_dates_between_dates(self, from_date, to_date):
        """ Get dates between two dates

            Args:
                from_date (datetime)
                to_date (datetime)
            Returns:
                list
            Raises:
                n/a
        """

        try:
            from_date = datetime(
                from_date.year, from_date.month, from_date.day)
            to_date = datetime(to_date.year, to_date.month, to_date.day)
            days = (to_date + datetime.timedelta(days=1) - from_date).days
            return [from_date + timedelta(days=n) for n in range(days)]
        except:
            FGUtility.debug(str(sys.exc_info()))

    def create_dates_between_dates(self, from_date, to_date, val=None):
        """ Get dates between two dates

            Args:
                from_date (datetime)
                to_date (datetime)
            Returns:
                dict
            Raises:
                n/a
        """

        try:
            from_date = datetime(
                from_date.year, from_date.month, from_date.day)
            to_date = datetime(to_date.year, to_date.month, to_date.day)
            days = (to_date + timedelta(days=1) - from_date).days
            return {from_date + timedelta(days=n): val for n in range(days)}
        except:
            FGUtility.debug(str(sys.exc_info()))

    def create_months_between_dates(self, from_date, to_date, val=None):
        """ Get months between two dates

            Args:
                from_date (datetime)
                to_date (datetime)
            Returns:
                dict
            Raises:
                n/a
        """

        try:
            months = self.get_months_between_dates(from_date, to_date)
            return {month: val for month in months}
        except:
            FGUtility.debug(str(sys.exc_info()))

    def set_months(self):
        dates = self.get_months_between_dates(self.from_date, self.to_date)
        self.months = dates

    def set_distinct(self, val):
        self.distinct = val

    def get_filter(self, name=None):
        if name and name in self:
            return self.name
        else:
            newval = copy.copy(self)
            del newval.selected
            return newval

    def _is_searching_all(self):
        if not self.from_date and not self.to_date:
            return True
        return False

    def _is_in_date(self, instance):

        if self._is_searching_all():
            return True
        try:
            if (instance["t_start"] > self.to_date) or (instance["t_end"] < self.from_date):
                return False
        except:
            # openstack data doesnt have t_end sometimes.
            # e.g. t_end is None (0000-00-00 00:00:00)
            return False
        # Newly added for exception
        # try:
        #    if instance["trace"]["extant"]["stop"] < self.from_date:
        #        return False
        # except:
        #    pass
        return True

    def _is_filtered(self, instance):
        if self.nodename and self.nodename != instance["hostname"]:
            return False
        if self.platform and self.platform != instance["cloudplatform.platform"]:
            return False
        if self.username and self.username != instance["ownerId"]:
            return False
        if self.project:
            if int(self.project) != instance["ProjectId"]:
                return False
        return True

    def _is_userinfo_needed(self, refresh=False):
        if not refresh:
            return self.userinfo_needed
        if self.groupby in {"project", "institution", "projectleader", "discipline"}:
            return True
        elif self.groups:
            for k in self.groups:
                if k in {"ProjectLead", "ProjectId", "Institution", "Discipline"}:
                    return True
        if self.project:
            # If project is set, userinfo is required.
            return True
        return False

    def set_search_date(self, from_date, to_date):
        self.set_date(from_date, to_date)

    def select(self, instance):
        default = self.get(instance, self.keys_to_select)
        extra = {}
        if self._is_userinfo_needed():
            extra = self.get(instance, self.keys_to_select_extra)
        default.update(extra)

        self.store2cache(instance)  # for later use
        return default

    def select_metric(self, name):
        self.selected_metric = name
        self.set_internal_options([name])

    def get(self, instance, keys):
        return dict((key, instance[key]) for key in keys)

    def get_val(self, _dict, keys):
        return list(_dict[key] for key in keys)

    def get_values(self, _dict, keys):
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

    def get_groups(self):
        ins = self.get_selected_instance()
        return self.get_values(ins, self.groups)

    def get_metric(self):
        return self.stats

    def get_series(self):
        series = []
        try:
            for group, metrics in self.get_metric().iteritems():
                for metric, period in metrics.iteritems():
                    if len(metrics) > 1:
                        series_name = metric
                    else:
                        series_name = group
                    stat = {"name": series_name,
                            "data": period[self.period or self.groupby]}  # period.values()[0] }
                    series.append(stat)
        except:
            print sys.exc_info()
            FGUtility.debug(True)

            # Just try  01/08/2013
            for metric_name in self.metric:  # self.metric is list
                record = {}
                for group, v in self.get_metric().iteritems():
                    val = v[metric_name][
                        self.period or self.groupby or "Total"]
                    record[group] = val

                stat = {"name": metric_name,
                        "data": record}
                series.append(stat)

        return series

    def get_csv(self):
        series = []
        try:
            for group, metrics in self.get_metric().iteritems():
                for metric, period in metrics.iteritems():
                    if len(metrics) > 1:
                        series_name = metric
                    else:
                        series_name = group
                    for k, v in period[self.period or self.groupby].iteritems():
                        series.append([k, v])
        except:

            # Just try  01/08/2013
            for metric_name in self.metric:  # self.metric is list
                for group, v in self.get_metric().iteritems():
                    val = v[metric_name][
                        self.period or self.groupby or "Total"]
                    series.append([group, val])

        # TEMP ADDED FOR SORTING 01/09/2013
        series = sorted(series, key=lambda item: item[1], reverse=True)

        # HEADER ADDED
        header = [[self.groupby or "Total", "Value"]]
        header[0][0] = header[0][0].capitalize()
        series = header + series
        return series

    def collect(self, instance):
        instance = self.select(instance)
        self.get_statistics()
        return True

    def get_statistics(self):
        groups = self.get_groups()
        for metric in self.metric:
            self.select_metric(metric)
            self.update_metric_beta(groups, metric)
            # self.update_metrics(groups, self.stats, metric)

    def _is_unique(self, key, value):
        ''' if value is unique, return itself. Otherwise return None'''
        if not self.distinct:
            return value

        try:
            self.distinct_list[key][value] += 1
            if self.distinct_list[key][value] == 1:
                return value
            return None
        except:
            self.distinct_list[key] = Counter({value: 1})
            return value

    def update_metric_beta(self, groups, metric):
        mdict = self.stats
        for group in groups:
            try:
                mdict = mdict[group]
            except:
                mdict[group] = OrderedDict()
                mdict = mdict[group]

        # Total
        self.calculate_total(mdict, metric)
        # Period
        try:
            period_func = getattr(self, "_divide_into_" + str(self.period))
            period_func(mdict[metric])
            period_func = getattr(self, "_groupby_" + str(self.groupby))
            period_func(mdict[metric])
        except:
            pass

    def update_metrics(self, glist, mdict, key):
        if len(glist) == 0:
            self.calculate_total(mdict, key)
            # Add daily dict temporarily
            try:
                period_func = getattr(self, "_divide_into_" + str(self.period))
                period_func(mdict[key])
            except:
                pass
            try:
                # This _groupby_ shall be removed and merged to groups because it has same functionality with groups... 12/27/2012
                # E.g. set groups ProjectLead
                '''
                {'Yogesh Simmhan': {'count': {'Total': 56}}, 'David Lowenthal': {'count': {'Total': 2}}, 'Morris Riedel': {'count': {'Total': 8}}, 'Hyungro Lee': {'count': {'Total': 2}}, 'Alan Sill': {'count': {'Total': 1}}, 'Gregor von Laszewski': {'count': {'Total': 201}}, 'Shantenu Jha': {'count': {'Total': 14}}, 'Zhan Wang': {'count': {'Total': 24}}, 'Ilkay Altintas': {'count': {'Total': 12}}, 'Shava Smallen': {'count': {'Total': 2}}, 'Preston Smith': {'count': {'Total': 4}}, 'Michael Wilde': {'count': {'Total': 16}}}
                '''
                # e.g. set groupby projectleader
                '''
                {'All': {'count': {'projectleader': {'Yogesh Simmhan': 56, 'David Lowenthal': 2, 'Morris Riedel': 8, 'Hyungro Lee': 2, 'Alan Sill': 1, 'Gregor von Laszewski': 201, 'Shantenu Jha': 14, 'Zhan Wang': 24, 'Ilkay Altintas': 12, 'Shava Smallen': 2, 'Preston Smith': 4, 'Michael Wilde': 16}, 'Total': 342}}}
                '''
                period_func = getattr(self, "_groupby_" + str(self.groupby))
                period_func(mdict[key])
            except:
                pass

            return mdict[key]

        group = glist.pop(0)
        if not group in mdict:
            mdict[group] = {}
        return self.update_metrics(glist, mdict[group], key)

    def calculate_total(self, mdict, key):
        new = self.get_metric_factor(
            self.columns, self.get_selected_instance())
        new = self.do_time_conversion(new)
        total = "Total"
        try:
            old = mdict[key][total]
        except:
            old = None
            mdict[key] = {total: None}
        new = self._is_unique(key + total, new)
        mdict[key][total] = self.calculate(old, new)

    def do_time_conversion(self, val):
        # Temporary lines 12/27/2012
        if set([self.selected_metric]) & (set(self.names.metric.runtime) | set(self.names.metric.runtimeusers)):
            val = (
                val + self.time_conversion // 2) // self.time_conversion  # 864000 seconds = 1440 minutes = 24 hours = 1 day
        return val or 1

    def _groupby_None(self, *args):
        return

    def _groupby_Total(self, *args):
        return self._groupby_None(args)

    def _groupby_walltime(self, mdict):
        val = self.get_metric_factor(
            self.columns, self.get_selected_instance())
        selected = self.get_selected_instance()
        t_delta = self.get_t_delta(selected)

        if not self.groupby in mdict:
            mdict[
                self.groupby] = {"a. <1 min": 0, "b. <30 min": 0, "c. <1 hr": 0,
                                 "d. <3 hr": 0, "e. <12 hr": 0, "f. <1 day": 0, "g. <2 days": 0, "h. more": 0}

        interval = t_delta // 60
        if interval < 1:
            mdict[self.groupby]["a. <1 min"] += val
        elif interval < 30:
            mdict[self.groupby]["b. <30 min"] += val
        elif interval < 60:
            mdict[self.groupby]["c. <1 hr"] += val
        elif interval < 60 * 3:
            mdict[self.groupby]["d. <3 hr"] += val
        elif interval < 60 * 12:
            mdict[self.groupby]["e. <12 hr"] += val
        elif interval < 60 * 24:
            mdict[self.groupby]["f. <1 day"] += val
        elif interval < 60 * 48:
            mdict[self.groupby]["g. <2 days"] += val
        else:
            mdict[self.groupby]["h. more"] += val

    def _groupby_project(self, mdict):
        if not self._is_userinfo_needed():
            return

        selected = self.get_selected_instance()
        val = self.get_metric_factor(self.columns, selected)

        if not self.groupby in mdict:
            mdict[self.groupby] = {}
        project = re.sub("fg-None:None", "Others", "fg-" + str(
            selected["ProjectId"]) + ":" + str(selected["Title"]))
        if not project in mdict[self.groupby]:
            mdict[self.groupby][project] = val
        else:
            mdict[self.groupby][project] += val

    def _groupby_institution(self, mdict):
        if not self._is_userinfo_needed():
            return

        selected = self.get_selected_instance()
        val = self.get_metric_factor(self.columns, selected)
        val = self.do_time_conversion(val)

        if not self.groupby in mdict:
            mdict[self.groupby] = {}
        project = re.sub("None", "Others", str(selected["Institution"]))
        if not project in mdict[self.groupby]:
            mdict[self.groupby][project] = val
        else:
            mdict[self.groupby][project] += val

    def _groupby_projectleader(self, mdict):
        if not self._is_userinfo_needed():
            return

        selected = self.get_selected_instance()
        val = self.get_metric_factor(self.columns, selected)
        val = self.do_time_conversion(val)

        if not self.groupby in mdict:
            mdict[self.groupby] = {}
        project = re.sub("None", "Others", str(selected["ProjectLead"]))
        if not project in mdict[self.groupby]:
            mdict[self.groupby][project] = val
        else:
            mdict[self.groupby][project] += val

    def _groupby_discipline(self, mdict):
        if not self._is_userinfo_needed():
            return

        selected = self.get_selected_instance()
        val = self.get_metric_factor(self.columns, selected)
        val = self.do_time_conversion(val)

        if not self.groupby in mdict:
            mdict[self.groupby] = {}
        project = re.sub("None", "Others", str(selected["Discipline"]))
        if not project in mdict[self.groupby]:
            mdict[self.groupby][project] = val
        else:
            mdict[self.groupby][project] += val

    def get_t_delta(self, row):

        start = row["t_start"]
        last = row['t_end']
        #last = row["date"]

        #if row["state"] == "Teardown":
        #    if row["t_end"]:
        #        last = min(row["date"], row["t_end"])
        # In a previous version, t_end is missing, so we check.
        # If it exists, the earlier datetime should be used because we used to
        # put future time to t_end, i.e. 3000-12-31 11:59:59.

        # We updated this logic and removed the future time to t_end.

        #try:
        #    last = max(row["date"], row["t_end"])
        #except:
        #    pass

        t_delta = (last - start).total_seconds()
        if t_delta < 0:
            t_delta = timedelta(0).total_seconds()
        return t_delta

    '''
    from collections import Counter

    ex)
    res = histogram
    1 = res[0:5]
    2 = res[6:10]

    def histogram(iterable, low, high, bins):
    '''
    '''Count elements from the iterable into evenly spaced bins
        #>>> scores = [82, 85, 90, 91, 70, 87, 45]
        #>>> histogram(scores, 0, 100, 10)
        #[0, 0, 0, 0, 1, 0, 0, 1, 3, 2]
    '''
    '''
        step = (high - low + 0.0) / bins
        dist = Counter((float(x) - low) // step for x in iterable)
        return [dist[b] for b in range(bins)]
    '''

    def _divide_into_None(self, mdict):
        return

    def _divide_into_Total(self, mdict):
        return self._divide_into_None(mdict)

    def _divide_into_daily(self, mdict):
        try:
            mdict[self.period]
        except:
            mdict[self.period] = {}
            first_day = datetime(
                self.from_date.year, self.from_date.month, self.from_date.day)
            for single_date in (first_day + timedelta(days=n) for n in range(self.day_count + 1)):
                mdict[self.period].setdefault(single_date, 0)
        a = mdict[self.period]
        b = self.calculate_daily()
        entries2update = {k: self.calculate(a.get(
            k), b.get(k)) for k in set(a) & set(b)}
        a.update(entries2update)

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

    def _divide_into_monthly(self, mdict):
        try:
            mdict[self.period]
        except:
            mdict[self.period] = {}
            for single_date in self.months:
                mdict[self.period].setdefault(single_date, 0)
        a = mdict[self.period]
        b = self.calculate_monthly()
        entries2update = {k: self.calculate(a.get(
            k), b.get(k)) for k in set(a) & set(b)}
        a.update(entries2update)

    def calculate_monthly(self):
        selected = self.get_selected_instance()
        value = self.get_metric_factor(self.columns, selected)

        months = self.create_months_between_dates(
            selected["t_start"], selected["t_end"], value)
        self.adjust_each_metric_in_month(months, value)
        return months

    def calculate_daily(self):
        selected = self.get_selected_instance()
        value = self.get_metric_factor(self.columns, selected)
        if not value:
            return {}

        # possible metrics
        # 1. runtime
        # 2. count
        # 3. ccvm
        init_value = value
        if set([self.selected_metric]) & (set(self.names.metric.runtime) | set(self.names.metric.runtimeusers)):
            init_value = self.do_time_conversion(
                86400)  # 864000 seconds = 1440 minutes = 24 hours = 1 day

        dates = self.create_dates_between_dates(selected[
                                                "t_start"], selected["t_end"], init_value)
        self.adjust_each_metric_daily(dates, value)
        return dates

    def adjust_each_metric_daily(self, dates, value=None):
        if set([self.selected_metric]) & (set(self.names.metric.runtime) | set(self.names.metric.runtimeusers)):
            selected = self.get_selected_instance()
            t_start = selected["t_start"]
            t_end = selected["t_end"]
            first_day = datetime(t_start.year, t_start.month, t_start.day)
            end_of_first_day = first_day + timedelta(
                seconds=86400)  # datetime.combine(t_start + timedelta(days=1), datetime.strptime("00:00:00", "%H:%M:%S").time())
            end_day = datetime(t_end.year, t_end.month, t_end.day)
                               # datetime.combine(t_end.date(),
                               # datetime.strptime("00:00:00",
                               # "%H:%M:%S").time())
            start_of_end_day = end_day
            if first_day == end_day:
                dates[first_day] = self.do_time_conversion(
                    (t_end - t_start).total_seconds())
            else:
                dates[first_day] = self.do_time_conversion(
                    (end_of_first_day - t_start).total_seconds())
                dates[end_day] = self.do_time_conversion(
                    (t_end - start_of_end_day).total_seconds())
        elif set([self.selected_metric]) & set(self.names.metric.countusers):
            for entry_date, entry_value in dates.iteritems():
                new_value = self._is_unique(
                    self.selected_metric + self.period + str(entry_date), value)
                if new_value is None:
                    dates[entry_date] = new_value

    def adjust_each_metric_in_month(self, dates, value=None):
        if set([self.selected_metric]) & (set(self.names.metric.runtime) | set(self.names.metric.runtimeusers)):
            selected = self.get_selected_instance()
            t_start = selected["t_start"]
            t_end = selected["t_end"]
            first_month = datetime(t_start.year, t_start.month, 1)
            end_of_first_month = datetime(t_start.year, t_start.month, monthrange(
                t_start.year, t_start.month)[1], 23, 59, 59)
            end_month = datetime(
                t_end.year, t_end.month, 1)  # datetime.combine(t_end.date(), datetime.strptime("00:00:00", "%H:%M:%S").time())
            start_of_end_month = end_month
            for month_key, month_value in dates.iteritems():
                days = monthrange(month_key.year, month_key.month)[1]
                dates[month_key] = self.do_time_conversion(86400 * days)
            if first_month == end_month:
                dates[first_month] = self.do_time_conversion(
                    (t_end - t_start).total_seconds())
            else:
                dates[first_month] = self.do_time_conversion(
                    (end_of_first_month - t_start).total_seconds())
                dates[end_month] = self.do_time_conversion(
                    (t_end - start_of_end_month).total_seconds())
        elif set([self.selected_metric]) & set(self.names.metric.countusers):
            for entry_date, entry_value in dates.iteritems():
                new_value = self._is_unique(
                    self.selected_metric + self.period + str(entry_date), value)
                if new_value is None:
                    dates[entry_date] = new_value

    def adjust_stats_keys(self, key=None):
        if set(self.groups) & set(["serviceTag"]):
            if key:
                new_key = self.get_clustername(key)
                return new_key
                # self.stats[new_key] = self.stats.pop(key)
            else:
                for key, val in self.stats.iteritems():
                    new_key = self.get_clustername(key)
                    self.stats[new_key] = self.stats.pop(key)

    def get_clustername(self, name):
        try:
            m = re.search(
                r'http://(.*):8775/axis2/services/EucalyptusNC', name, re.M | re.I)
            return m.group(1)
        except:
            return name

    def set_internal_options(self, metric):
        '''Set default values for internal calculation and statistics

            Args:
                metric (list): metric selected
        '''
        if set(metric) & set(self.names.metric.count):
            self.calc = "count"
            self.columns = None
            self.set_distinct(False)
            # "count(*)"
        elif set(metric) & set(self.names.metric.countusers):
            self.calc = "count"
            self.columns = ["ownerId"]
            self.set_distinct(True)
            # "count(distinct ownerId)"
        elif set(metric) & set(self.names.metric.runtime):
            self.calc = "sum"
            self.columns = ["duration"]
            self.set_distinct(False)
        elif set(metric) & set(self.names.metric.runtimeusers):
            self.calc = "sum"
            self.columns = ["duration"]
            self.groups = ["ownerId"]
            # "sum(duration)"
            # group by ownerId
        elif set(metric) & set(self.names.metric.cores):
            self.calc = "sum"
            self.columns = ["ccvm", "cores"]
            self.groups = ["instance.cloudPlatformIdRef"]
            # self.period = "daily"
            # "sum(ccvm_cores)"
            # group by instance.cloudPlatformIdRef, CAST(date as date)
        elif set(metric) & set(self.names.metric.memories):
            self.calc = "sum"
            self.columns = ["ccvm", "mem"]
            self.groups = ["instance.cloudPlatformIdRef"]
            # self.period = "daily"
            # "sum(ccvm_mem)"
            # group by instance.cloudPlatformIdRef, CAST(date as date)
        elif set(metric) & set(self.names.metric.disks):
            self.calc = "sum"
            self.columns = ["ccvm", "disk"]
            self.groups = ["instance.cloudPlatformIdRef"]
            # self.period = "daily"
            # "sum(ccvm_disk)"
            # group by instance.cloudPlatformIdRef, CAST(date as date)

    # Recursion is too expensive in Python. Need to be replaced to a iteration.
    def get_metric_factor(self, columns, selected):
        if columns is None:
            return 1
        elif len(columns) == 0:
            return selected

        return self.get_metric_factor(columns[1:], selected[columns[0]])

    def calculate(self, old, new):
        if self.calc == self.names.calc.count:
            if new:
                return (old or 0) + 1
            return (old or 0)
        elif self.calc == self.names.calc.summation:
            return (old or 0) + (new or 0)
        elif self.calc == self.names.calc.average:
            return ((old or 0) + (new or 0)) / 2
        elif self.calc == self.names.calc.minimum:
            try:
                return min(old or new, new)
            except:
                return 0
        elif self.calc == self.names.calc.maximum:
            try:
                return max(old or new, new)
            except:
                return 0

    def store2cache(self, selected):
        if self.cache:
            self.selected.append(selected)
        else:
            self.selected = [selected]

    def get_selected_instance(self):
        try:
            return self.selected[-1]
        except:
            return

    def get_node_names(self):
        return str(self.nodename or self.all_nodenames)

    def get_platform_names(self):
        return str(self.platform or self.all_platforms)

    def show_None(self, param=None):
        self.show_filter()

    def show_filter(self):
        pprint(vars(self.get_filter()))

    def clear(self):
        self.__init__()
