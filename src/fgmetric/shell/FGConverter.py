import argparse
import os
import sys
import sqlite3 as lite
import MySQLdb
from collections import deque
from datetime import datetime
from fgmetric.shell.FGConstants import FGConst
from fgmetric.shell.FGDatabase import FGDatabase
from fgmetric.util.FGUtility import FGUtility


class FGConverter:

    # future = instances.in_the_future
    # past = instances.in_the_past

    s_date = None
    e_date = None

    platform = None
    platform_version = None
    hostname = None
    confname = None
    dbname_nova = None
    dbname_keystone = None

    query = None
    rows = None  # from database
    records = None  # for fg database

    userinfo = None
    cloudplatform = None

    argparser = None

    def __init__(self):
        self.db = FGDatabase()
        self.db_dest = FGDatabase()

    def __del__(self):
        self.db_close()

    def convert_to_fg(self):
        self.check_platform()
        self.db_connect()
        self.convert_instance()
        self.convert_userinfo()
        self.db_close()

    def check_platform(self):
        _check = getattr(self, "_check_platform_" + self.platform)
        _check()

    def _check_platform_nimbus(self):

        self.platform_version = self.platform_version or FGConst.DEFAULT_NIMBUS_VERSION
        self.db.db_type = self.db.db_type or FGConst.DEFAULT_NIMBUS_DB

        # this query is for sqlite3 because [timestamp] is only used on
        # sqlite3?
        self.query = 'SELECT t1.time as "t_start [timestamp]",\
                    t3.time as "t_end [timestamp]",\
                    t1.uuid as instanceId,\
                    t2.dn,\
                    t1.cpu_count as ccvm_cores,\
                    t1.memory as ccvm_mem,\
                    t1.vmm as serviceTag \
                    from create_events t1, user t2, remove_events t3 \
                    on t1.user_id=t2.id and t1.uuid=t3.uuid \
                    where t1.time >= \'' + str(self.s_date) + '\' and t3.time <= \'' + str(self.e_date) + '\''

    def _check_platform_openstack(self):

        if not self.dbname_nova or not self.dbname_keystone or not self.db.dbhost or not self.db.dbuser or not self.db.dbpasswd:
            msg = "db info is missing"
            print msg
            raise ValueError(msg)

        self.platform_version = self.platform_version or FGConst.DEFAULT_OPENSTACK_VERSION
        self.db.db_type = self.db.db_type or FGConst.DEFAULT_OPENSTACK_DB
        self.db.dbname = self.dbname_nova

        self.query = 'SELECT created_at as trace_pending_start, \
                    launched_at as trace_extant_start,\
                    terminated_at as trace_teardown_start, \
                    deleted_at as trace_teardown_stop, \
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
                    created_at as t_start,  \
                    COALESCE(deleted_at, terminated_at, updated_at) as t_end, \
                    uuid as instanceId, \
                    access_ip_v4 as ccnet_publicIp,\
                    ephemeral_gb as ccvm_disk \
                    from instances \
                    where updated_at >= \'' + str(self.s_date) + '\' and updated_at <= \'' + str(self.e_date) + '\''
        # COALESCE(launched_at, created_at, scheduled_at) as t_start, \

    def db_connect(self):
        self.db.connect()
        self.db_dest.conf()
        self.db_dest.connect()

    def db_close(self):
        self.db.close()
        self.db_dest.close()

    def read_from_source(self):
        self.rows = self.db.query(self.query)

    def write_to_dest(self):
        self.db_dest.write_instance(self.records)

    def convert_instance(self):
        self.read_from_source()
        self.map_to_fg()
        self.write_to_dest()

    def convert_userinfo(self):
        _convert = getattr(self, "_convert_userinfo_of_" + self.platform)
        _convert()

    def _convert_userinfo_of_nimbus(self):
        return

    def _convert_userinfo_of_openstack(self):
        res = self._read_userinfo_of_nova_with_project_info()
        self.db_dest.write_userinfo(res)

    def _read_userinfo_of_nova_with_project_info(self):
        keystone = self.db
        keystone.dbname = self.dbname_keystone
        keystone.connect()
        userinfo = keystone.query("select user_id, tenant_id, user.name as user_name, tenant.name as tenant_name \
                from user_tenant_membership, tenant, user \
                where user.id=user_tenant_membership.user_id \
                and tenant.id=user_tenant_membership.tenant_id")  # select id, name from user")
        keystone.close()
        records = []
        for row in userinfo:
            try:
                res = FGUtility.retrieve_userinfo_ldap(row["user_name"])
                if not res:
                    res = {}
                res["ownerid"] = row["user_id"]
                res["username"] = row["user_name"]
                res["project"] = row["tenant_name"]
                res["hostname"] = self.hostname
                print res
                records.append(res)
            except:
                print sys.exc_info()
                raise
        return records

    def read_cloudplatform(self):
        if self.cloudplatform:
            return
        self.cloudplatform = self.db_dest.read_cloudplatform()

    def get_cloudplatform_id(self, querydict={}):
        class ContinueOutOfALoop(Exception):
            pass
        self.read_cloudplatform()
        for row in self.cloudplatform:
            try:
                for key in querydict:
                    if row[key] != querydict[key]:
                        raise ContinueOutOfALoop
                return row["cloudPlatformId"]
            except ContinueOutOfALoop:
                continue
        return None

    def map_to_fg(self):
        rows = self.rows
        records = []

        whereclause = {"platform": self.platform, "hostname":
                       self.hostname, "version": self.platform_version}
        cloudplatformid = self.get_cloudplatform_id(whereclause)

            # 1. draw mapping table between openstack 'instances' and fg 'instance' table.
            # 2. define each column to know what exactly it means
            # 3. leave comments for missing and skipped columns
            # 4. check search options to see it is validate

        for row in rows:
            record = row

            try:
                record["instanceId"] = record["instanceId"][:15]
                record["ts"] = record["t_start"]
                # record["calltype"] = ""
                # record["userData"] = ""
                # record["kernelId"] = ""
                # record["emiURL"] = ""
                # record["t_start"] = row["t_start"]
                # record["t_end"] = row["t_end"]
                if record["t_end"] and record["t_start"]:
                    record["duration"] = (record[
                                          "t_end"] - record["t_start"]).total_seconds()
                # record["trace"] = {
                #    "pending" : { "start" : self.future, "stop" : self.past, "queue" : deque("",10)},
                #    "extant" : { "start" : self.future, "stop" : self.past, "queue" : deque("",10)},
                #    "teardown" : { "start" : self.future, "stop" : self.past, "queue" : deque("",10)}
                #    }
                # record["serviceTag"] = row["serviceTag"] or ""
                # record["groupNames"] = ""
                # record["keyName"] = ""
                # record["msgtype"] = ""
                # record["volumesSize"] = 0.0
                # record["linetype"] = ""
                if "dn" in record and not "ownerId" in record:
                    if len(record["dn"].split("CN=")) > 1:
                        record["ownerId"] = record["dn"].split("CN=")[1]
                    else:
                        record["ownerId"] = record["dn"]
                try:
                    del record["dn"]
                except:
                    pass
                record["date"] = record["t_start"]
                # record["id"] = 0
                # record["ncHostIdx"] = 0
                # record["ccvm"] = { "mem" : record["ccvm_mem"], "cores" : record["ccvm_cores"], "disk" : record[0 }
                # if "ccvm_disk" in row:
                #    record["ccvm"]["disk"] = row["ccvm_disk"]
                # if "emiId" in row:
                #    record["emiId"] = row["emiId"]
                # else:
                #    record["emiId"] = ""
                # record["ccnet"] = { "publicIp" : "", "privateMac" : "",
                # "networkIndex" : "", "vlan" : "", "privateIp" : "" }

                # record["ramdiskURL"] = ""
                # record["accountId"] = ""
                # record["kernelURL"] = ""
                # record["ramdiskId"] = ""
                # record["volumes"] = ""
                # record["launchIndex"] = 0
                # record["bundleTaskStateName"] = ""
                # record["reservationId"] = ""
                record["platform"] = self.platform
                # record["euca_hostname"] = self.hostname
                # record["euca_version"] = self.platform_version
                # record["state"] = "Teardown" # need to be changed
                if not "state" in record:
                    record["state"] = "Teardown"
                record["state"] = self.convert_state(record["state"])
                record["cloudPlatformIdRef"] = cloudplatformid
                records.append(record)
            except:
                print sys.exc_info()
                print record
                pass

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

    def set_instance_conf(self, confname=""):
        if confname and len(confname) > 0:
            self.db_dest.set_conf(confname)
            self.db_dest.update_conf()

    def set_parser(self):
        def_s_date = "19700101"
        def_e_date = "29991231"
        def_conf = "futuregrid.cfg"
        def_nova = "nova"
        def_keystone = "keystone"
        def_db = "mysql"

        parser = argparse.ArgumentParser()
        parser.add_argument("-s", "--from", dest="s_date", default=def_s_date,
                            help="Start date to begin parsing (type: YYYYMMDD)")
        parser.add_argument("-e", "--to", dest="e_date", default=def_e_date,
                            help="End date to finish parsing (type: YYYYMMDD)")

        parser.add_argument("-p", "--platform", required=True,
                            help="Cloud platform name, required. (e.g. nimbus, openstack, eucalyptus, etc)")
        parser.add_argument("-pv", "--platform_version",
                            help="Cloud platform version. (e.g. 2.9 for nimbus, essex for openstack, and  2.0 or 3.1 for eucalyptus)")
        parser.add_argument("-n", "--hostname", required=True,
                            help="Hostname of the cloud platform, required. (e.g., hotel, sierra, india, alamo, foxtrot)")
        parser.add_argument("--conf", dest="conf",
                            help="futuregrid.cfg filepath (e.g. $HOME/.futuregrid/futuregrid.cfg)")

        parser.add_argument("-db", "--database", default=def_db,
                            help="database type to load (e.g. mysql or sqlite3)")

        # sqlite3 for nimbus
        parser.add_argument("-i", "--file", dest="input_file",
                            help="the sqlite3 filename with path (e.g. /home/metric/nimbus/alamo/alamo)")

        # mysql for openstack
        parser.add_argument("-dbn", "--dbname_nova", default=def_nova,
                            help="Database of nova to use")
        parser.add_argument("-dbk", "--dbname_keystone", default=def_keystone,
                            help="Database of keystone to use")
        parser.add_argument("-dh", "--dbhost",
                            help="Connect to database host")
        parser.add_argument("-du", "--dbuser",
                            help="User for login of database")
        parser.add_argument("-dp", "--dbpass",
                            help="Password to use when connecting to database server")
        parser.add_argument("-dP", "--dbport", default=3306,
                            help="Port number to use for connection or 3306 for default")

        args = parser.parse_args()
        print args

        try:

            self.s_date = datetime.strptime(args.s_date, "%Y%m%d")
            self.e_date = datetime.strptime(args.e_date, "%Y%m%d")
            self.platform = args.platform
            self.platform_version = args.platform_version
            self.hostname = args.hostname
            self.confname = self.set_instance_conf(args.conf)

            self.db.db_type = args.database
            self.dbname_nova = args.dbname_nova
            self.dbname_keystone = args.dbname_keystone
            self.db.dbhost = args.dbhost
            self.db.dbuser = args.dbuser
            self.db.dbpasswd = args.dbpass
            self.db.dbport = args.dbport

            self.db.set_sqlite3_file(args.input_file)

        except:
            pass  # print sys.exc_info()[0]

        self.argparser = parser


def main():
    converter = FGConverter()
    converter.set_parser()
    converter.convert_to_fg()

if __name__ == "__main__":
    main()
