import futuregrid.cloud.metric.FGNovaDB

class NovaMetric:

    def __init__(self):
        self.instances = []
        self.novadb = futuregrid.cloud.metric.FGNovaDB.NovaDB("futuregrid.cfg")

    def read_from_db(self):

        instance_list = self.novadb.read_instances()

        for element in instance_list:
            self.instances.append(element)

    def calculate_stats(self, from_date, to_date):
        print from_date
        print to_date
        print self.instances[0]

