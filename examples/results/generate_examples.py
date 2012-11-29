from datetime import datetime, timedelta
import ConfigParser
from pprint import pprint
import calendar

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
                        s_date = self.start_date
                        while (s_date < self.end_date):
                            e_date = self.get_nextdate(s_date, period)
                            accumulated += self.get_text(hostname, platform, period, metric, s_date, e_date)
                            s_date = e_date
                        self.write_file(hostname, platform, period, metric, accumulated)
                        accumulated = ""

    def get_nextdate(self, s_date, period):
        if period == "weekly":
            return (s_date + timedelta(weeks=1)).replace(hour=0,minute=0,second=0)
        elif period == "monthly":
            try:
                day = calendar.monthrange(s_date.year, s_date.month)[1] - s_date.day + 1
            except:
                day = 31
            return (s_date + timedelta(days=day)).replace(hour=0,minute=0,second=0)
        elif period == "quarterly":
            return self.get_firstday_of_nextquarter(s_date)
        elif period == "daily":
            return timedelta(days=1).replace(hour=0,minute=0,second=0)

    def get_firstday_of_nextquarter(self, s_date):
        current_q = (s_date.month - 1) // 3 + 1
        year = s_date.year
        if current_q == 1:
            month = 4
        elif current_q == 2:
            month = 7
        elif current_q == 3:
            month = 10
        elif current_q == 4:
            month = 1
            year = s_date.year + 1
        return s_date.replace(year=year, month=month, day=1,hour=0,minute=0,second=0)

    def get_text(self, hostname, platform, period, metric, s_date, e_date):
        local = { "metric":metric,
                "hostname":hostname,
                "platform":platform,
                "period":period,
                "year":s_date.year,
                "month":str(s_date.month).zfill(2),
                "start_date":s_date.strftime("%Y-%m-%dT%H:%M:%S"),
                "end_date":e_date.strftime("%Y-%m-%dT%H:%M:%S"),
                "path":self.get_output_path(period, s_date)
                }
        replaced_txt = self.template[metric] % vars()["local"]
        return replaced_txt

    def get_output_path(self, period, s_date):
        if period == "quarterly":
            return str(s_date.year) + "-Q" + str((s_date.month - 1) // 3 + 1)
        else:
            return str(s_date.year) + "-" + str(s_date.month).zfill(2)
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
