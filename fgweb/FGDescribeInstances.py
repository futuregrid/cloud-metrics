import cherrypy
import subprocess
import sys
import os
import re
from collections import OrderedDict
import Xml2Dict
import Userinfo
import MySQLdb

class DescribeInstances:

    rawoutput = None
    xmloutput = None
    xml2dict = None
    platform = None
    hostname = None
    search_dict = None

    userinfo = None
    stats = None
    stats_internal = None

    def __init__(self):
        self.userinfo = Userinfo.Userinfo()
        self.init_stats()

    def init_stats(self):
        self.stats = { "1. Total":0, "2. Groups": 0, "3. Users":0, "5. Running VMs":0,  "4. Pending VMs":0, "7. Terminated VMs":0, "6. Shutting-down VMs":0}
        self.stats_internal = { "users": {}, "groups": {}}
        self.fail_cmd = False

    def init_xml(self):
        self.xmloutput = None
        self.xml2dict = None

    def get(self, obj):
        accumulated = {}
        self.set_search(obj)
        self.read_from_cmd() # set xmloutput
        self.convert_xml_to_dict() # set xml2dict
        instance_ids = self.get_val("instanceId", self.xml2dict, self.search_dict)
        owner_ids = self.userinfo.get_ownerId(instance_ids)
        for owner_id in owner_ids:
            owner_name = "".join(owner_id) #self.userinfo.convert_ownerId_str(owner_id['ownerId'])
            self.calculate_metric(obj["metric"], owner_name, accumulated)

        return accumulated

    def calculate_metric(self, operator, record, data, init_value=1):
        if not record in data:
            data[record] = init_value
        else:
            if operator == "count":
                data[record] += 1

    def set_search(self, obj):
        self.platform = obj["platform"]
        self.hostname = obj["nodename"]
        self.search_dict = obj["search"]

    def set_service(self, name):
        self.platform = name

    def set_hostname(self, name):
        self.hostname = name

    def list_instances(self):
        self.init_stats()
        res1 = self.list_eucalyptus()
        self.init_stats()
        res11 = self.list_eucalyptus_2()
        self.init_stats()
        res2 = self.list_openstack()
        res = self.header() + str(res1) + str(res11) + str(res2) + self.tail()
        
        return res

    def list_eucalyptus(self):
        self.platform = "eucalyptus"
        self.hostname = "india"
        self.read_from_cmd()
        self.convert_xml_to_dict()
        return self.display()
    
    def list_eucalyptus_2(self):
        self.platform = "eucalyptus"
        self.hostname = "sierra"
        self.read_from_cmd()
        self.convert_xml_to_dict()
        return self.display()

    def list_openstack(self):
        self.platform = "openstack"
        self.hostname = "india"
        self.read_from_cmd()
        self.convert_xml_to_dict()
        return self.display()

    def get_val(self, keyname, data, search_dict=None):
        val_list = []
        if search_dict:
            for search_item in search_dict.keys():
                if search_item in data and data[search_item] != search_dict[search_item]:
                    return val_list

        for key, val in data.iteritems():
            if isinstance(val, dict):
                val_list.extend(self.get_val(keyname, val, search_dict))
            else:
                if key == keyname:
                    val_list.append(val)
        return val_list

    def display(self):
        title = self.display_title()
        if self.fail_cmd:
            return title 
        table = self.display_table()
        stats = self.display_stats() 
        return title + stats + "<br><br>" + table

    def display_title(self):
        return "<h2>"+self.platform.title()+ " on " + self.hostname.title() + " *</h2>"

    def display_stats(self):
        ''' display summary of vms '''
        msg = ""
        for key, value in sorted(self.stats.iteritems()):
            if key == "2. Groups":
                description = "group(s)"
            elif key == "3. Users":
                description = "user(s)"
            else:
                description = "instance(s)"
            msg += "<tr><td>%s<td>%s %s</td></tr>"  % (key, value, description)
        return "<table border=1>"+msg+"</table>"

    def count_stats(self, k, v):
        if k == "ownerId":
            self.stats["1. Total"] += 1
        elif k == "name":
            if v == "running":
                self.stats["5. Running VMs"] += 1
            elif v == "terminated":
                self.stats["7. Terminated VMs"] += 1
            elif v == "pending":
                self.stats["4. Pending VMs"] += 1
            elif v == "shutting-down":
                self.stats["6. Shutting-down VMs"] += 1

        elif k == "keyName":
            if v in self.stats_internal["users"]:
                self.stats_internal["users"][v] += 1
            else:
                self.stats_internal["users"][v] = 1
        if k == "ownerId":
            if v in self.stats_internal["groups"]:
                self.stats_internal["groups"][v] += 1
            else:
                self.stats_internal["groups"][v] = 1

        self.stats["2. Groups"] = len(self.stats_internal["groups"])
        self.stats["3. Users"] = len(self.stats_internal["users"])
        return

    def display_table(self):
        #for i in self.xml2dict.iteritems():
        #    print i
        res = ""
        header = "<th>ownerId<th>groupId<th>reservationId<th>productCodes<th>blockDeviceMapping<th>availabilityZone<th>ipAddress<th>instanceId<th>code<th>state<th>Monitoring<th>keyName<th>imageId<th>privateDnsName<th>reason<th>dnsName<th>launchTime<th>rootDeviceType<th>rootDeviceName<th>kernelId<th>ramdiskId<th>amiLaunchIndex<th>instanceType<th>privateIpAddress"
        if self.platform == "openstack":
            header = "<th>ownerId<th>groupId<th>reservationId<th>availabilityZone<th>dnsName<th>instanceType<th>kernelId<th>instanceId<th>code<th>state<th>publicDnsName<th>imageId<th>productCodesSet<th>privateDnsName<th>ipAddress<th>keyName<th>launchTime<th>rootDeviceType<th>ramdiskId<th>amiLaunchIndex<th>rootDeviceName<th>privateIpAddress<th>requestId"

        res = res + "<table border=1>"+ header + self.print_ins(self.xml2dict)+"</table>"
        return res

    def get_cmd(self):
        cmd = ["euca-describe-instances", "verbose", "--debug"]
        if self.platform == "eucalyptus":
            if self.hostname == "india":
                cmd.extend(["--config", "/home/hyungro/.futuregrid/eucalyptus/admin/eucarc"])
            elif self.hostname == "sierra":
                cmd.extend(["--config", "/home/hyungro/.futuregrid/eucalyptus/sierra/admin/eucarc"])
        elif self.platform == "openstack":
            if self.hostname == "india":
                cmd.extend(["--config", "/home/hyungro/.futuregrid/openstack/novarc"])
                cmd.remove("verbose")

        return cmd

    def read_from_cmd(self, cmd=None):

        if not cmd:
            cmd = self.get_cmd()

        try:
            self.rawoutput = subprocess.check_output(cmd, stderr=subprocess.STDOUT).splitlines()
        except:
            self.fail_cmd = True
            print sys.exc_info
            return

        for line in self.rawoutput:
            if re.search("DescribeInstancesResponse", line):
                self.xmloutput = line.split("[DEBUG]:")[1]
                break

    def convert_xml_to_dict(self):
        try:
            xml2dict = Xml2Dict.Xml2Dict(self.xmloutput)
            self.xml2dict = xml2dict.parse()
        except:
            pass

    def header(self):
        return "<h1>Web-based euca-describe-instances</h1> showing information about instances on FutureGrid (Eucalyptus, OpenStack)"

    def tail(self):
        return "<br><p>* These sections are mainly generated by the execution of admin's euca-describe-instances.<br>\
                This web-based euca-describe-instances helps to viewing information about instances in summary or in detail.<br>\
                Refresh your browser to get the latest information.<br><br>\
                To show a short summary of launched instances, we simply created statistics.<br>\
                1. Total shows the number of total launched instances,<br>\
                2. Groups shows the number of total groups that requested instances,<br>\
                3. Users shows the number of total users who requested instances,<br>\
                4. Pending VMs shows the number of initializing instances,<br>\
                5. Running VMs shows the number of working instances,<br>\
                6. Shutting-down VMs shows the number of stopping instances,<br>\
                7. Terminated VMs shows the number of removed instances.<br>\
                For more information about ec2(euca)-describe-instances, please refer to <a href=\"http://docs.amazonwebservices.com/AWSEC2/latest/CommandLineReference/ApiReference-cmd-DescribeInstances.html\">aws documentation</a>.\
                <br><br>\
                Source repository: <a href=\"https://github.com/lee212/Misc\">github: Misc/euca-describe-instances-web</a>\
                <br>\
                Powered by CherryPy"

        #return "<p><span style=\"font-size:10px;\">" + str(msg) + "</span></p>"

    def convert_to_dict_from_stdout(self):

        # http://docs.amazonwebservices.com/AWSEC2/latest/CommandLineReference/ApiReference-cmd-DescribeInstances.html
        #
        # example:
        #
        # RESERVATION   r-078141E6  110223663177    default
        # INSTANCE    i-DA574028  emi-A8F63C29    149.165.158.203 10.131.178.57   running selvikey    0       m1.small    2012-10-17T23:58:18.188Z    euca3india  eki-226638E6    eri-32DE3771        monitoring-disabled 149.165.158.203 10.131.178.57           instance-store                                  
        # RESERVATION r-982D3FA6  458299102773    default
        # INSTANCE    i-44014279  emi-FB4A3E74    149.165.158.223 10.133.83.96    running     0       m1.small    2012-09-17T19:23:37.693Z    euca3india  eki-226638E6    eri-32DE3771        monitoring-disabled 149.165.158.223 10.133.83.96            instance-store                                  
        # RESERVATION r-3DAE42F2  159083787446    default
        # INSTANCE    i-80924259  emi-805D3DBD    149.165.158.228 10.150.212.78   running my-instance1    0       m1.large    2012-09-23T20:53:19.016Z    euca3india  eki-226638E6    eri-32DE3771        monitoring-disabled 149.165.158.228 10.150.212.78           instance-store                                  
        #
        # RESERVATION     r-705d5818      111122223333    default
        # INSTANCE        i-53cb5b38      ami-b232d0db    ec2-184-73-10-99.compute-1.amazonaws.com domU-12-31-39-00-A5-11.compute-1.internal        running         0               m1.small 2010-04-07T12:49:28+0000 us-east-1a      aki-94c527fd    ari-96c527ff            monitoring-disabled       184.73.10.99    10.254.170.223                  ebs   paravirtual  xen
        # BLOCKDEVICE     /dev/sda1       vol-a36bc4ca    2010-04-07T12:28:01.000Z
        # BLOCKDEVICE     /dev/sdb        vol-a16bc4c8    2010-04-07T12:28:01.000Z
        # RESERVATION     r-705d5818      111122223333    default
        # INSTANCE        i-39c85852      ami-b232d0db    terminated      gsg-keypair       0               m1.small        2010-04-07T12:21:21+0000        us-east-1a      aki-94c527fd      ari-96c527ff            monitoring-disabled                              ebs   paravirtual  xen
        # RESERVATION     r-9284a1fa      111122223333    default
        # INSTANCE        i-996fc0f2      ami-3c47a355    ec2-184-73-195-182.compute-1.amazonaws.com domU-12-31-39-09-25-62.compute-1.internal       running keypair    0               m1.small  2010-03-17T13:17:41+0000        us-east-1a      aki-a71cf9ce    ari-a51cf9cc     monitoring-disabled      184.73.195.182  10.210.42.144                   instance-store   paravirtual  xen
        #########################
        # The RESERVATION identifier
        # The ID of the reservation
        # The AWS account ID
        # The name of each security group the instance is in (for instances not running in a VPC)
        #########################
        # The INSTANCE identifier
        # The ID of each running instance
        # The AMI ID of the image on which the instance is based
        # The public DNS name associated with the instance. This is only present for instances in the running state.
        # The private DNS name associated with the instance. This is only present for instances in the running state.
        # The state of the instance
        # The key name. If a key was associated with the instance at launch, its name will appear.
        # The AMI launch index
        # The product codes associated with the instance
        # The instance type

        # The instance launch time
        # The Availability Zone
        # The ID of the kernel
        # The ID of the RAM disk
        # The monitoring state
        # The public IP address

        # The private IP addresses associated with the instance. Multiple private IP addresses are only available in Amazon VPC.
        # The tenancy of the instance (if the instance is running within a VPC). An instance with a tenancy of dedicated runs on single-tenant hardware.
        # The subnet ID (if the instance is running in a VPC)
        # The VPC ID (if the instance is running in a VPC)
        # The type of root device (ebs or instance-store)
        # The placement group the cluster instance is in
        # The virtualization type (paravirtual or hvm)
        # The ID of each security group the instance is in (for instances running in a VPC)
        # Any tags assigned to the instance
        # The hypervisor type (xen or ovm)
        #########################
        # The BLOCKDEVICE identifier (one for each Amazon EBS volume, if the instance has a block device mapping), along with the device name, volume ID, and timestamp
        lines = self.output.split("\n")

        prog = re.compile( r'(?P<rsv_title>\w+)\s+(?P<rsv_id>[\w-]+)\s+(?P<account_id>\w+)\s+(?P<security_group>\w+)\n\
                (?P<ins_title>\w+)\s+(?P<ins_id>[\w-]+)\s+(?P<ami_id>[\w-]+)\s+(?P<public_dns>[\d.]+)\s+(?P<state>\w+)\s+(?P<owner_id>[\w-]+)\s+(?P<launch_index>\d+)\s+(?P<ins_type>[\w.]+)\s+\
                (?P<ins_launch_time>[\dT:+-Z]+)\s+(?P<availability_zone>[\w-]+)\s+(?P<kernel_id>[\w-]+)\s+(?P<ramdisk_id>[\w-]+)\s+(?P<monitoring_state>[\w-]+)\s+(?P<public_ip>[\d.]+)\s+\
                (?P<private_ip>[\d.]+)\s+(?P<tenancy>[\w-]+)\s+(?P<vir_type>\w+)\s+(?P<hyper_type>\w+)', re.M|re.I)

    def print_ins(self, dictionary, ident = '', braces=1):
        all_msg = ""
        try:
            for key, value in dictionary.iteritems():
                msg = ""
                if isinstance(value, dict):
                    #msg = '%s%s%s%s' %(ident,braces*'[',key,braces*']') 
                    if braces == 2:
                        msg = "<tr>"
                    ident = str(key)
                    msg = msg + self.print_ins(value, ident+' ', braces+1)
                else:
                    msg = "<td>" + str(value) + "</td>"
                    self.count_stats(key, value)
                all_msg = all_msg + msg
        except:
            pass

        return all_msg

    def print_dict(self, dictionary, ident = '', braces=1):
        """ Recursively prints nested dictionaries."""

        for key, value in dictionary.iteritems():
            if isinstance(value, dict):
                print '%s%s%s%s' %(ident,braces*'[',key,braces*']') 
                self.print_dict(value, ident+'  ', braces+1)
            else:
                print ident+'%s = %s' %(key, value)

    def output(self):
        return "Hello World!"

