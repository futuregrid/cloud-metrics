#!/usr/bin/env python

import pprint
import os
import ConfigParser
import MySQLdb
import hashlib
import argparse
import sys

pp = pprint.PrettyPrinter(indent=0)
    
class FGEucaMetricsDB(object):

    # Initialize
    def __init__(self, configfile="futuregrid.cfg"):

        #read config from file configfile
        config = ConfigParser.ConfigParser()
        #cfgfile = os.path.dirname(os.path.abspath(__file__)) + "/" + configfile
        cfgfile = os.getenv("HOME") + "/.futuregrid/" + configfile
        config.read(cfgfile)

        #db parameters
        try:
            dbhost = config.get('EucaLogDB', 'host')
            dbport = int(config.get('EucaLogDB', 'port'))
            dbuser = config.get('EucaLogDB', 'user')
            dbpasswd = config.get('EucaLogDB', 'passwd')
            dbname = config.get('EucaLogDB', 'db')
        except ConfigParser.NoSectionError:
            print cfgfile + " does not exist"
            sys.exit()

	#table 
	self.tablename = "instance" #default table

        #connect to db
        self.conn = MySQLdb.connect (dbhost, dbuser, dbpasswd, dbname, dbport)
        self.cursor = self.conn.cursor (MySQLdb.cursors.DictCursor)
        
        #create table if not exist
        createTb = "create table if not exists instance (\
                    uidentifier VARCHAR(32) PRIMARY KEY NOT NULL, \
                    instanceId VARCHAR(16), \
                    ts DATETIME, \
                    calltype VARCHAR(32), \
                    userData VARCHAR(32), \
                    kernelId VARCHAR(32), \
                    emiURL VARCHAR(128), \
                    t_start DATETIME, \
                    t_end DATETIME, \
                    duration FLOAT, \
                    trace_pending_start DATETIME, \
                    trace_pending_stop DATETIME, \
                    trace_extant_start DATETIME, \
                    trace_extant_stop DATETIME, \
                    trace_teardown_start DATETIME, \
                    trace_teardown_stop DATETIME, \
                    serviceTag VARCHAR(128), \
                    groupNames VARCHAR(64), \
                    keyName VARCHAR(512), \
                    msgtype VARCHAR(16), \
                    volumesSize FLOAT, \
                    linetype VARCHAR(32), \
                    ownerId VARCHAR(32), \
                    date DATETIME, \
                    id INT, \
                    ncHostIdx INT, \
                    ccvm_mem INT, \
                    ccvm_cores INT, \
                    ccvm_disk INT, \
                    emiId VARCHAR(32), \
                    ccnet_publicIp VARCHAR(32), \
                    ccnet_privateMac VARCHAR(32), \
                    ccnet_networkIndex VARCHAR(32), \
                    ccnet_vlan VARCHAR(32), \
                    ccnet_privateIp VARCHAR(32), \
                    ramdiskURL VARCHAR(128), \
                    state VARCHAR(16), \
                    kernelURL VARCHAR(128), \
                    ramdiskId VARCHAR(32), \
                    volumes VARCHAR(32), \
                    launchIndex INT, \
                    reservationId VARCHAR(32) )"
        try:
            pass#self.cursor.execute(createTb)
        except MySQLdb.Error:
            pass
        #print "initilized!"

    # destructor
    def __del__(self):
        try:
            self.cursor.close()
            self.conn.close()
        except:
            pass

    # help function to format values to be inserted into mysql db
    def _fmtstr(self, astr):
        #if(astr == ''):
        #    ret = 'NULL'
        #else:
        ret = "'" + astr + "'"
        return ret

    # read from the database.
    def read(self, querydict={}, optional=""):
        querystr = "";
        if querydict:
            for key in querydict:
                value = querydict[key]
                astr = key + "='" + value + "'"
                if querystr != "":
                    querystr += " and "
                querystr += astr            
                print "qstr:->" + querystr + "<---"
                rquery = "SELECT * FROM " + self.tablename + " where " + querystr + optional
        else:
            rquery = "SELECT * from " + self.tablename + optional
            
        self.cursor.execute(rquery)
        rows = self.cursor.fetchall()
        multikeys = ["trace", "ccvm", "ccnet"]
        listvalues = ["groupNames", "volumes"]
        lrows = list(rows)
        ret = []
        for arow in lrows:
            rowret = {}
            for key in arow:
                keys = key.rsplit("_")
                if keys[0] in multikeys:
                    self._assignVal2Multi(rowret, keys, arow[key])
                elif key in listvalues:
                    if not arow[key] is None:
                        values = arow[key].rsplit(" ")
                        rowret[key] = values
                    else:
                        rowret[key] = []
                else:
                    rowret[key] = arow[key]
            ret.append(rowret)
        return ret

    def delete(self, querydict={}):
        querystr = "";
        if querydict:
            for key in querydict:
                value = querydict[key]
                astr = key + "='" + value + "'"
                if querystr != "":
                    querystr += " and "
                querystr += astr            
                rquery = "delete FROM " + self.tablename + " where " + querystr
        else:
            rquery = "delete from " + self.tablename
        
	try:
		self.cursor.execute(rquery)
        except MySQLdb.Error:
		pass
        return 0
        
        
    # help function to initialize(if necessary) and assign value to nested dict
    def _assignVal2Multi(self, themulti, keys, value=None):
        tolevel = len(keys) - 1
        curlevel = 0
        nextlevel = curlevel + 1
        if not themulti.has_key(keys[curlevel]):
            themulti[keys[curlevel]] = {}
        cur = themulti[keys[curlevel]]
        while nextlevel < tolevel:
            if not cur.has_key(keys[nextlevel]):
                cur[keys[nextlevel]] = {}
            cur = cur[keys[nextlevel]]
            curlevel += 1
            nextlevel += 1

        cur[keys[nextlevel]] = value
        return cur

    def value_todate(self,string):
        return datetime.strptime(string, '%Y-%m-%d %H:%M:%S')

    # write instance object into db
    def write(self, entryObj):
        print entryObj
        uidcat = entryObj["instanceId"] + " - " + str(entryObj["ts"])
        m = hashlib.md5()
        m.update(uidcat)
        uid = m.hexdigest()
        pp.pprint(entryObj)
        wquery = "INSERT INTO instance( uidentifier, \
                                    instanceId, \
                                    ts, \
                                    calltype, \
                                    userData, \
                                    kernelId, \
                                    emiURL, \
                                    t_start, \
                                    t_end, \
                                    duration, \
                                    trace_pending_start, \
                                    trace_pending_stop, \
                                    trace_extant_start, \
                                    trace_extant_stop, \
                                    trace_teardown_start, \
                                    trace_teardown_stop, \
                                    serviceTag, \
                                    groupNames, \
                                    keyName, \
                                    msgtype, \
                                    volumesSize, \
                                    linetype, \
                                    ownerId, \
                                    date, \
                                    id, \
                                    ncHostIdx, \
                                    ccvm_mem, \
                                    ccvm_cores, \
                                    ccvm_disk, \
                                    emiId, \
                                    ccnet_publicIp, \
                                    ccnet_privateMac, \
                                    ccnet_networkIndex, \
                                    ccnet_vlan, \
                                    ccnet_privateIp, \
                                    ramdiskURL, \
                                    state, \
                                    kernelURL, \
                                    ramdiskId, \
                                    volumes, \
                                    launchIndex, \
                                    reservationId) \
                            VALUES (" \
                                    + self._fmtstr(uid) + "," \
                                    + self._fmtstr(entryObj["instanceId"]) + "," \
                                    + self._fmtstr(str(entryObj["ts"])) + "," \
                                    + self._fmtstr(entryObj["calltype"]) + "," \
                                    + self._fmtstr(entryObj["userData"]) + "," \
                                    + self._fmtstr(entryObj["kernelId"]) + "," \
                                    + self._fmtstr(entryObj["emiURL"]) + "," \
                                    + self._fmtstr(str(entryObj["t_start"])) + "," \
                                    + self._fmtstr(str(entryObj["t_end"])) + "," \
                                    + str(entryObj["duration"]) + "," \
                                    + self._fmtstr(str(entryObj["trace"]["pending"]["start"])) + "," \
                                    + self._fmtstr(str(entryObj["trace"]["pending"]["stop"])) + "," \
                                    + self._fmtstr(str(entryObj["trace"]["extant"]["start"])) + "," \
                                    + self._fmtstr(str(entryObj["trace"]["extant"]["stop"])) + "," \
                                    + self._fmtstr(str(entryObj["trace"]["teardown"]["start"])) + "," \
                                    + self._fmtstr(str(entryObj["trace"]["teardown"]["stop"])) + "," \
                                    + self._fmtstr(entryObj["serviceTag"]) + "," \
                                    + self._fmtstr(" ".join(entryObj["groupNames"])) + "," \
                                    + self._fmtstr(entryObj["keyName"]) + "," \
                                    + self._fmtstr(entryObj["msgtype"]) + "," \
                                    + str(entryObj["volumesSize"]) + "," \
                                    + self._fmtstr(entryObj["linetype"]) + "," \
                                    + self._fmtstr(entryObj["ownerId"]) + "," \
                                    + self._fmtstr(str(entryObj["date"])) + "," \
                                    + str(entryObj["id"]) + "," \
                                    + str(entryObj["ncHostIdx"]) + "," \
                                    + str(entryObj["ccvm"]["mem"]) + "," \
                                    + str(entryObj["ccvm"]["cores"]) + "," \
                                    + str(entryObj["ccvm"]["disk"]) + "," \
                                    + self._fmtstr(entryObj["emiId"]) + "," \
                                    + self._fmtstr(entryObj["ccnet"]["publicIp"]) + "," \
                                    + self._fmtstr(entryObj["ccnet"]["privateMac"]) + "," \
                                    + self._fmtstr(entryObj["ccnet"]["networkIndex"]) + "," \
                                    + self._fmtstr(entryObj["ccnet"]["vlan"]) + "," \
                                    + self._fmtstr(entryObj["ccnet"]["privateIp"]) + "," \
                                    + self._fmtstr(entryObj["ramdiskURL"]) + "," \
                                    + self._fmtstr(entryObj["state"]) + "," \
                                    + self._fmtstr(entryObj["kernelURL"]) + "," \
                                    + self._fmtstr(entryObj["ramdiskId"]) + "," \
                                    + self._fmtstr(" ".join(entryObj["volumes"])) + "," \
                                    + str(entryObj["launchIndex"]) + "," \
                                    + self._fmtstr(entryObj["reservationId"]) + ")"
        #print wquery
        try:
            self.cursor.execute(wquery)
        except MySQLdb.Error:
            pass

    # Change table 
    def change_table(self, table_name):
	    self.tablename=table_name
	    return

