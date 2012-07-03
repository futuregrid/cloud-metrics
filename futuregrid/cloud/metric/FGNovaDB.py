#!/usr/bin/env python

import os
import ConfigParser
import MySQLdb
import sys

class NovaDB(object):

    instances_table = "instances"

    def __init__(self, configfile="futuregrid.cfg"):

        #read config from file configfile
        config = ConfigParser.ConfigParser()
        cfgfile = os.getenv("HOME") + "/.futuregrid/" + configfile
        config.read(cfgfile)

        try:
            dbhost = config.get('NovaDB', 'host')
            dbport = int(config.get('NovaDB', 'port'))
            dbuser = config.get('NovaDB', 'user')
            dbpasswd = config.get('NovaDB', 'passwd')
            dbname = config.get('NovaDB', 'novadb')
            keystonedbname =config.get('NovaDB', 'keystonedb')
        except ConfigParser.NoSectionError:
            print cfgfile + " does not exist"
            sys.exit()

        #connect to db
        self.conn = MySQLdb.connect (dbhost, dbuser, dbpasswd, dbname, dbport)
        self.cursor = self.conn.cursor (MySQLdb.cursors.DictCursor)
        
    def __del__(self):
        try:
            self.cursor.close()
            self.conn.close()
        except:
            pass

    # read from the database.
    def _read(self, tablename, querydict, optional=""):
        
        querystr = "";
        ret = []

        if querydict:
            for key in querydict:
                value = querydict[key]
                astr = key + "='" + value + "'"
                if querystr != "":
                    querystr += " and "
                querystr += astr            
                print "qstr:->" + querystr + "<---"
                rquery = "SELECT * FROM " + tablename + " where " + querystr + optional
        else:
            rquery = "SELECT * from " + tablename + optional
           
        try:
            self.cursor.execute(rquery)
        except MYSQLdb.Error:
            pass

        rows = self.cursor.fetchall()

        for arow in list(rows):
            ret.append(arow)
        return ret

    def read_instances(self, querydict={}):
        return self._read(self.instances_table, querydict)

    def value_todate(self,string):
        return datetime.strptime(string, '%Y-%m-%d %H:%M:%S')
