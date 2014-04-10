import cherrypy
import json
from fgmetric.realtime.FGMongodb import FGMongodb
from fgmetric.charts.FGCharts import FGCharts

class FGmonitorWeb:
    def __init__(self):
        self.fgmongodb = FGMongodb()
        self.fgmongodb.connect()
        self.chart = FGCharts()

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

    def series_floatingIPs(self):
        res = {}
        found = self.fgmongodb.find("floatingip", {})
        for record in found:
            total = len(record["data"])
            avail = total
            for data in record['data']:
                if data['instanceid'] == 'None':
                    avail += 1
            res[record["time"]] = avail

        new_res = { "name" : "floatingip",\
                    "data" : res }
        return [new_res]

    def count_computenodes(self):
        res = []
        found = self.fgmongodb.find("computenodes", {})
        for record in found:
            total = len(record["data"])
            avail = total
            for data in record['data']:
                if data['state'] != ':-)':
                    avail -= 1
            res.append({ "service": record["service"],\
                    "hostname": record["hostname"], \
                    "total": total,\
                    "avail": avail,\
                    "time": str(record["time"])})

        return res

    def series_computenodes(self):
        res = {}
        found = self.fgmongodb.find("computenodes", {})
        for record in found:
            total = len(record["data"])
            avail = total
            for data in record['data']:
                if data['state'] != ':-)':
                    avail -= 1
            res[record["time"]] = avail

        new_res = { "name" : "computenodes",\
                    "data" : res }
        return [new_res]

    @cherrypy.expose
    def chart_computenodes(self):
        self.chart.set_chart_api("highcharts")
        self.chart.set_type("line-time-series")
        res = self.series_computenodes()
        self.chart.set_series(res)
        self.chart.load_script_path("global")
        res = {"stdout":None}
        self.chart.display(res)
        return res["stdout"]

    @cherrypy.expose
    def chart_floatingips(self):
        self.chart.set_chart_api("highcharts")
        self.chart.set_type("line-time-series")
        res = self.series_floatingIPs()
        self.chart.set_series(res)
        self.chart.load_script_path("global")
        res = {"stdout":None}
        self.chart.display(res)
        return res["stdout"]

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def list(self):
        return self.count_floatingIPs()

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def listips(self):
        return self.count_floatingIPs()

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def listnodes(self):
        return self.count_computenodes()

    listips.exposed = True
    listnodes.exposed = True
    list.exposed = True

def main():
    cherrypy.config.update({'server.socket_host':'129.79.49.179', 
                            'server.socket_port': 28080,
                            'server.thread_pool': 10})
    #cherrypy.engine.subscribe('start_thread', connect)
    cherrypy.quickstart(FGmonitorWeb())

if __name__ == "__main__":
    main()
