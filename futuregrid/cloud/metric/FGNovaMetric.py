from datetime import *

import futuregrid.cloud.metric.FGNovaDB

class NovaMetric:

    def __init__(self):
        self.instances = []
        self.userinfo = []
        self.users = {}
        self.novadb = futuregrid.cloud.metric.FGNovaDB.NovaDB("futuregrid.cfg")

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

        for instance in self.instances:

            start_time = datetime.strptime(instance['launched_at'], '%Y-%m-%d %H:%M:%S')
            end_time = datetime.strptime(instance['terminated_at'], '%Y-%m-%d %H:%M:%S')
            nodename = instance['availability_zone']
            userid = instance['id']
            t_delta = float(end_time - start_time)
            
            if start_time < date_from or start_tim > date_to:
                continue
            
            # If a nodename is set, stats is only for the compute cluster node specified
            if self.nodename and self.nodename != nodename:
                continue

            if userid in self.users:
                self.users[userid]['count'] += 1
                self.users[userid]['sum'] += t_delta  # sum of time 
                self.users[userid]['min'] = min (t_delta, self.users[userid]['min'])
                self.users[userid]['max'] = max (t_delta, self.users[userid]['max'])
                self.users[userid]['avg'] = self.users[userid]['sum'] / self.users[name]['count']
            else:
                self.users[userid] = {'count' : 1,
                                    'sum' : 0.0,
                                    'min' : t_delta,
                                    'max' : t_delta,
                                    'avg' : 0.0
                                    }

