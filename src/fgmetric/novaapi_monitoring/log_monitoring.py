import logging
from mongolog.handlers import MongoHandler
from fgmetric.shell.FGConfig import FGConfig
from docopt import docopt
import re
import time

class log_monitoring:

    # cloud service name + hostname
    name = "nova-api.india" 

    def __init__(self):
        self.get_dbinfo()
        self.open_handler()

    def get_dbinfo(self):
        #access info
        fgconfig = FGConfig()
        self.dbinfo = fgconfig.get_config("CloudMetricsMongoDB")

    def open_handler(self):
        # set logging
        self.log = logging.getLogger(self.name)
        self.log.addHandler(MongoHandler.to(db=self.dbinfo["db"], 
            collection='log', host=self.dbinfo["host"], 
            port=self.dbinfo["port"], username=self.dbinfo["user"],
            password=self.dbinfo["passwd"]))

    def get_docopt(self):
        """Log Monitoring
        
        Usage:
          log_monitoring [-hvf NAME]

        Options:
          -h --help             Show this help message and exit
          --version             Show version and exit
          -f NAME --file=NAME   Parse the file
        """
        doc = self.get_docopt.__doc__
        self.args = docopt(doc)

    def read_file(self):
        try:
            filename = self.args["--file"]
            f = open(filename, 'r')
            while True:
                line = ''
                while len(line) == 0 or line[-1] != '\n':
                    tail = f.readline()
                    if tail == '':
                        time.sleep(0.1)          # avoid busy waiting
                        # f.seek(0, io.SEEK_CUR) # appears to be unneccessary
                        continue
                    line += tail
                self.parse_log(line)
        except:
            return

    def parse_log(self, line):
        try:
            re.compile

    def _test(self):
        self.log.setLevel(logging.DEBUG)
        self.log.debug("1 - debug message")
        self.log.info("2 - info message")
        self.log.warn("3 - warn message")
        self.log.error("4 - error message")
        self.log.critical("5 - critical message")

if __name__ == "__main__":
    mon = log_monitoring()
    mon.get_docopt()
    mon.read_file()
    #mon.tailf_input() - logwatcher?
    #mon.write_to_db_based on log type
    #mon.exception for not tagged log message

    
