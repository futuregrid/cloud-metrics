import argparse, os
import sqlite3 as lite
import MySQLdb
from collections import deque
from datetime import datetime
import fgmetric.FGParser as FGParser

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
    read_database = None
    dbname = None
    dbname_nova = None
    dbname_keystone = None
    dbhost = None
    dbuser = None
    dbpass = None
    dbport = None

    rows = None     #from database
    records = None  #for fg database

    def convert_to_fg(self):
        if not self.check_platform():
            return
        self.read_database()
        self.map_to_fg()
        self.write_db()

    def check_platform(self):
        if self.platform == "nimbus":
            if not self.filename or not self.filepath:
                print "sqlite3 file is missing"
                return False
            default_version = "2.9"
            read_database = getattr(self, "read_" + "sqlite3")
        elif self.platform == "openstack":
            if not self.dbname_nova or not self.dbname_keystone or not self.dbhost or not self.dbuser or not self.dbpass:
                print "db info is missing"
                return False
            default_version = "essex"
            read_database = getattr(self, "read_" + "nova_and_keystone")
        
        self.read_database = read_database

        if not self.platform_version or len(self.platform_version) == 0:
            self.platform_version = default_version

        return True

    def read_sqlite3(self):

        try: 
            con = lite.connect(self.filepath + "/" + self.filename, detect_types = lite.PARSE_COLNAMES)
            def dict_factory(cursor, row):
                d = {}
                for idx, col in enumerate(cursor.description):
                    d[col[0]] = row[idx]
                return d
            con.row_factory = dict_factory#lite.Row
            con.text_factory = str
            cur = con.cursor()
            cur.execute('select t1.time as "t_start [timestamp]",\
                    t3.time as "t_end [timestamp]",\
                    t1.uuid as instanceId,\
                    t2.dn,\
                    t1.cpu_count as ccvm_cores,\
                    t1.memory as ccvm_mem,\
                    t1.vmm as serviceTag \
                    from create_events t1, user t2, remove_events t3 \
                    on t1.user_id=t2.id and t1.uuid=t3.uuid \
                    where t1.time >= \'' + str(self.s_date) + '\' and t3.time <= \'' + str(self.e_date) + '\'')
            rows = cur.fetchall()
            self.rows = rows
        except lite.Error, e:
            print "Error %s:" % e.args[0]
            pass
        finally:
            if con:
                con.close()

    def read_nova_and_keystone(self):

        conn = None
        try:
            #connect to db
            conn = MySQLdb.connect (self.dbhost, self.dbuser, self.dbpass, self.dbname_nova, self.dbport)#dbhost, dbuser, dbpasswd, dbname, dbport)
            cursor = conn.cursor (MySQLdb.cursors.DictCursor)
            # 1. draw mapping table between openstack 'instances' and fg 'instance' table.
            # 2. define each column to know what exactly it means
            # 3. leave comments for missing and skipped columns
            # 4. check search options to see it is validate
            rquery = 'SELECT created_at as trace_extant_start,\
                    id,\
                    user_id as ownerId,\
                    project_id as accountId,\
                    image_ref as emiId,\
                    kernel_id as kernelId,\
                    ramdisk_id as ramdiskId,\
                    key_data as keyName,\
                    vm_state as state,\
                    memory_mb as ccvm_mem, \
                    vcpus as ccvm_cores, \
                    host as serviceTag, \
                    reservation_id as reservationId,\
                    launched_at as t_start, \
                    terminated_at as t_end, \
                    uuid as instanceId, \
                    access_ip_v4 as ccnet_publicIp,\
                    ephemeral_gb as ccvm_disk \
                    from instances \
                    where updated_at >= \'' + str(self.s_date) + '\' and updated_at <= \'' + str(self.e_date) + '\''
            cursor.execute(rquery)
            rows = cursor.fetchall()
            self.rows = rows
        except MySQLdb.Error, e:
            print "Error %s:" % e.args[0]
            pass
        finally:
            if conn:
                cursor.close()
                conn.close()

    def read_userinfo(self):
        print 1
    def read_cloudplatform(self):
        print 1

    def map_to_fg(self):
        rows = self.rows
        records = []

        for row in rows:
            record = row

            record["instanceId"] = record["instanceId"][:15]
            record["ts"] = record["t_start"]
            #record["calltype"] = ""
            #record["userData"] = ""
            #record["kernelId"] = ""
            #record["emiURL"] = ""
            #record["t_start"] = row["t_start"]
            #record["t_end"] = row["t_end"]
            record["duration"] = (record["t_end"] - record["t_start"]).total_seconds()
            #record["trace"] = {
            #    "pending" : { "start" : self.future, "stop" : self.past, "queue" : deque("",10)},
            #    "extant" : { "start" : self.future, "stop" : self.past, "queue" : deque("",10)},
            #    "teardown" : { "start" : self.future, "stop" : self.past, "queue" : deque("",10)}
            #    }
            #record["serviceTag"] = row["serviceTag"] or ""
            #record["groupNames"] = ""
            #record["keyName"] = ""
            #record["msgtype"] = ""
            #record["volumesSize"] = 0.0
            #record["linetype"] = ""
            if "dn" in record and not "ownerId" in record:
                if len(record["dn"].split("CN=")) > 1:
                    record["ownerId"] = record["dn"].split("CN=")[1]
                else:
                    record["ownerId"] = record["dn"]
            record["date"] = record["t_start"]
            #record["id"] = 0
            #record["ncHostIdx"] = 0
            #record["ccvm"] = { "mem" : record["ccvm_mem"], "cores" : record["ccvm_cores"], "disk" : record[0 }
            #if "ccvm_disk" in row:
            #    record["ccvm"]["disk"] = row["ccvm_disk"]
            #if "emiId" in row:
            #    record["emiId"] = row["emiId"]
            #else:
            #    record["emiId"] = ""
            #record["ccnet"] = { "publicIp" : "", "privateMac" : "", "networkIndex" : "", "vlan" : "", "privateIp" : "" }

            #record["ramdiskURL"] = ""
            #record["accountId"] = ""
            #record["kernelURL"] = ""
            #record["ramdiskId"] = ""
            #record["volumes"] = ""
            #record["launchIndex"] = 0
            #record["bundleTaskStateName"] = ""
            #record["reservationId"] = ""
            record["platform"] = self.platform
            record["euca_hostname"] = self.hostname
            record["euca_version"] = self.platform_version
            #record["state"] = "Teardown" # need to be changed
            if not "state" in record:
                record["state"] = "Teardown"
            record["state"] = self.convert_state(record["state"])
            print record
            break
            records.append(record)

        self.records = records

    def convert_state(self, state):
        if self.platform == "openstack":
            if state == "active":
                return "Extant"
            elif state == "building":
                return "Pending"
            elif state == "deleted" or "shutoff":
                return "Teardown"
            elif state == "error":
                return state
        return state

    def write_db(self):

        for record in self.records:
            self.instances.eucadb._write(record)
                                        
    def set_parser(self):
        def_s_date = "19700101"
        def_e_date = "29991231"
        def_conf = "futuregrid.cfg"

        parser = argparse.ArgumentParser()
        parser.add_argument("-s", "--from", dest="s_date", default=def_s_date,
                help="Start date to begin parsing (type: YYYYMMDD)")
        parser.add_argument("-e", "--to", dest="e_date", default=def_e_date,
                help="End date to finish parsing (type: YYYYMMDD)")

        # sqlite3 for nimbus
        parser.add_argument("-i", "--file", dest="input_file",
                help="the sqlite3 filename with path (e.g. /home/metric/nimbus/alamo/alamo)")

        parser.add_argument("-p", "--platform", required=True,
                help="Cloud platform name, required. (e.g. nimbus, openstack, eucalyptus, etc)")
        parser.add_argument("-pv", "--platform_version",
                help="Cloud platform version. (e.g. 2.9 for nimbus, essex for openstack, and  2.0 or 3.1 for eucalyptus)")
        parser.add_argument("-n", "--hostname", required=True,
                help="Hostname of the cloud platform, required. (e.g., hotel, sierra, india, alamo, foxtrot)")
        parser.add_argument("--conf", dest="conf",
                help="The configuraton file of the FG Cloud Metrics (e.g. $HOME/.futuregrid/futuregrid.cfg)")

        # mysql for openstack
        parser.add_argument("-dbn", "--dbname_nova",
                help="Database of nova to use")
        parser.add_argument("-dbk", "--dbname_keystone",
                help="Database of keystone to use")
        parser.add_argument("-dh", "--dbhost",
                help="Connect to database host")
        parser.add_argument("-du", "--dbuser",
                help="User for login of database")
        parser.add_argument("-dp", "--dbpass",
                help="Password to use when connecting to database server")
        parser.add_argument("-dP", "--dbport", default=3306,
                help="Port number to use for connection or 3306 for default")

        self.parser = parser
        args = parser.parse_args()
        print args

        self.s_date = datetime.strptime(args.s_date, "%Y%m%d")
        self.e_date = datetime.strptime(args.e_date, "%Y%m%d")
        self.platform = args.platform
        try:
           
            self.dbname_nova = args.dbname_nova
            self.dbname_keystone = args.dbname_keystone
            self.dbhost = args.dbhost
            self.dbuser = args.dbuser
            self.dbpass = args.dbpass
            self.dbport = args.dbport

            abspath = os.path.abspath(args.input_file)
            filename = os.path.basename(abspath)
            filepath = os.path.dirname(abspath)
            self.filename = filename
            self.filepath = filepath
 
        except:
            if not self.check_platform():
                raise ValueError("missing args for (" + self.platform + ")")

        self.platform_version = args.platform_version
        self.hostname = args.hostname
        self.confname = self.set_instance_conf(args.conf)

    def set_instance_conf(self, confname=""):
        if confname and len(confname) > 0:
            self.instances.set_conf(confname)

def main():
    converter = FGConverter()
    converter.set_parser()
    converter.convert_to_fg()

if __name__ == "__main__":
    main()
