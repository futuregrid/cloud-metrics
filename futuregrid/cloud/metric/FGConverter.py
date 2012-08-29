import futuregrid.cloud.metric.FGParser as FGParser
import argparse
import sqlite3 as lite
from collections import deque
import os
from datetime import datetime

class FGConverter:

    instances = FGParser.Instances()

    future = instances.in_the_future
    past = instances.in_the_past

    s_date = None
    e_date = None

    filename = None
    filepath = None

    platform = None
    platform_version = None
    hostname = None
    confname = None

    rows = None     #from database
    records = None  #for fg database

    def convert_to_fg(self):
        if self.platform == "nimbus":
            self.platform_version = "2.9"
            self.read_sqlite3()
            self.map_to_fg()

        self.write_db()

    def read_sqlite3(self):

        try: 
            con = lite.connect(self.filepath + "/" + self.filename, detect_types = lite.PARSE_COLNAMES)
            con.row_factory = lite.Row
            con.text_factory = str
            cur = con.cursor()
            cur.execute('select t1.time as "t_start [timestamp]", t3.time as "t_end [timestamp]", t1.uuid as instanceId, t2.dn, t1.cpu_count as ccvm_cores, t1.memory as ccvm_mem, t1.vmm as serviceTag from create_events t1, user t2, remove_events t3 on t1.user_id=t2.id and t1.uuid=t3.uuid where t1.time >= \'' + str(self.s_date) + '\' and t3.time <= \'' + str(self.e_date) + '\'')
            rows = cur.fetchall()
            self.rows =rows
        except lite.Error, e:
            print "Error %s:" % e.args[0]
            pass
        finally:
            if con:
                con.close()

    def map_to_fg(self):
        rows = self.rows
        records = []

        for row in rows:
            record = {}

            record["instanceId"] = row["instanceId"][:15]
            record["ts"] = row["t_start"]
            record["calltype"] = ""
            record["userData"] = ""
            record["kernelId"] = ""
            record["emiURL"] = ""
            record["t_start"] = row["t_start"]
            record["t_end"] = row["t_end"]
            record["duration"] = (row["t_end"] - row["t_start"]).total_seconds()
            record["trace"] = {
                "pending" : { "start" : self.future, "stop" : self.past, "queue" : deque("",10)},
                "extant" : { "start" : self.future, "stop" : self.past, "queue" : deque("",10)},
                "teardown" : { "start" : self.future, "stop" : self.past, "queue" : deque("",10)}
                }
            record["serviceTag"] = row["serviceTag"] or ""
            record["groupNames"] = ""
            record["keyName"] = ""
            record["msgtype"] = ""
            record["volumesSize"] = 0.0
            record["linetype"] = ""
            if len(row["dn"].split("CN=")) > 1:
                record["ownerId"] = row["dn"].split("CN=")[1]
            else:
                record["ownerId"] = row["dn"]
            record["date"] = row["t_start"]
            record["id"] = 0
            record["ncHostIdx"] = 0
            record["ccvm"] = { "mem" : row["ccvm_mem"], "cores" : row["ccvm_cores"], "disk" : 0 }
            record["emiId"] = ""
            record["ccnet"] = { "publicIp" : "", "privateMac" : "", "networkIndex" : "", "vlan" : "", "privateIp" : "" }
            record["ramdiskURL"] = ""
            record["accountId"] = ""
            record["kernelURL"] = ""
            record["ramdiskId"] = ""
            record["volumes"] = ""
            record["launchIndex"] = 0
            record["bundleTaskStateName"] = ""
            record["reservationId"] = ""
            record["platform"] = self.platform
            record["euca_hostname"] = self.hostname
            record["euca_version"] = self.platform_version
            record["state"] = "Teardown" # need to be changed
            records.append(record)

        self.records = records

    def write_db(self):

        for record in self.records:
            self.instances.eucadb.write(record)
                                        
    def set_parser(self):
        def_s_date = "19700101"
        def_e_date = "29991231"
        def_conf = "futuregrid.cfg"

        parser = argparse.ArgumentParser()
        parser.add_argument("-s", "--from", dest="s_date", default=def_s_date,
                help="Start date to begin parsing (type: YYYYMMDD)")
        parser.add_argument("-e", "--to", dest="e_date", default=def_e_date,
                help="End date to finish parsing (type: YYYYMMDD)")
        parser.add_argument("-i", "--file", dest="input_file", required=True,
                help="the sqlite3 filename with path (e.g. /home/metric/nimbus/alamo/alamo) ")
        parser.add_argument("-p", "--platform", required=True,
                help="Cloud platform name, required. (e.g. nimbus, openstack, eucalyptus, etc)")
        parser.add_argument("-n", "--hostname", required=True,
                help="Hostname of the cloud platform, required. (e.g., hotel, sierra, india, alamo, foxtrot)")
        parser.add_argument("--conf", dest="conf",
                help="The configuraton file of the FG Cloud Metrics (e.g. $HOME/.futuregrid/futuregrid.cfg) ")
        self.parser = parser
        args = parser.parse_args()
        print args

        self.s_date = datetime.strptime(args.s_date, "%Y%m%d")
        self.e_date = datetime.strptime(args.e_date, "%Y%m%d")
        abspath = os.path.abspath(args.input_file)
        filename = os.path.basename(abspath)
        filepath = os.path.dirname(abspath)
        self.filename = filename
        self.filepath = filepath
        self.platform = args.platform
        self.hostname = args.hostname
        self.confname = self.set_instance_conf(args.conf)

    def set_instance_conf(self, confname=""):
        if len(confname) > 0:
            self.instances.set_conf(confname)

def main():
    converter = FGConverter()
    converter.set_parser()
    converter.convert_to_fg()

if __name__ == "__main__":
    main()
