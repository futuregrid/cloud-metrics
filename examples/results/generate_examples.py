from datetime import datetime, timedelta
import ConfigParser
from pprint import pprint

class FGExampleGenerator:

    template = {}
    template_path = ".template/"

    output_path = "output/"

    def get_conf(self):
        config = ConfigParser.ConfigParser()
        config.read(".conf")
        section = "FGReports"

        try:
            self.start_date = config.get(section, "start_date")
            self.end_date = config.get(section, "end_date")
            self.platforms = config.get(section, "platform")
            self.hostnames = config.get(section, "hostname")
            self.periods = config.get(section, "period")
            self.metrics = config.get(section, "metric")
        except ConfigParser.NoSectionError as e:
            print sys.exc_info()
            raise

        self.platforms = self.strips(self.platforms)
        self.hostnames = self.strips(self.hostnames)
        self.periods = self.strips(self.periods)
        self.metrics = self.strips(self.metrics)
        self.start_date = datetime.strptime(self.start_date, "%Y-%m-%dT%H:%M:%S")
        if not self.end_date:
            self.end_date = datetime.today()
        else:
            self.end_date = datetime.strptime(self.end_date, "%Y-%m-%dT%H:%M:%S")

    def strips(self, val):
        return [a.strip() for a in val.split(",")]

    def initialize(self):
        self.get_conf()
        #self.get_start_date()
        #self.get_end_date()
        #self.get_options()
        #self.get_period() # weekly, daily, monthly, quarterly
        #self.get_platforms() # openstack, eucalyptus, nimbus
        #self.get_hosts() # india, sierra, hotel, alamo, foxtrot
        self.load_template()

    def load_template(self):
        for metric in self.metrics:
            filename = self.template_path + str(metric) + ".template"
            self.template[metric] = self.read_file(filename)

    def read_file(self, filename):
        f = open(filename, "r")
        f_txt = f.read()
        f.close()
        return f_txt

    def generate_examples(self):
        accumulated = ""
        for metric in self.metrics:
            for hostname in self.hostnames:
                for platform in self.platforms:
                    for period in self.periods:
                        single_date = self.start_date
                        while (single_date < self.end_date):
                            accumulated += self.get_text(hostname, platform, period, metric, single_date)
                            single_date += self.get_timegap(period)
                        self.write_file(hostname, platform, period, metric, accumulated)
                        accumulated = ""

    def get_timegap(self, period):
        if period == "weekly":
            return timedelta(weeks=1)
        elif period == "monthly":
            return timedelta(days=31)
        elif period == "quarterly":
            return timedelta(days=91)
        elif period == "daily":
            return timedelta(days=1)

    def get_text(self, hostname, platform, period, metric, s_date):
        local = { "metric":metric,
                "hostname":hostname,
                "platform":platform,
                "period":period,
                "year":s_date.year,
                "month":str(s_date.month).zfill(2),
                }
        print vars()
        replaced_txt = self.template[metric] % vars()["local"]
        print vars()["local"]
        print replaced_txt
        return replaced_txt

    def write_file(self, hostname, platform, period, metric, replaced_txt):
        filename = self.output_path + str(metric) + "_" + str(hostname) + "_" + str(platform) + "_" + str(period) + ".txt"
        f = open(filename, "w")
        f.write(replaced_txt)
        f.close

    def show_variable(self):
        pprint(vars(self))

if __name__ == "__main__":
    examples = FGExampleGenerator()
    examples.initialize()
    examples.show_variable()
    examples.generate_examples()
