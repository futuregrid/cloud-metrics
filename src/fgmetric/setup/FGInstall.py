#!/usr/bin/env python

import os
import sys
import pprint
import ConfigParser
import argparse
import MySQLdb
import getpass

pp = pprint.PrettyPrinter(indent=0)
    
class FGInstall(object):

    instance_table = "instance"
    userinfo_table = "userinfo"
    projectinfo_table = "projectinfo"
    cloudplatform_table = "cloudplatform"
    def_cfg_path = os.getenv("HOME") + "/.futuregrid/"
    def_cfg_filename = "futuregrid.cfg"
    def_yaml_filename = "futuregrid.yaml"
    cfg_section_name = "CloudMetricsDB"
    dbinfo = { "host": None,
                "port": None,
                "userid": None,
                "passwd": None,
                "dbname": None }

    # Initialize
    def __init__(self):
        self.get_argparse()
        if not self.exist_cfgfile() or self.force_cfgfile():
            self.get_dbinfo()
            self.create_cfgfile()
            self.chmod_cfgfile()
        self.create_db()
        self.close_db()

    def exist_cfgfile(self):
        #read config from file configfile
        self.cfgfile = self.cfg_path + self.args.conf
        try:
            with open(self.cfgfile):
                return True
        except IOError:
            print self.cfgfile + " exist."
            return False

    def force_cfgfile(self):
        input_var = raw_input("Rewrite cfgfile? [y/N]: ")
        if input_var.lower() == "y":
            return True
        return False

    def create_cfgfile(self):
        config = ConfigParser.RawConfigParser()
        config.add_section(self.cfg_section_name)
        config.set(self.cfg_section_name, 'host', self.dbinfo['host'])#=suzie.futuregrid.org\n\
        config.set(self.cfg_section_name, 'port', self.dbinfo['port'])#=3306\n\
        config.set(self.cfg_section_name, 'user', self.dbinfo['userid'])#=fgmetric\n\
        config.set(self.cfg_section_name, 'passwd', self.dbinfo['passwd'])#=\n\
        config.set(self.cfg_section_name, 'db', self.dbinfo['dbname'])#=cloudmetrics\n\

        with open(self.cfgfile, 'wb') as configfile:
            print
            print "... creating " + self.cfgfile + " file ..."
            config.write(configfile)
            print "... database information successfully saved ..."

    def chmod_cfgfile(self):
        """Change a file mode to 0600. Only owner is allowed to read and write."""
        os.chmod(self.cfgfile, 0600)

    def create_yamlfile(self):
        f = open(self.cfg_path + self.def_yaml_filename, "w")
        dataMap = { cfg_section_name : self.dbinfo }
        yaml.dump(dataMap, f)
        f.close()

    def get_dbinfo(self):

        print "=" * 30
        print "Installing Cloud Metrics ..."
        print "=" * 30
        print
        print "If you have installed MySQL database for Cloud Metrics,"
        print "you will be asked to type the database information."
        print
        print "-" * 30
        print "mysql database information"
        print "-" * 30

        try:
            self.dbinfo['host'] = raw_input("db host ip address: ")
            self.dbinfo['port'] = raw_input("db port (default:3306): ") or "3306"
            self.dbinfo['userid'] = raw_input("db userid: ")
            self.dbinfo['passwd'] = getpass.getpass("db password: ")
            self.dbinfo['dbname'] = raw_input("db name: ")
        except:
            print sys.exc_info()
            raise

    def create_db(self):

        print "-" * 30
        print "MySQL table creation"
        print "-" * 30

        cfgfile = self.cfgfile
        config = ConfigParser.ConfigParser()
        config.read(cfgfile)

        try:
            #db parameters
            dbhost = config.get('CloudMetricsDB', 'host')
            dbport = int(config.get('CloudMetricsDB', 'port'))
            dbuser = config.get('CloudMetricsDB', 'user')
            dbpasswd = config.get('CloudMetricsDB', 'passwd')
            dbname = config.get('CloudMetricsDB', 'db')
            #euca_hostname = config.get('CloudMetricsDB', 'euca_hostname')
            #euca_version = config.get('CloudMetricsDB', 'euca_version')
        except ConfigParser.NoSectionError:
            print cfgfile + " does not exist"
            sys.exit()

        #set parameters
        #self.euca_version = euca_version
        #self.euca_hostname = euca_hostname

        #connect to db
        self.conn = MySQLdb.connect (dbhost, dbuser, dbpasswd, dbname, dbport)
        self.cursor = self.conn.cursor (MySQLdb.cursors.DictCursor)
        
        #create table if not exist
        create_instance_table = "create table if not exists " + self.instance_table + " (\
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
                accountId VARCHAR(32), \
                kernelURL VARCHAR(128), \
                ramdiskId VARCHAR(32), \
                volumes VARCHAR(1024), \
                launchIndex INT, \
                platform VARCHAR(16), \
                bundleTaskStateName VARCHAR(16), \
                reservationId VARCHAR(32), \
                cloudPlatformIdRef tinyint)"

        create_userinfo_table = "create table if not exists " + self.userinfo_table + " (\
                ownerid varchar(32) primary key not null, \
                first_name varchar(32), \
                last_name varchar(32), \
                uid INT, \
                username varchar(32), \
                project varchar(16), \
                hostname varchar(16), \
                email varchar(255))"

        create_cloudplatform_table = "create table if not exists " + self.cloudplatform_table + " (\
                cloudPlatformId tinyint primary key auto_increment not null, \
                hostname varchar(32), \
                version varchar(8), \
                platform varchar(16), \
                institution varchar(16), \
                cores int default 0)"

        create_projectinfo_table = "CREATE TABLE if not exists " + self.projectinfo_table + " (\
              `ProjectId` int(11) NOT NULL DEFAULT '0',\
              `Completed` varchar(16) COLLATE utf8_unicode_ci DEFAULT NULL,\
              `Title` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,\
              `ProjectLead` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,\
              `Institution` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,\
              `Department` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,\
              `Keywords` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,\
              `Results` varchar(512) COLLATE utf8_unicode_ci DEFAULT NULL,\
              PRIMARY KEY (`ProjectId`)\
            ) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;"

        try:
            print "... creating MySQL tables for Cloud Metrics ..."
            self.cursor.execute(create_instance_table)
            print self.instance_table + " created if not exists"
            self.cursor.execute(create_userinfo_table)
            print self.userinfo_table + " created if not exists"
            self.cursor.execute(create_projectinfo_table)
            print self.projectinfo_table + " created if not exists"
            self.cursor.execute(create_cloudplatform_table)
            print self.cloudplatform_table + " created if not exists"
        except MySQLdb.Error:
            pass

    def close_db(self):
        try:
            self.cursor.close()
            self.conn.close()
        except:
            pass

    def get_argparse(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--conf", dest="conf", default=self.def_cfg_filename,
                help="configuraton file for Cloud Metrics")
        parser.add_argument("--yaml", dest="yaml", default=self.def_yaml_filename,
                help="configuraton YAML file for Cloud Metrics")
        self.args = parser.parse_args()

    def __del__(self):
        ''' destructor '''
        pass

def main():
    install = FGInstall()

if __name__ == '__main__':
    main()
