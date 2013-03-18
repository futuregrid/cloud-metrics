#!/usr/bin/env python

import os
import ConfigParser
import MySQLdb
import sys

class FGNovaDB(object):

    instances_table = "instances" # in nova
    userinfo_table = "user" # in keystone

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

        self.conn_keystone = MySQLdb.connect (dbhost, dbuser, dbpasswd, keystonedbname, dbport)
        self.cursor_keystone = self.conn_keystone.cursor (MySQLdb.cursors.DictCursor)
        
    def __del__(self):
        try:
            self.cursor.close()
            self.conn.close()

            self.cursor_keystone.close()
            self.conn_keystone.close()

        except:
            pass

    def count(self):
        rquery = "select count(*) from " + self.instances_table
        self.cursor.execute(rquery)
        rows = self.cursor.fetchall()
        return rows

    # read from the database.
    def _read(self, mysql_cursor, tablename, querydict, optional=""):
        
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
            mysql_cursor.execute(rquery)
        except MySQLdb.Error:
            pass

        rows = mysql_cursor.fetchall()

        for arow in list(rows):
            ret.append(arow)
        return ret

    def read_instances(self, querydict={}):
        return self._read(self.cursor, self.instances_table, querydict)

    def read_userinfo(self, querydict={}):
        return self._read(self.cursor_keystone, self.userinfo_table, querydict)

    def value_todate(self,string):
        return datetime.strptime(string, '%Y-%m-%d %H:%M:%S')
