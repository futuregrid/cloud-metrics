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
        try:
            fgconfig = FGConfig()
            self.dbinfo = fgconfig.get_config("CloudMetricsMongoDB")
        except:
            print "Failed to load futuregrid.yaml"
            raise

    def open_handler(self):
        # set logging
        try:
            self.log = logging.getLogger(self.name)
            self.log.addHandler(MongoHandler.to(db=self.dbinfo["db"], 
                collection='log', host=self.dbinfo["host"], 
                port=self.dbinfo["port"], username=self.dbinfo["user"],
                password=self.dbinfo["passwd"]))
        except:
            print "Faild to open mongodb"
            raise

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
        """Parse nova-api.log

        Log template:
        DATE LOG_TYPE API_NAME [REQUEST_ID USER_ID TENANT_ID] EVENT_MESSAGE

        Value type:
            DATE: YYYY-MM-DD HH:MM:SS
            LOG_TYPE: DEBUG|INFO|AUDIT|WARNING|ERROR|CRITICAL (*ref: nova/openstack/common/log.py)
            API_NAME: string with dot(.) (ex. nova.api.ec2)
            REQUEST_ID: req-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4} (ex.req-60eef213-ba15-4e59-8bc2-9b16049e11c1)
            USER_ID: [0-9a-f]{32} (id in keystone db)
            TENANT_ID: [0-9a-f]{32} (id in keystone db)
            EVENT_MESSAGE: msg

        Example message:
        2013-03-29 06:38:11 DEBUG nova.api.ec2 [req-77d26d51-0049-487e-a2af-a6e4fa79c056 e25c4264dcba4569a0c0d2f3f6a8919c 461884eef90047fbb4eb9ec92f22a1e3] action: DescribeAddresses from (pid=25893) __call__ /usr/lib/python2.7/dist-packages/nova /api/ec2/__init__.py:435
        """
        try:
            regex = re.compile("(\d{2,4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\s([^\s]*)\s([^\s]*)\s\[([^\s]*)\s([^\s]*)\s([^\s]*)\]\s([^$]*)")
            r = regex.search(line)
            log = {}
            log["date"] = r.group(1)
            log["log_type"] = r.group(2)
            log["api_name"] = r.group(3)
            log["request_id"] = r.group(4)
            log["user_id"] = r.group(5)
            log["tenant_id"] = r.group(6)
            log["event_message"] = r.group(7)


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

    
