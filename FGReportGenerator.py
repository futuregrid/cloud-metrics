from datetime import date, datetime, timedelta
from argparse import ArgumentParser
import sys

class FGReportGenerator:
    def __init__(self):
        self.cmd_ext = ".txt"
        self.rst_ext = ".rst"
        self.init_vars()
        self.init_template_vars()

    def init_vars(self):
        self.hostnames = []
        self.services = []
        self.args = None
        self.index_rst = "index.rst"
        self.reports_directory = "reports"
        self.template_directory = "examples/"
        self.cmd_directory = self.reports_directory + "/cmd/"
        self.rst_directory = self.reports_directory + "/rst/"

    def init_template_vars(self):
        self.hostname = ""
        self.service = ""
        self.from_date = ""
        self.to_date = ""
        self.from_dateT = ""
        self.to_dateT = ""
        self.output_directory = "output/" # + from and to date

    def get_parameter(self):
        parser = ArgumentParser()
        parser.add_argument('-n', '--hostname', dest='hostnames', default=[], nargs='*', help="hostname (e.g. india, sierra, alamo, foxtrot, hotel, etc..)")
        parser.add_argument('-s', '--service', dest='services', default=[], nargs='*', help="cloud service (e.g. eucalyptus, openstack, nimbus, openebula, etc..)")
        parser.add_argument('-t', '--template', required=True, help="template name to use (e.g. xsede reads xsede.rst xsede.txt)")
        parser.add_argument('--from', dest="from_date", help="from date (YYYYMMDDThh:mm:ss)")
        parser.add_argument('--to', dest="to_date", help="to date (YYYYMMDDThh:mm:ss")
        args = parser.parse_args()
        self.args = args
        self.hostnames = args.hostnames
        self.services = args.services
        self.template = args.template
        try:
            from_date = datetime.strptime(args.from_date, '%Y%m%dT%H:%M:%S')
            to_date = datetime.strptime(args.to_date, '%Y%m%dT%H:%M:%S')
        except:
            today = date.today()
            sixmonthsago = today - timedelta(days=181)
            from_date = datetime(sixmonthsago.year, sixmonthsago.month, sixmonthsago.day, 0, 0, 0)
            to_date = datetime(today.year, today.month, today.day, 0, 0, 0)

        self.from_dateT = from_date.strftime('%Y-%m-%dT%H:%M:%S')
        self.to_dateT = to_date.strftime('%Y-%m-%dT%H:%M:%S')
        self.from_date = str(from_date)
        self.to_date = str(to_date)

        #self.hostname = ", ".join(self.hostnames)
        #self.service = ", ".join(self.services)

    def read_template(self):
        self.raw_cmd_txt = self.read_file(self.template_directory + self.template + self.cmd_ext)
        self.raw_rst_txt = self.read_file(self.template_directory + self.template + self.rst_ext)
        self.raw_cmd_txt = "\r\n".join(self.raw_cmd_txt)
        self.raw_rst_txt = "\r\n".join(self.raw_rst_txt)

    def read_file(self, filename):
        with open(filename) as f:
            lines = f.read().splitlines()
            return lines

    def write_file(self, filepath, msg):
        # Write mode creates a new file or overwrites the existing content of the file. 
        # Write mode will _always_ destroy the existing contents of a file.
        try:
            # This will create a new file or **overwrite an existing file**.
            f = open(filepath, "w")
            try:
                if isinstance(msg, list):
                    msg = '\r\n'.join(msg)
                f.write(msg) # Write a string to a file
            finally:
                f.close()
        except IOError:
            pass

    def generate_cmd_text(self):
        self.cmd_txt = self.replace_vars("cmd")

    def generate_rst_text(self):
        self.rst_txt = self.replace_vars("rst")

    def replace_vars(self,name):
        var = getattr(self, "raw_" + str(name) + "_txt")
        res = {}
        for host in self.hostnames or ["All"]:
            for serv in self.services or ["All"]:
                self.adjust_names("hostname", host)
                self.adjust_names("service", serv)
                res[host] = { serv : var % vars(self) }
        return res

    def update_index_rst(self):
        today = date.today().strftime("%a, %d %b %Y")
        list_of_rst = "\r\n".join(self.get_list_of_rst())
        msg = ["FG Usage Report", \
                "===============", \
                "Date Created: ",\
                today, \
                " ", \
                ".. toctree::", \
                "\t:maxdepth: 2", \
                " ", \
                list_of_rst ]
        msg = "\r\n".join(msg)

        self.write_file(self.index_rst, msg)

    def get_list_of_rst(self):
        res = []
        for host in self.hostnames:
            for serv in self.services:
                res.append("\t" + self.rst_directory + host + "-" + serv)
        return res

    def write_cmd_text(self):
        for host, service in self.cmd_txt.iteritems():
            for serv, msg in service.iteritems():
                filename = host + "-" + serv + self.cmd_ext
                self.write_file(self.cmd_directory + filename, msg)

    def write_rst_text(self):
        for host, service in self.rst_txt.iteritems():
            for serv, msg in service.iteritems():
                filename = host + "-" + serv + self.rst_ext
                self.write_file(self.rst_directory + filename, msg)

    def adjust_names(self, name, val):
        if val != "All":
            setattr(self, name, val)

if __name__ == "__main__":
    report = FGReportGenerator()
    report.get_parameter()
    report.read_template()
    report.generate_cmd_text()
    report.generate_rst_text()
    report.write_cmd_text()
    report.write_rst_text()
    report.update_index_rst()
