import datetime

class FGExampleGenerator:

    def initialize(self):
        #self.get_conf()
        self.get_start_date()
        self.get_end_date()
        #self.get_options()
        self.get_period() # weekly, daily, monthly, quarterly
        self.get_platforms() # openstack, eucalyptus, nimbus
        self.get_hosts() # india, sierra, hotel, alamo, foxtrot
        self.load_template()

    def set_date(self):
        start_date = datetime.date(2011, 11, 01)
        start_date_for_weekly = start_date
        t_end_date = datetime.date.today()
        week = datetime.timedelta(weeks=1)

    def open_template(self):
        template_file = ".template"
        f = open(template_file, "r")
        f_txt = f.read()
        f.close()

    def generate_examples(self):
        while (1):
            if start_date > t_end_date:
                break

            end_date = start_date + datetime.timedelta(days=6)
            replaced_txt = f_txt % vars()
            f2 = open(str(start_date) + ".txt", "w")
            f2.write(replaced_txt)
            f2.close
            start_date = start_date + week
            if (start_date_for_weekly + (10 * week)) == start_date:
                start_date_for_weekly = start_date_for_weekly + week

if __name__ == "__main__":
    examples = FGExampleGenerator()
    examples.initialize()
    examples.generate_examples()