class DescribeInstancesWeb(object):

    def __init__(self):
        self.ins = DescribeInstances()

    def index(self):
        return self.ins.output()

    def list(self):
        return self.ins.list_instances()

    def count(self):
        return

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
        #sorted_res = OrderedDict(sorted(res.items(), key=lambda t: t[0]))
        #return sorted_res

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def count_vms_user_sierra_euca(self):
        return self.ins.get({"metric":"count", \
                "item":"vm", \
                "group":"user",\
                "nodename":"sierra",\
                "platform":"eucalyptus",\
                "search" : {'instanceState': {'code': '16', 'name': 'running'}}})

    index.exposed = True
    list.exposed = True
    count_vms_user_india_euca.exposed = True
    count_vms_user_sierra_euca.exposed = True

def connect(thread_index):
    cherrypy.thread_data.db = MySQLdb.connect(os.environ["FG_METRIC_DB_HOST"], os.environ["FG_METRIC_DB_ID"], os.environ["FG_METRIC_DB_PASS"], os.environ["FG_METRIC_DB_NAME"])

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "cmd":
        obj = DescribeInstances()
        obj.list_instances()
    else:
        #cherrypy.tree.mount(DescribeInstancesWeb())
        #cherrypy.engine.start(blocking=False)
        #cherrypy.server.socket_port = 8765
        #errypy.server.quickstart()
        #webbrowser.open("http://192.79.49.179:8765")
        #cherrypy.engine.block()
        # CherryPy autoreload must be disabled for the flup server to work
        #cherrypy.config.update({'engine.autoreload_on':False})
        cherrypy.config.update({'server.socket_host': os.environ["FG_HOSTING_IP"],
            'server.socket_port': 8080,
        #    'server.thread_pool': 10,
            })
        cherrypy.engine.subscribe('start_thread', connect)
        cherrypy.quickstart(DescribeInstancesWeb())

if __name__ == "__main__":
    main()
