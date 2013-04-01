import logging
from mongolog.handlers import MongoHandler
from fgmetric.shell.FGConfig import FGConfig

class monitoring:

    # cloud service name + hostname
    name = "nova-api.india" 

    def __init__(self):

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
        log.setLevel(logging.DEBUG)
        log.debug("1 - debug message")
        log.info("2 - info message")
        log.warn("3 - warn message")
        log.error("4 - error message")
        log.critical("5 - critical message")
