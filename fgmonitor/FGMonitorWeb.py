import cherrypy
import json
from fgmonitor.FGMongodb import FGMongodb

class FGmonitorWeb:
    def __init__(self):
        self.fgmongodb = FGMongodb()
        self.fgmongodb.connect()

    def count_floatingIPs(self):
        res = []
        found = self.fgmongodb.find("floatingip", {})
        for record in found:
            total = len(record["data"])
            avail = 0
            for data in record['data']:
                if data['instanceid'] == 'None':
                    avail += 1
            res.append({ "service": record["service"],\
                    "hostname": record["hostname"], \
                    "total": total,\
                    "avail": avail,\
                    "time": str(record["time"])})

        return res

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def list(self):
        return self.count_floatingIPs()

    list.exposed = True

def main():
    cherrypy.config.update({'server.socket_host':'129.79.49.179', 
                            'server.socket_port': 28080,
                            'server.thread_pool': 10})
    #cherrypy.engine.subscribe('start_thread', connect)
    cherrypy.quickstart(FGmonitorWeb())

if __name__ == "__main__":
    main()
