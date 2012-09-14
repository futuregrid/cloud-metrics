from datetime import *

class FGSearch:

    name = None
    from_date = None
    to_date = None
    day_count = None
    period = None
    stat = {}
    metric = {}
    groupby = None

    project = None
    nodename = None
    platform = None
    userid = None
    username = None

    operation = None # count, avg, min, max, sum

    result = None

    def __init__(self):
        self.name = None
        self.keys_to_select = { 't_start', 't_end', 'duration' }

    def set_metric(self, name):
        self.name = name

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

    def set_date(self, from_date, to_date):
        """Set search/analyze period

            Args:
                from_date (str): first date of calculation. '%Y-%m-%dT%H:%M:%S' is only allowed.
                to_date (str): end date of calculation.
            Returns:
                n/a
            Raises:
                n/a

        """

        print from_date
        print to_date
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

    def _is_filtered(self, instance):
        if self.username and self.username != instance["ownerId"]:
            return False
        if self.nodename and self.nodename != instance["hostname"]:
            return False
        if self.platform and self.platform != instance["platform"]:
            return False
        return True

    def set_search_date(self, from_date, to_date):
        self.set_date(from_date, to_date)

    def retrieve(self, instance):
        self.get(instance, self.keys_to_select)

    def get(self, instance, keys):
        self.result = dict((key, instance[key]) for key in keys)
        return self.result
