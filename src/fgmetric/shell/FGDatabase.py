import os
import sys
import ConfigParser
import hashlib
import MySQLdb
import sqlite3
import pprint
from datetime import datetime
from fgmetric.shell.FGConstants import FGConst


class FGDatabase:

    instance_table = "instance"
    userinfo_table = "userinfo"
    cloudplatform_table = "cloudplatform"
    projectinfo_table = "projectinfo"
    column_cp_ins = "cloudPlatformIdRef"
    column_cp_cp = "cloudPlatformId"

    conn = None
    cursor = None

    query = None

    pp = pprint.PrettyPrinter(indent=0)

    def __init__(self):
        self.config_filename = FGConst.DEFAULT_CONFIG_FILENAME
        self.config_filepath = FGConst.DEFAULT_CONFIG_FILEPATH
        self.db_type = "mysql"

    def __del__(self):
        self.close()

    def conf(self):
        config = ConfigParser.ConfigParser()
        config.read(self.get_config_file())

        try:
            self.dbhost = config.get('CloudMetricsDB', 'host')
            self.dbport = int(config.get('CloudMetricsDB', 'port'))
            self.dbuser = config.get('CloudMetricsDB', 'user')
            self.dbpasswd = config.get('CloudMetricsDB', 'passwd')
            self.dbname = config.get('CloudMetricsDB', 'db')
        except ConfigParser.NoSectionError:
            try:
                self.dbhost = config.get('EucaLogDB', 'host')
                self.dbport = int(config.get('EucaLogDB', 'port'))
                self.dbuser = config.get('EucaLogDB', 'user')
                self.dbpasswd = config.get('EucaLogDB', 'passwd')
                self.dbname = config.get('EucaLogDB', 'db')
            except ConfigParser.NoSectionError:
                raise

    def set_conf(self, input_file):

        try:
            if os.path.dirname(input_file):
                abspath = os.path.abspath(input_file)
                self.config_filepath = os.path.dirname(abspath)
            self.config_filename = os.path.basename(input_file)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise

    def update_conf(self):
        self.conf()

    def get_config_file(self):
        return self.config_filepath + "/" + self.config_filename

    def set_sqlite3_file(self, input_file):
        try:
            abspath = os.path.abspath(input_file)
            self.sqlite3_filename = os.path.basename(abspath)
            self.sqlite3_filepath = os.path.dirname(abspath)
        except:
            pass

    def get_sqlite3_file(self):
        return self.sqlite3_filepath + "/" + self.sqlite3_filename

    def connect(self):
        conn_database = getattr(self, "_connect_" + self.db_type)
        conn_database()

    def _connect_mysql(self):
        try:
            self.conn = MySQLdb.connect(
                self.dbhost, self.dbuser, self.dbpasswd, self.dbname, self.dbport)  # , cursorclass=MySQLdb.cursors.DictCursor)
            self.cursor = self.conn.cursor(
                cursorclass=MySQLdb.cursors.DictCursor)
        except MySQLdb.Error as e:
            print "Error %s:" % e.args[0]
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise

    def _connect_sqlite3(self):

        def dict_factory(cursor, row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d

        try:
            conn = sqlite3.connect(
                self.get_sqlite3_file(), detect_types=sqlite3.PARSE_COLNAMES)
            conn.row_factory = dict_factory  # lite.Row
            conn.text_factory = str
            self.conn = conn
            self.cursor = self.conn.cursor()
        except sqlite3.Error, e:
            print "Error %s:" % e.args[0]

    def close(self):
        # if self.cursor:
        #    self.cursor.close()
        if self.conn and self.conn.open:
            self.conn.close()

    '''
    def select(self):
    def insert(self):
    def alter(self):
    def delete(self):
    '''

    def read(self, querydict={}, optional=""):
        ''' read from the database '''

        foreign_key_for_cloudplatform = self.instance_table + "." + \
            self.column_cp_ins + "=" + \
            self.cloudplatform_table + "." + self.column_cp_cp
        querystr = ""
        if querydict:
            for key in querydict:
                value = querydict[key]
                astr = key + "='" + value + "'"
                if querystr != "":
                    querystr += " and "
                querystr += astr
                rquery = "SELECT * FROM " + self.instance_table + "," + self.cloudplatform_table + \
                    " where " + foreign_key_for_cloudplatform + \
                    " and " + querystr + optional
                # rquery = "select * from instance, cloudplatform  where
                # instance.cloudPlatform=cloudplatform.cloudPlatformId limit
                # 5";
        else:
            '''
            rquery = "SELECT uidentifier, t_start, t_end, duration, serviceTag, ownerId, ccvm_mem, ccvm_cores, ccvm_disk, hostname, " + self.cloudplatform_table + ".platform, \
                    trace_pending_start, trace_pending_stop,\
                    trace_extant_start, trace_extant_stop,\
                    trace_teardown_start, trace_teardown_stop,\
                    state, date \
            '''
            rquery = "select * \
                    from " + self.instance_table + "," + self.cloudplatform_table + " where " + foreign_key_for_cloudplatform + " " + optional
        self.cursor.execute(rquery)
        rows = self.cursor.fetchall()
        multikeys = ["trace", "ccvm"]  # , "ccnet"]
        # listvalues = ["groupNames", "volumes"]
        ret = []
        for arow in rows:
            rowret = {}
            for key in arow:
                keys = key.rsplit("_")
                if keys[0] in multikeys:
                    self._assignVal2Multi(rowret, keys, arow[key])
                    '''
                    elif key in listvalues:
                        if not arow[key] is None:
                            values = arow[key].rsplit(" ")
                            rowret[key] = values
                        else:
                            rowret[key] = []
                    '''
                else:
                    rowret[key] = arow[key]
            ret.append(rowret)
        return ret

    def _assignVal2Multi(self, themulti, keys, value=None):
        ''' help function to initialize(if necessary) and assign value to nested dict '''
        tolevel = len(keys) - 1
        curlevel = 0
        nextlevel = curlevel + 1
        if keys[curlevel] not in themulti:
            themulti[keys[curlevel]] = {}
        cur = themulti[keys[curlevel]]
        while nextlevel < tolevel:
            if keys[nextlevel] not in cur:
                cur[keys[nextlevel]] = {}
            cur = cur[keys[nextlevel]]
            curlevel += 1
            nextlevel += 1

        cur[keys[nextlevel]] = value
        return cur

    def _read(self, cursor, tablename, querydict, optional=""):
        return self._select(cursor=cursor, table=tablename, where=querydict,
                            optional=optional)

    def _select(self, *args, **kwargs):
        """select table with keyword arguments

            Expected keyword arguments:
                cursor=
                table=
                expr=
                where=
                optional=

            Args:
                *args : arguments
                **kwargs : keywords  
        
        """
        cursor = kwargs['cursor']
        tablename = kwargs['table']
        try:
            expr = kwargs['expr']
        except:
            expr = "*"
        try:
            querydict = kwargs['where']
        except:
            querydict = {}
        try:
            optional = kwargs['optional']
        except:
            optional = ""
        querystr = self._get_querystr(querydict)
        ret = []

        rquery = "SELECT " + expr + " FROM " + tablename + querystr + optional

        try:
            cursor.execute(rquery)
        except (MySQLdb.Error, sqlite3.Error) as e:
            print str(e)
            print sys.exc_info()
            pass
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise

        rows = cursor.fetchall()
        return rows

    def _get_querystr(self, querydict):
        querystr = ""
        for key in querydict:
            value = querydict[key]
            astr = key + "='" + value + "' "
            if querystr != "":
                querystr += " and "
            else:
                querystr = " where "
            querystr += astr

        return querystr

    def get_instance(self, querydict={}):
        return self.read_instance(querydict)

    def read_instance(self, querydict={}):
        return self._read(self.cursor, self.instance_table, querydict)

    def get_userinfo(self, querydict={}, optional=""):
        return self.read_userinfo(querydict, optional)

    def get_userinfo_detail(self):
        return self._select(cursor=self.cursor, table=self.userinfo_table, \
                            expr=" *, GROUP_CONCAT(distinct project) as \
                            projects, GROUP_CONCAT(distinct hostname) as \
                            hostnames ", where="", optional=" group by username ")

    def read_projectinfo(self, querydict={}):
        return self._read(self.cursor, self.projectinfo_table, querydict)

    def read_userinfo(self, querydict={}, optional=""):
        return self._read(self.cursor, self.userinfo_table, querydict, optional)

    def get_cloudplatform(self, querydict={}):
        return self.read_cloudplatform(querydict)

    def read_cloudplatform(self, querydict={}):
        return self._read(self.cursor, self.cloudplatform_table, querydict)

    def _delete(self, tablename, querydict):

        querystr = ""
        if querydict:
            for key in querydict:
                value = querydict[key]
                astr = key + "='" + value + "'"
                if querystr != "":
                    querystr += " and "
                querystr += astr
                rquery = "delete FROM " + tablename + " where " + querystr
        else:
            rquery = "delete from " + tablename

        try:
            self.cursor.execute(rquery)
        except (MySQLdb.Error, sqlite3.Error) as e:
            print str(e)
            pass
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise

    def delete_instance(self, querydict={}):
        self._delete(self.instance_table, querydict)

    def delete_userinfo(self, querydict={}):
        self._delete(self.userinfo_table, querydict)

    def write(self, entryObj):
        ''' write instance object into db '''
        # ts has small variation. we ignore seconds here to create index
        new_ts = datetime(entryObj["ts"].year, entryObj["ts"].month, entryObj[
                          "ts"].day, entryObj["ts"].hour, entryObj["ts"].minute, 0)
        uid = self._get_hash(entryObj[
                             "instanceId"] + " - " + str(new_ts))  # str(entryObj["ts"]))
        # self.pp.pprint(entryObj)
        wquery = "INSERT INTO " + self.instance_table + " ( uidentifier, \
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
                                    accountId, \
                                    kernelURL, \
                                    ramdiskId, \
                                    volumes, \
                                    launchIndex, \
                                    platform, \
                                    bundleTaskStateName, \
                                    reservationId, \
                                    cloudPlatformIdRef ) \
                            VALUES (" \
                                    + self._fmtstr(uid) + "," \
                                    + self._fmtstr(entryObj["instanceId"]) + "," \
                                    + self._fmtstr(str(entryObj["ts"])) + "," \
                                    + self._fmtstr(entryObj["calltype"]) + "," \
                                    + self._fmtstr(entryObj["userData"]) + "," \
                                    + self._fmtstr(self._fillempty(entryObj, "kernelId")) + "," \
                                    + self._fmtstr(self._fillempty(entryObj, "emiURL")) + "," \
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
                                    + self._fmtstr(self._fillempty(entryObj, "emiId")) + "," \
                                    + self._fmtstr(entryObj["ccnet"]["publicIp"]) + "," \
                                    + self._fmtstr(entryObj["ccnet"]["privateMac"]) + "," \
                                    + self._fmtstr(entryObj["ccnet"]["networkIndex"]) + "," \
                                    + self._fmtstr(entryObj["ccnet"]["vlan"]) + "," \
                                    + self._fmtstr(entryObj["ccnet"]["privateIp"]) + "," \
                                    + self._fmtstr(self._fillempty(entryObj, "ramdiskURL")) + "," \
                                    + self._fmtstr(entryObj["state"]) + "," \
                                    + self._fmtstr(self._fillempty(entryObj, "accountId")) + "," \
                                    + self._fmtstr(self._fillempty(entryObj, "kernelURL")) + "," \
                                    + self._fmtstr(self._fillempty(entryObj, "ramdiskId")) + "," \
                                    + self._fmtstr(" ".join(entryObj["volumes"])) + "," \
                                    + str(entryObj["launchIndex"]) + "," \
                                    + self._fmtstr(self._fillempty(entryObj, "platform")) + "," \
                                    + self._fmtstr(self._fillempty(entryObj, "bundleTaskStateName")) + "," \
                                    + self._fmtstr(entryObj["reservationId"]) + "," \
                                    + self._fmtstr(str(entryObj[
                                                   "cloudPlatformIdRef"])) + ")"

        wquery += " on duplicate key update " \
            + "t_end=" \
            + self._fmtstr(str(entryObj["t_end"])) + "," \
            + " duration=" \
            + str(entryObj["duration"]) + "," \
            + " trace_pending_start=LEAST(trace_pending_start, " \
            + self._fmtstr(str(entryObj["trace"]["pending"]["start"])) + ") ," \
            + " trace_pending_stop=GREATEST(trace_pending_stop, " \
            + self._fmtstr(str(entryObj["trace"]["pending"]["stop"])) + ") ," \
            + " trace_extant_start=LEAST(trace_extant_start, " \
            + self._fmtstr(str(entryObj["trace"]["extant"]["start"])) + ") ," \
            + " trace_extant_stop=GREATEST(trace_extant_stop, " \
            + self._fmtstr(str(entryObj["trace"]["extant"]["stop"])) + ") ," \
            + " trace_teardown_start=LEAST(trace_teardown_start, " \
            + self._fmtstr(str(entryObj["trace"]["teardown"]["start"])) + ") ," \
            + " trace_teardown_stop=GREATEST(trace_teardown_stop, " \
            + self._fmtstr(str(entryObj["trace"]["teardown"]["stop"])) + ") ," \
            + " date=" \
            + self._fmtstr(str(entryObj["date"])) + "," \
            + " state=" \
            + self._fmtstr(entryObj["state"])

        # print wquery
        try:
            self.cursor.execute(wquery)

        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            pass
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise

    def _get_hash(self, name):
        m = hashlib.md5()
        m.update(name)
        uid = m.hexdigest()
        return uid

    def write_instance(self, entryObj):
        if isinstance(entryObj, list):
            for entry in entryObj:
                try:
                    entry["uidentifier"] = self._get_hash(entry[
                                                          "instanceId"] + " - " + str(entry["ts"]))
                    self._write("instance", entry)
                except:
                    print sys.exc_info()
                    pass
        else:
            try:
                entryObj["uidentifier"] = self._get_hash(entryObj[
                                                         "instanceId"] + " - " + str(entryObj["ts"]))
                self._write("instance", entryObj)
            except:
                print sys.exc_info()
                pass

    def write_userinfo(self, entryObj):
        ''' write userinfo object into db '''
        if isinstance(entryObj, list):
            for entry in entryObj:
                self._write("userinfo", entry)
        else:
            self._write("userinfo", entryObj)

    def _write(self, tablename, entryObj):

        try:
            keys = ", ".join(entryObj.keys())
            values = "'" + "' ,'".join(str(x) for x in entryObj.values()) + "'"
            wquery = "INSERT INTO " + tablename + \
                " ( " + keys + " ) VALUES ( " + values + " )"
            # print wquery
            self.cursor.execute(wquery)

        except (MySQLdb.Error, sqlite3.Error) as e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            pass
        except AttributeError, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            pass
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise

    def query(self, query=None):
        try:
            query = query or self.query
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            return rows
        except (sqlite3.Error, MySQLdb.Error) as e:
            print "Error %s:" % e.args[0]
            pass

    def change_table(self, table_name):
        self.instance_table = table_name
        return

    def _fmtstr(self, astr):
        ret = "'" + astr + "'"
        return ret

    def _fillempty(self, entry, key):
        if not key in entry:
            return ""
        else:
            return entry[key]

    def convert_nested2list(self, nested, newkey):
        if not isinstance(nested, type({})):
            return {newkey[1:]: nested}
        for key in nested:
            return self.convert_nested2list(nested[key], newkey + "_" + key)
