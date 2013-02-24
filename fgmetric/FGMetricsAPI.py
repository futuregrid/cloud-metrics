from fgmetric.FGDatabase import FGDatabase
from fgmetric.FGSearch import FGSearch

class FGMetricsAPI:

    def __init__(self):
        self.init_db()

    def init_db(self):
        self.db = FGDatabase()
        self.db.conf()
        self.db.connect()

    def set_date(self, s_date, e_date):
        self.start_date = s_date
        self.end_date = e_date

    def set_metric(self, name):
        self.metric = name

    def set_user(self, name):
        self.username = name

    def set_cloud(self, name):
        self.cloud = name

    def set_hostname(self, name):
        self.hostname = name

    def get_metric(self):
        # TBD
        return

    def get_cloud(self):
        # TBD
        return

    def set_period(self, name):
        self.period = name

    def get_period(self):
        # TBD
        return

    def get_stats(self):
        userinfo = self.db.read_userinfo({"username":self.username})
        ownerids = [element['ownerid'] for element in userinfo]
        #print ownerids 
        res = []
        for ownerid in ownerids:
            instances = self.db.read_instance({"ownerid":ownerid}) # querydict doesn't cover >= and <=. it only covers strings at this time. {"t_start":self.start_date})
            print instances
            res.append(instances)

        print res


