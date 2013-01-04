import cherrypy
import sys
import MySQLdb
from fgmetric.FGDatabase import FGDatabase

class FGResourceReporter:
    def __init__(self):
        self.db = FGDatabase()
        self.db.conf()
        self.db.connect()
        self.cloudservice = None

    def read_cloudservice(self):
        self.cloudservice = self.db.read_cloudplatform()

    def list(self):
        self.read_cloudservice()
        for service in self.cloudservice:
            print service["hostname"], service["institution"], service["platform"]
            
        return self.cloudservice
    
class FGRRWeb(object):

    def __init__(self):
        self.ins = FGResourceReporter()

    def list(self):
        return self.ins.list()

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def count_vms_user_india_euca(self):
        res = self.ins.get({"metric":"count", \
                "item":"vm", \
                "group":"user",\
                "nodename":"india",\
                "platform":"eucalyptus",\
                "search" : {'instanceState': {'code': '16', 'name': 'running'}}})
        return res

    list.exposed = True
    count_vms_user_india_euca.exposed = True

def connect(thread_index):
    cherrypy.thread_data.db = MySQLdb.connect('suzie.futuregrid.org', 'hrlee', 'AeT2W8Rh', 'cloudmetrics')

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "cmd":
        obj = FGResourceReporter()
        print obj.list()
    else:
        cherrypy.config.update({'server.socket_host': '129.79.49.179',
            'server.socket_port': 18080,
        #    'server.thread_pool': 10,
            })
        cherrypy.engine.subscribe('start_thread', connect)
        cherrypy.quickstart(FGRRWeb())

if __name__ == "__main__":
    main()
