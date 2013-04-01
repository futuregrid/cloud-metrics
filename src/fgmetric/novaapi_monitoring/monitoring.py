import logging
from mongolog.handlers import MongoHandler
from fgmetric.shell.FGConfig import FGConfig

class monitoring:

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

    def _test(self):
        self.log.setLevel(logging.DEBUG)
        self.log.debug("1 - debug message")
        self.log.info("2 - info message")
        self.log.warn("3 - warn message")
        self.log.error("4 - error message")
        self.log.critical("5 - critical message")

if __name__ == "__main__":
    mon = monitoring()
    #mon.get_docopt()
    #mon.parse_file()
    #mon.tailf_input() - logwatcher?
    #mon.write_to_db_based on log type
    #mon.exception for not tagged log message

    
