from datetime import *

class FGStats:

    def __init__(self):
        self.name = None
        self.from_date = None
        self.to_date = None
        self.day_count = None
        self.period = None
        self.stat = {}
        self.metric = {}
        self.groupby = None

        self.project = None
        self.nodename = None
        self.platform = None
        self.userid = None

        self.operation = None # count, avg, min, max, sum

    def set_metric(self, name):
        self.name = name

    def set_period(self, name):
        self.period = name

    def set_search_date(self, from_date, to_date):
        """Set search/analyze period

            Args:
                from_date (str): first date of calculation. '%Y-%m-%dT%H:%M:%S' is only allowed.
                to_date (str): end date of calculation.
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

    def get_stats_from_istances(self, instances):

        for i in range(0, instances.count()):
            instance = instances.getdata(i)

            if not ((instance['ts'] >= self.from_date) and (instance['ts'] < self.to_date)):
                continue

            if not self._filter(instance):
                continue

            self._calculate_vm_count_and_runtime(instance)
        
    def _filter(self, ins):
        if self.project and ins['accountId'] != self.project:
            return False
        if self.nodename and ins['euca_hostname'] != self.nodename:
            return False
        #if self.platform and 
        #    return False
        if self.userid and ins['ownerId'] != self.userid:
            return False
        
        return True

    def _calculate_vm_count_and_runtime(self, ins):

        if self.name != ( "vm_count" or "vm_runtime" ):
            return

        groupname = self.groupby
        grouped = ins[groupname]
        #TEMPORARY fixed variables
        ownerid = ins['ownerId']
        groupname = "ownerId"
        grouped = ins[groupname]
        t_delta = float(ins['duration'])
        if self.stat[grouped]:
            self.stat[grouped]['count'] += 1
            self.stat[grouped]['runtime'] += t_delta
            self.stat[grouped]['max'] = max(t_delta, self.stat[grouped]['max'])
            self.stat[grouped]['min'] = min(t_delta, self.stat[grouped]['min'])
            self.stat[grouped]['avg'] = self.stat[grouped]['runtime'] / self.stat[grouped]['count']
        else:
            self.stat[grouped] = { groupname : grouped,
                    'count' : 1,
                    'runtime' : t_delta,
                    'max' : t_delta,
                    'min' : t_delta,
                    'avg' : t_delta }

    def create_new_metric(self, name):
        self.metric[name] = FGStats()

