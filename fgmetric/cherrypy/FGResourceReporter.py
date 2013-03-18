import json
import subprocess
import cherrypy
import sys
import os
import MySQLdb
from fgmetric.shell.FGDatabase import FGDatabase
from fgmetric.cherrypy.FGDescribeInstances import DescribeInstances

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
                    "cores": 488 },
                    {"hostname":"alamo", \
                    "institution": "TACC", \
                    "platform": "HPC", \
                    "cores": 608 },
                    {"hostname": "hotel", \
                    "institution": "UC", \
                    "platform": "HPC", \
                    "cores": 312 },
                    {"hostname": "sierra", \
                    "institution": "UCSD", \
                    "platform": "HPC", \
                    "cores": 248}]

    def list(self):
        res = self.list_cloudservice()
        res2 = self.list_HPC()
        return res + res2

    def list_HPC(self):
        res = []
        self.read_HPC()
        for hpc in self.hpc:
            status = "On" # for test
            try:
                usercount = self.hpctools(hpc["hostname"], "usercount").strip()
                nodecount = self.hpctools(hpc["hostname"], "nodecount").strip()
                corecount = self.hpctools(hpc["hostname"], "corecount").strip()
                utilization = str(round(100 * float(corecount) / hpc["cores"], 2)) + "%"
            except:
                print sys.exc_info()
                usercount = nodecount  = corecount = utilization = 0 
                status = "Off"

            res.append({ "Name": hpc["hostname"], \
                    "Institution": hpc["institution"], \
                    "Cloud Service": hpc["platform"], \
                    "Status": status, \
                    "Utilization":  utilization, \
                    "Active Projects": "--",\
                    "Active Users": usercount,\
                    "Running Instances": str(nodecount) + "**", \
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
                html = self.euca2ools.print_ins(self.euca2ools.xml2dict)
                groups = self.euca2ools.stats["2. Groups"]
                users = self.euca2ools.stats["3. Users"]
                vms = self.euca2ools.stats["5. Running VMs"]
                cores = vms
                utilization = self.get_utilization(service)
                if self.euca2ools.fail_cmd:
                    status = "Off"
                else:
                    status = "On"
                if html[:13] == "<td>None</td>":
                    status = "Off"

            else:
                groups = "--"
                users = self.nimbustools(service["hostname"],"users")
                vms = self.nimbustools(service["hostname"],"nodes")
                cores = self.nimbustools(service["hostname"],"cores")
                utilization = self.get_utilization_nimbus(cores, service)
                status = "On*"

            #print self.euca2ools.stats
            res.append({ "Name":service["hostname"], \
                    "Institution": service["institution"], \
                    "Cloud Service": service["platform"], \
                    "Status": status, \
                    "Utilization":  utilization, \
                    "Active Projects": groups, \
                    "Active Users": users, \
                    "Running Instances": vms, \
                    "Cores (used/avail)":  str(cores) + " / " + str(service["cores"]) \
                    })
            #print self.euca2ools.display_stats()
            
        return res

    def get_utilization(self, service):
        return str(round(100 * float(self.euca2ools.stats["5. Running VMs"]) / float(service["cores"]), 2)) + "%"

    def get_utilization_nimbus(self, vms, service):
        return str(round(100 * float(vms) / float(service["cores"]), 2)) + "%"

    def hpctools(self, server, name, data=None):
        func = getattr(self, "_hpc_" + str(name))
        return func(server, data)

    def _hpc_usercount(self, server, data=None):
        ''' Execute qstat in remote
        
        qstat provides pbs node information for more detail, see:http://www.clusterresources.com/torquedocs21/commands/qstat.shtml 
        We get " R " state. This can be performed in the other way like 'qstat -B' but it is same, we keep our own way.
        
        '''
        return subprocess.check_output(["ssh","-i", "/home/hyungro/.ssh/.i","hrlee@" + server + ".futuregrid.org","source /etc/bashrc;qstat|grep \" R \"|awk '{ print $3}'|sort -u|wc -l"])
 
    def _hpc_nodecount(self, server, data=None):
        ''' Execute qstat in remote and parse exec_host values to get nodes

        qstat -f -1 displays full information. exec_host means running host information with specific template like 'hostname/core_number+...'
        our script simply separates them and counts it'''

        return subprocess.check_output(["ssh","-i", "/home/hyungro/.ssh/.i","hrlee@" + server + ".futuregrid.org","source /etc/bashrc;qstat -f -1|sed -ne \"s/^\\s*exec_host = //p\"|sed \"s/+/\\n/g\"|awk -F\"/\" '{ print $1}'|sort -u|wc -l"])

    def _hpc_corecount(self, server, data=None):
        return subprocess.check_output(["ssh","-i", "/home/hyungro/.ssh/.i","hrlee@" + server + ".futuregrid.org","source /etc/bashrc;qstat -f -1|sed -ne \"s/^\\s*exec_host = //p\"|sed \"s/+/\\n/g\"|wc -l"])
            #awk -F\"/\" '{ print $2}'|awk '{s+=1} END {print s}'"])

    def nimbustools(self, server, name, data=None):
        func = getattr(self, "_nimbus_" + str(name))
        return func(server, data)

    def _nimbus_users(self, server, data=None):
        res = subprocess.check_output(["ssh","-i", "/home/hyungro/.ssh/.i","hrlee@hotel.futuregrid.org","cat /home/nimbus/realtime_metrics/" + server + "/nimbus_admin.json"])
        data = json.loads(res)
        self.nimbus_users = data
        users = {}
        for record in data:
            if record["state"] in {"Running", "Cancelled"} :
                users[record["creator"]] = None
        return len(users)

    def _nimbus_cores(self, server, data=None):
        try:
            data = self.nimbus_users
        except:
            res = subprocess.check_output(["ssh","-i", "/home/hyungro/.ssh/.i","hrlee@hotel.futuregrid.org","cat /home/nimbus/realtime_metrics/" + server + "/nimbus_admin.json"])
            data = json.loads(res)
            self.nimbus_users = data
        cores = 0
        for record in data:
            if record["state"] in { "Running", "Cancelled"}:
                cores += int(record["cpu count"])
        return cores

    def _nimbus_nodes(self, server, data=None):
        res = subprocess.check_output(["ssh","-i", "/home/hyungro/.ssh/.i","hrlee@hotel.futuregrid.org","cat /home/nimbus/realtime_metrics/" + server + "/nimbus_admin.json"])
        data = json.loads(res)
        cnt = 0
        for record in data:
            if record["state"] in { "Running", "Cancelled"}:#record["in_use"] == "true":#record["active"] == "true":
                cnt += 1
        return cnt

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
        html_table += "<br>* Nimbus has been updated every minute"
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
    cherrypy.thread_data.db = MySQLdb.connect(os.environ["FG_METRIC_DB_HOST"], os.environ["FG_METRIC_DB_ID"], os.environ["FG_METRIC_DB_PASS"], os.environ["FG_METRIC_DB_NAME"])

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "cmd":
        obj = FGResourceReporter()
        print obj.list()
    else:
        cherrypy.config.update({'server.socket_host': os.environ["FG_HOSTING_IP"],
            'server.socket_port': 18080,
        #    'server.thread_pool': 10,
            })
        cherrypy.engine.subscribe('start_thread', connect)
        cherrypy.quickstart(FGRRWeb())

if __name__ == "__main__":
    main()
