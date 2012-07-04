from datetime import *

import futuregrid.cloud.metric.FGNovaDB

class NovaMetric:

    def __init__(self):
        self.instances = []
        self.userinfo = []
        self.users = {}
        self.nodename = None
        self.novadb = futuregrid.cloud.metric.FGNovaDB.NovaDB("futuregrid.cfg")

        self.from_date = None
        self.to_date = None

    def read_from_db(self):

        instance_list = self.novadb.read_instances()

        for element in instance_list:
            self.instances.append(element)

        userinfo_list = self.novadb.read_userinfo()

        for element in userinfo_list:
            self.userinfo.append(element)

    def calculate_stats(self, from_date, to_date):
        """Calculate user-based statstics about VM instances per user: 
        
        Args:
            from_date (str): date to start calculation. Types are 'all' or '%Y-%m-%dT%H:%M:%S'
            to_date (str): end date to finish calculation.
        Returns:
            n/a
        Raises:
            n/a

        """

        date_from = datetime.strptime(from_date, '%Y-%m-%dT%H:%M:%S')
        date_to   = datetime.strptime(to_date, '%Y-%m-%dT%H:%M:%S')

        self.from_date = date_from
        self.to_date = date_to

        for instance in self.instances:

            start_time = self.get_start_time(instance)
            end_time = self.get_end_time(instance)

            nodename = instance['availability_zone']
            userid = instance['user_id']

            t_delta = self.get_t_delta(instance)
            
            if start_time < date_from or start_time > date_to:
                continue
            
            # If a nodename is set, stats is only for the compute cluster node specified
            if self.nodename and self.nodename != nodename:
                continue

            if userid in self.users:
                self.users[userid]['count'] += 1
                self.users[userid]['sum'] += t_delta  # sum of time 
                self.users[userid]['min'] = min (t_delta, self.users[userid]['min'])
                self.users[userid]['max'] = max (t_delta, self.users[userid]['max'])
                self.users[userid]['avg'] = self.users[userid]['sum'] / float(self.users[userid]['count'])
            else:
                self.users[userid] = {'count' : 1,
                                    'sum' : 0,
                                    'min' : t_delta,
                                    'max' : t_delta,
                                    'avg' : 0.0
                                    }

    def get_start_time(self, instance):

        if instance['launched_at']:
            start_time = instance['launched_at']
        else:
            start_time = instance['created_at'] # or 'scheduled_at' ?
        return start_time

    def get_end_time(self, instance):

        if instance['terminated_at']:
            end_time = instance['terminated_at']
        elif instance['deleted_at']:
            end_time = instance['deleted_at']
        elif instance['updated_at']:
            end_time = instance['updated_at']
        else:
            end_time = self.to_date
        return end_time

    def get_t_delta(self, instance):

        t_delta = (self.get_end_time(instance) - self.get_start_time(instance)).seconds
        return t_delta