# testing
def testing():
    tstobj = '{\
        "calltype": "refresh_instances",\
        "userData": "",\
        "kernelId": "eki-78EF12D2",\
        "emiURL": "http://149.165.146.135:8773/services/Walrus/centos53/centos.5-3.x86-64.img.manifest.xml",\
        "trace": {\
            "teardown": {\
                "start": "2011-11-10 09:28:30",\
                "stop": "2011-11-10 09:31:21"\
            },\
            "extant": {\
                "start": "2011-11-10 09:28:30",\
                "stop": "2011-11-10 09:28:30"\
            },\
            "pending": {\
                "start": "2011-11-10 09:28:30",\
                "stop": "2011-11-10 09:28:30"\
            }\
        },\
        "serviceTag": "http://i10:8775/axis2/services/EucalyptusNC",\
        "instanceId": "i-534109B6",\
        "duration": "9.0",\
        "t_start": "2011-11-10 09:28:21",\
        "ts": "2011-11-10 09:28:21",\
        "groupNames": [\
            "default"\
        ],\
        "keyName": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCTu5lGYZr/XvkXlPW7d+/VKaZgaCb/n19uY9bZcGT7e7jshGjEUjVrhgNs7+fukoOLmwWDdg42KjyNf3P4W1O5AXdtpxQMNgCvjcv7joRjbBg8O7SE31uPvvy+ih8r/SBueAiRvzHDKPK5XV+H3v2V22302CkEt0V5YQSx6q1yGQOKhU7jCsK68dgguBaubf4N90G2UzvUFf1UAUocX80JSq/b3cH5/myEQqndazm/H3fMoBrUpn/GUvuyfeKlcbGct3Ho0eMQCrkKKRYsru/IdTqZhPGCYQPWUdR2mH9SD8QDpGdV9GOpIquTZqXhlIUKE7TNmLCoFZ9SOm3/tCGx admin@eucalyptus",\
        "msgtype": "EUCADEBUG ",\
        "volumesSize": "0",\
        "linetype": "print_ccInstance",\
        "ownerId": "admin",\
        "date": "2011-11-10 09:28:30",\
        "id": "011265",\
        "t_end": "2011-11-10 09:28:30",\
        "ncHostIdx": "8",\
        "ccvm": {\
            "mem": "512",\
            "cores": "1",\
            "disk": "5"\
        },\
        "emiId": "emi-0B951139",\
        "ccnet": {\
            "publicIp": "149.165.159.130",\
            "privateMac": "D0:0D:53:41:09:B6",\
            "networkIndex": "4",\
            "vlan": "10",\
            "privateIp": "10.0.2.4"\
        },\
        "ramdiskURL": "http://149.165.146.135:8773/services/Walrus/xeninitrd/initrd-2.6.27.21-0.1-xen.manifest.xml",\
        "state": "Teardown",\
        "kernelURL": "http://149.165.146.135:8773/services/Walrus/xenkernel/vmlinuz-2.6.27.21-0.1-xen.manifest.xml",\
        "ramdiskId": "eri-5BB61255",\
        "volumes": [\
            ""\
        ],\
        "launchIndex": "0",\
        "reservationId": "r-3DE7089D"\
        }'
    tstobj2 = '{\
        "calltype": "refresh_instances",\
        "userData": "",\
        "kernelId": "eki-78EF12D2",\
        "emiURL": "http://149.165.146.135:8773/services/Walrus/centos53/centos.5-3.x86-64.img.manifest.xml",\
        "trace": {\
            "teardown": {\
                "start": "2011-11-10 09:28:30",\
                "stop": "2011-11-10 09:31:21"\
            },\
            "extant": {\
                "start": "2011-11-10 09:28:30",\
                "stop": "2011-11-10 09:28:30"\
            },\
            "pending": {\
                "start": "2011-11-10 09:28:30",\
                "stop": "2011-11-10 09:28:30"\
            }\
        },\
        "serviceTag": "http://i10:8775/axis2/services/EucalyptusNC",\
        "instanceId": "i-534109B9",\
        "duration": "9.0",\
        "t_start": "2011-11-10 09:28:21",\
        "ts": "2011-11-10 09:28:21",\
        "groupNames": [\
            "default",\
            "admin"\
        ],\
        "keyName": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCTu5lGYZr/XvkXlPW7d+/VKaZgaCb/n19uY9bZcGT7e7jshGjEUjVrhgNs7+fukoOLmwWDdg42KjyNf3P4W1O5AXdtpxQMNgCvjcv7joRjbBg8O7SE31uPvvy+ih8r/SBueAiRvzHDKPK5XV+H3v2V22302CkEt0V5YQSx6q1yGQOKhU7jCsK68dgguBaubf4N90G2UzvUFf1UAUocX80JSq/b3cH5/myEQqndazm/H3fMoBrUpn/GUvuyfeKlcbGct3Ho0eMQCrkKKRYsru/IdTqZhPGCYQPWUdR2mH9SD8QDpGdV9GOpIquTZqXhlIUKE7TNmLCoFZ9SOm3/tCGx admin@eucalyptus",\
        "msgtype": "EUCADEBUG ",\
        "volumesSize": "0",\
        "linetype": "print_ccInstance",\
        "ownerId": "admin",\
        "date": "2011-11-10 09:28:30",\
        "id": "011265",\
        "t_end": "2011-11-10 09:28:30",\
        "ncHostIdx": "8",\
        "ccvm": {\
            "mem": "512",\
            "cores": "1",\
            "disk": "5"\
        },\
        "emiId": "emi-0B951139",\
        "ccnet": {\
            "publicIp": "149.165.159.130",\
            "privateMac": "D0:0D:53:41:09:B6",\
            "networkIndex": "4",\
            "vlan": "10",\
            "privateIp": "10.0.2.4"\
        },\
        "ramdiskURL": "http://149.165.146.135:8773/services/Walrus/xeninitrd/initrd-2.6.27.21-0.1-xen.manifest.xml",\
        "state": "Teardown",\
        "kernelURL": "http://149.165.146.135:8773/services/Walrus/xenkernel/vmlinuz-2.6.27.21-0.1-xen.manifest.xml",\
        "ramdiskId": "eri-5BB61255",\
        "volumes": [\
            ""\
        ],\
        "launchIndex": "0",\
        "reservationId": "r-3DE7089D"\
        }'
    testobj = eval(tstobj)
    testobj2 = eval(tstobj2)
    #print testobj
    eucadb = FGEucaMetricsDB("futuregrid.cfg.local")
    eucadb.write(testobj)
    eucadb.write(testobj2)
    keys = ["instanceId", "ownerId"]
    values = ["i-534109B9", "admin"]
    #if len(keys) > 1:
    qdict = dict(zip(keys,values))
    #else:
    #    qdict = {keys[0]: values[0]}
    #print qdict
    records = eucadb.read(qdict)
    print records
    print records[0]["instanceId"]
    print records[0]["trace"]["teardown"]["start"]
    print records[0]["trace"]["teardown"]["stop"]
    #if len(records) > 0:
    #    for record in records:
    #        print record
    #        #print "%s %s %s" % (record["instanceId"], record["ownerId"], record["ts"])
    #else:
    #    print "no records found"
    #var = {}
    #keys = ["l1", "l21", "l31"]
    #eucadb._assignVal2Multi(var, keys)
    #print var
    #keys = ["l1", "l22", "l31"]
    #eucadb._assignVal2Multi(var, keys)
    #print var
    #keys = ["l1", "l22", "l32"]
    #print eucadb._assignVal2Multi(var, keys, "value")
    #print var
