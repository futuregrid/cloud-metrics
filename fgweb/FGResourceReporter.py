import subprocess
import cherrypy
import sys
import MySQLdb
from fgmetric.FGDatabase import FGDatabase
from fgweb.FGDescribeInstances import DescribeInstances

class FGResourceReporter:
    def __init__(self):
        self.euca2ools = DescribeInstances()
        self.euca2ools.init_stats()
        self.db = FGDatabase()
        self.db.conf()
        self.db.connect()
        self.cloudservice = None

    def read_cloudservice(self):
        self.cloudservice = self.db.read_cloudplatform()

    def read_HPC(self):
        # We put india as a test case here
        self.hpc = [{"hostname":"india", \
                    "institution": "IU", \
                    "platform": "HPC", \
                    "cores": 496 }]

    def list(self):
        res = self.list_cloudservice()
        res2 = self.list_HPC()
        return res + res2

    def list_HPC(self):
        res = []
        self.read_HPC()
        for hpc in self.hpc:
            status = "On" # for test
            usercount = self.hpctools(hpc["hostname"], "usercount").strip()
            nodecount = self.hpctools(hpc["hostname"], "nodecount").strip()
            corecount = self.hpctools(hpc["hostname"], "corecount").strip()
            utilization = str(round(100 * float(corecount) / hpc["cores"], 2)) + "%"
            res.append({ "Name": hpc["hostname"], \
                    "Institution": hpc["institution"], \
                    "Cloud Service": hpc["platform"], \
                    "Status": status, \
                    "Utilization":  utilization, \
                    "Active Projects": "--",\
                    "Active Users": usercount,\
                    "Running Instances": nodecount + "**", \
                    "Cores (used/avail)":  str(corecount) + " / " + str(hpc["cores"]) \
                    })
        return res

    def list_cloudservice(self):
        res = []
        self.read_cloudservice()
        for service in self.cloudservice:
            self.euca2ools.init_stats()
            self.euca2ools.init_xml()
            # TEMPORARy
            if service["cloudPlatformId"] == 1:
                continue
            if service["platform"] != "nimbus":
                self.euca2ools.set_service(service["platform"])
                self.euca2ools.set_hostname(service["hostname"])
                self.euca2ools.read_from_cmd()
                self.euca2ools.convert_xml_to_dict()
                self.euca2ools.print_ins(self.euca2ools.xml2dict)

            if self.euca2ools.fail_cmd:
                status = "Off"
            else:
                status = "On"
            utilization = self.get_utilization(service)
            self.adjust_nimbus(service)
            #print self.euca2ools.stats
            res.append({ "Name":service["hostname"], \
                    "Institution": service["institution"], \
                    "Cloud Service": service["platform"], \
                    "Status": status, \
                    "Utilization":  utilization, \
                    "Active Projects": self.euca2ools.stats["2. Groups"], \
                    "Active Users": self.euca2ools.stats["3. Users"], \
                    "Running Instances": self.euca2ools.stats["5. Running VMs"], \
                    "Cores (used/avail)":  str(self.euca2ools.stats["5. Running VMs"]) + " / " + str(service["cores"]) \
                    })
            #print self.euca2ools.display_stats()
            
        return res

    def get_utilization(self, service):
        cores = service["cores"]
        if service["platform"] == "nimbus":
            return "--*"
        return str(round(100 * float(self.euca2ools.stats["5. Running VMs"]) / float(cores), 2)) + "%"

    def adjust_nimbus(self, service):
        if service["platform"] == "nimbus":
            self.euca2ools.stats["2. Groups"] = "--*"
            self.euca2ools.stats["3. Users"] = "--*"
            self.euca2ools.stats["5. Running VMs"] = "--*"

    def hpctools(self, server, name, data=None):
        func = getattr(self, "_hpctools_" + str(name))
        return func(server, data)

    def _hpctools_usercount(self, server, data=None):
        return subprocess.check_output(["ssh","-i", "/home/hyungro/.ssh/.i","hrlee@" + server + ".futuregrid.org","qstat|grep \" R \"|awk '{ print $3}'|sort -u|wc -l"])
 
    def _hpctools_nodecount(self, server, data=None):
        return subprocess.check_output(["ssh","-i", "/home/hyungro/.ssh/.i","hrlee@" + server + ".futuregrid.org","qstat -n|grep \"/\"|sed -e \"s/+/\\n/g\" -e \"s/\s\+//\"|awk -F\"/\" '{ print $1}'|sort -u|wc -l"])

    def _hpctools_corecount(self, server, data=None):
        return subprocess.check_output(["ssh","-i", "/home/hyungro/.ssh/.i","hrlee@" + server + ".futuregrid.org","qstat -n|grep \"/\"|sed -e \"s/+/\\n/g\" -e \"s/\s\+//\"|awk -F\"/\" '{ print $2}'|awk '{s+=1} END {print s}'"])

class FGRRWeb(object):

    def __init__(self):
        self.ins = FGResourceReporter()

    def list(self):
        html_table = ""
        html_table_header = ""
        first = 0
        res = self.ins.list()
        for row in res:
            for k, v in row.iteritems():
                if first == 0:
                    html_table_header += "<th>" + str(k) + "</th>"
                html_table += "<td>" + str(v) + "</td>"
            first = 1
            html_table += "</tr><tr>"
        html_table = "<table><tr>" + html_table_header + "</tr><tr>" + html_table + "</tr></table>"
        html_table += "<br><p>* Nimbus doesn't support real time monitoring at this time"
        html_table += "<br>** HPC indicates nodes instead of VM instances" 
        return html_table

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
