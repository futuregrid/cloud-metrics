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
        self.header = ".header"
        self.main = ".main"
        self.footer = ".footer"

    def init_template_vars(self):
        self.hostname = ""
        self.service = ""
        self.from_date = ""
        self.to_date = ""
        self.from_dateT = ""
        self.to_dateT = ""
        self.output_directory = "output/" # + from and to date

        self.all_services = "eucalyptus, openstack, nimbus"
        self.all_hostnames = "sierra, india, hotel, alamo, foxtrot, p434fall13"
        self.service_name = ""
        self.host_name = ""

        # Services per host
        self.resources = { "india": { "eucalyptus", "openstack" }, \
                            "sierra": { "eucalyptus", "openstack", "nimbus" }, \
                            "alamo": { "nimbus", "openstack" }, \
                            "foxtrot": { "nimbus" }, \
                            "hotel": { "nimbus" }, \
                          "p434fall13": { "openstack" }}

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
        self.template_header = self.template + self.header
        self.template_main = self.template + self.main
        self.template_footer = self.template + self.footer

        try:
            from_date = datetime.strptime(args.from_date, '%Y%m%dT%H:%M:%S')
            to_date = datetime.strptime(args.to_date, '%Y%m%dT%H:%M:%S')
        except:
            today = date.today()
            sixmonthsago = today - timedelta(days=181)
            from_date = datetime(sixmonthsago.year, sixmonthsago.month, sixmonthsago.day, 0, 0, 0)
            to_date = datetime(today.year, today.month, today.day, 0, 0, 0)

        self.from_date = str(from_date)
        self.to_date = str(to_date)

        #self.hostname = ", ".join(self.hostnames)
        #self.service = ", ".join(self.services)

    def read_template(self):
        self.raw_cmd_txt = self.read_file(self.template_directory + self.template + self.cmd_ext)
        self.raw_cmd_txt = "\r\n".join(self.raw_cmd_txt)
        self.raw_cmd_singlerun_txt = self.read_file(self.template_directory + self.template + self.header  + self.cmd_ext)
        self.raw_cmd_singlerun_txt = "\r\n".join(self.raw_cmd_singlerun_txt)

        self.raw_rst_txt = self.read_file(self.template_directory + self.template_main + self.rst_ext)
        self.raw_rst_txt = "\r\n".join(self.raw_rst_txt)
        self.raw_rst_header_txt = self.read_file(self.template_directory + self.template_header + self.rst_ext)
        self.raw_rst_header_txt = "\r\n".join(self.raw_rst_header_txt)
        self.raw_rst_footer_txt = self.read_file(self.template_directory + self.template_footer + self.rst_ext)
        self.raw_rst_footer_txt = "\r\n".join(self.raw_rst_footer_txt)

    def read_file(self, filename):
        with open(filename) as f:
            lines = f.read().splitlines()
            return lines

    def write_file(self, filepath, msg, mode="w"):
        # Write mode creates a new file or overwrites the existing content of the file. 
        # Write mode will _always_ destroy the existing contents of a file.
        try:
            # This will create a new file or **overwrite an existing file**.
            f = open(filepath, mode)
            try:
                if isinstance(msg, list):
                    msg = '\r\n'.join(msg)
                f.write(msg) # Write a string to a file
            finally:
                f.close()
        except IOError:
            pass

    def generate_cmd_text(self):
        self.set_vars_for_template()
        self._generate_cmd_per_service_n_hostname()
        self._generate_cmd_singlerun()

    def _generate_cmd_per_service_n_hostname(self):
        self.cmd_txt = self.replace_vars("cmd")

    def _generate_cmd_singlerun(self):
        self.cmd_singlerun_txt = self.raw_cmd_singlerun_txt % vars(self)

    def generate_rst_text(self):
        self.set_vars_for_template()
        self._generate_rst_per_service_n_hostname()
        self._generate_rst_header_n_footer()

    def _generate_rst_per_service_n_hostname(self):
        self.rst_txt = self.replace_vars("rst")

    def _generate_rst_header_n_footer(self):
        self.rst_header_txt = self.raw_rst_header_txt % vars(self)
        self.rst_footer_txt = self.raw_rst_footer_txt % vars(self)

    def replace_vars(self,name):
        var = getattr(self, "raw_" + str(name) + "_txt")
        res = {}
        for host in self.hostnames or ["All"]:
            for serv in self.services or ["All"]:
            #for serv in self.services or self.resources[host]:
                self.adjust_names("hostname", host)
                self.adjust_names("service", serv)
                try:
                    self.adjust_names("service_name", ", ".join(self.resources[host]))
                except:
                    self.adjust_names("service_name", self.all_services)


                try:
                    res[host][serv] = var % vars(self)
                except:
                    res[host] = { serv : var % vars(self) }
        return res

    def is_real(self, hostname, service):
        """Return True/False if service does not exist in the hostname"""
        try:
            if service in self.resources[hostname]:
                return True
            else:
                return False
        except:
            return False
                
    def start_with_header_index_rst(self):
        today = date.today().strftime("%a, %d %b %Y")
        msg = ["FG Usage Report", \
                "===============", \
                "Date Created: ",\
                today, \
                " ", \
                ".. toctree::", \
                "\t:maxdepth: 2", \
                " \r\n"]
        self.write_file(self.index_rst, msg)

    def append_header_rst(self):
        msg = self.rst_directory + self.header[1:]
        self.append_lines_index_rst(msg)

    def append_main_rst(self):
        list_of_rst = "\r\n\t".join(self.get_list_of_rst())
        msg = [ list_of_rst ]
        msg = "".join(msg)
        self.append_lines_index_rst(msg)

    def append_footer_rst(self):
        msg = self.rst_directory + self.footer[1:]
        self.append_lines_index_rst(msg)

    def get_list_of_rst(self):
        res = []
        for host in self.hostnames:
            for serv in self.services or ["All"]:
                res.append(self.rst_directory + host + "-" + serv)
        return res

    def write_cmd_text(self):
        for host, service in self.cmd_txt.iteritems():
            for serv, msg in service.iteritems():
                filename = host + "-" + serv + self.cmd_ext
                self.write_file(self.cmd_directory + filename, msg)

        self._write_cmd_singlerun_text()

    def _write_cmd_singlerun_text(self):
        self.write_file(self.cmd_directory + self.header[1:] + self.cmd_ext, self.cmd_singlerun_txt)

    def write_rst_text(self):
        for host, service in self.rst_txt.iteritems():
            for serv, msg in service.iteritems():
                filename = host + "-" + serv + self.rst_ext
                self.write_file(self.rst_directory + filename, msg)

        self._write_rst_header_n_footer_text()

    def _write_rst_header_n_footer_text(self):
        self.write_file(self.rst_directory + self.header[1:] + self.rst_ext, self.rst_header_txt)
        self.write_file(self.rst_directory + self.footer[1:] + self.rst_ext, self.rst_footer_txt)

    def adjust_names(self, name, val):
        if val != "All":
            setattr(self, name, val)

    def set_vars_for_template(self):
        """Prepare template variables to be replaced in a right format

        Description:
            Template variables are named with 'tmpl_' prefix. For example,
            a variable for period would be 'tmpl_period'
        """
        
        # for better readable date format, convert current date to ...
        from_date = datetime.strptime(self.from_date, '%Y-%m-%d %H:%M:%S')
        to_date = datetime.strptime(self.to_date, '%Y-%m-%d %H:%M:%S')
        self.from_dateT = from_date.strftime('%Y-%m-%dT%H:%M:%S')
        self.to_dateT = to_date.strftime('%Y-%m-%dT%H:%M:%S')

        #tmpl_period
        dfrom = from_date.strftime('%B %d')
        dto = to_date.strftime('%B %d, %Y')
        self.tmpl_period = dfrom + " -- " + dto

        self.host_name = self.hostname
        self.service_name = self.service

        if not len(self.hostnames):
            self.host_name = self.all_hostnames

        if not len(self.services):
            self.service_name = self.all_services

    def append_lines_index_rst(self, msg):
        self.write_file(self.index_rst, "\t" + msg + "\r\n", "a")

    def write_index_rst(self):
        self.start_with_header_index_rst()
        self.append_header_rst()
        self.append_main_rst()
        self.append_footer_rst()

if __name__ == "__main__":
    report = FGReportGenerator()
    report.get_parameter()
    report.read_template()
    report.generate_cmd_text()
    report.generate_rst_text()
    report.write_cmd_text()
    report.write_rst_text()
    report.write_index_rst()