# main invokation

def command_clean_database():
    """
    MANUAL PAGE DRAFT

    NAME - fg-cleanup-table

    DESCRIPTION

    usage
	fg-cleanup-db <arguments>

    fg-cleanup-db

	-t tbl_name
	   deletes rows from tbl_name

	-d db_name
	   a database name of a table specified by -t tbl_name

	-w where_condition (optional)
	   specifies the conditions that identify which rows to delete

	--conf filename
	   configuraton file of the database to be used. The configuration file has the following format
	   
	   [EucaLogDB]
	   host=HOST
	   port=PORT
	   user=USER
	   passwd=PASS
	   db=DB
	   
	   if this parameter is not specified and a database is used the default location for this file is in
	   
	   ~/.futuregrid/futuregrid.cfg

    """
    def_table = "instance"
    def_db = "euca"
    def_conf = "futuregrid.cfg.local"

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", dest="table_name", default=def_table,
			help="table name to delete")
    parser.add_argument("-d", dest="db_name", default=def_db,
			help="db name")
    parser.add_argument("-w", dest="where_clause",
			help="WHERE clauses")
    parser.add_argument("-C", "--conf", dest="conf", default=def_conf,
			help="configuraton file of the database to be used")
    args = parser.parse_args()

    eucadb = FGEucaMetricsDB(args.conf)
    eucadb.change_table(args.table_name)

    # where_clause need to be query dict type 
    query_dict=""
    ret = eucadb.delete(query_dict)


if __name__ == '__main__':
    command_clean_database()
