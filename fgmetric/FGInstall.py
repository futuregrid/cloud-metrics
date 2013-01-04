#!/usr/bin/env python

import os
import sys
import pprint
import ConfigParser
import argparse
import MySQLdb

pp = pprint.PrettyPrinter(indent=0)
    
class FGInstall(object):

    instance_table = "instance"
    userinfo_table = "userinfo"
    projectinfo_table = "projectinfo"
    cloudplatform_table = "cloudplatform"

    # Initialize
    def __init__(self, configfile="futuregrid.cfg"):
        if not configfile:
            configfile="futuregrid.cfg"

        #read config from file configfile
        config = ConfigParser.ConfigParser()
        cfgfile = os.getenv("HOME") + "/.futuregrid/" + configfile
        config.read(cfgfile)

        print cfgfile + " has been loaded.\n"

        try:
            #db parameters
            dbhost = config.get('EucaLogDB', 'host')
            dbport = int(config.get('EucaLogDB', 'port'))
            dbuser = config.get('EucaLogDB', 'user')
            dbpasswd = config.get('EucaLogDB', 'passwd')
            dbname = config.get('EucaLogDB', 'db')
            euca_hostname = config.get('EucaLogDB', 'euca_hostname')
            euca_version = config.get('EucaLogDB', 'euca_version')
        except ConfigParser.NoSectionError:
            print cfgfile + " does not exist"
            sys.exit()

        #set parameters
        self.euca_version = euca_version
        self.euca_hostname = euca_hostname

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

        create_projectinfo_table = "CREATE TABLE if not exist " + self.projectinfo_table + " (\
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

    def __del__(self):
        ''' destructor '''
        try:
            self.cursor.close()
            self.conn.close()
        except:
            pass

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--conf", dest="conf",
            help="configuraton file of the database to be used")
    args = parser.parse_args()
    install = FGInstall(args.conf)

if __name__ == '__main__':
    main()
