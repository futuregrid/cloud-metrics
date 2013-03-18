from fgmetric.shell.FGParser import Instances
import MySQLdb
import sys
import cherrypy

class Userinfo:

    platform = None

#    def __init__(self):
 #       self.do_loaddb()

    def convert_ownerId_str(self, id):
        """Convert a owner id to a user name
        
        * This should be working with retrieving ldap commands
        * Currently, this function is a test version
        """

        if self.platform and (self.platform == "nova" or self.platform == "openstack"):
            id = self.convert_nova_userid_to_username(id)

        for element in self.instances.userinfo_data:
            if element['ownerid'] == id:
                try:
                    return element['first_name'] + " " + element['last_name']
                except:
                    return id

        # Second try if it does not exist
        for element in self.instances.userinfo_data:
            if element['username'] == id:
                try:
                    return element['first_name'] + " " + element['last_name']
                except:
                    return id

        if id == "EJMBZFNPMDQ73AUDPOUS3":
            return "eucalyptus-admin"
        else: 
            return id

    def convert_accountId_str(self, id):
        """Convert an account id to a user name

        * This should be working with retrieving ldap commands
        * Currently, this function is a test version

        # Temporarily add here 
        # But it will be replaced by 'euare-accountlist|grep $accountid'
        # e.g. euare-accountlist|grep fg82
        # fg82    281408815495
        """

        ## TEST ONLY ~!!!!! ##
        if id == "458299102773" :
            return "eucalyptus"
        elif id == "281408815495" :
            return "fg82"
        elif id == "000000000001" :
            return "system"
        elif id == "081364875274" :
            return "fg168"
        elif id == "150119767462" :
            return "fg3"
        elif id == "355794507465" :
            return "fg201"
        else :
            return id

    def convert_nova_userid_to_username(self, id):
        """Convert a owner id to a user name
        
        * This should be working with retrieving ldap commands
        * Currently, this function is a test version
        """

        for element in self.nova.userinfo:
            if element['id'] == id:
                return element['name']

    def set_fullname(self):
        for uname in self.users:
            fullname = self.convert_ownerId_str(uname)
            self.users[uname]['fullname'] = fullname

    def get_ownerId(self, instance_ids):

        ret = []
        conditions = "instanceId in ('" + "', '".join(instance_ids) + "') "
        #rquery = "select ownerId from " + self.instances.eucadb.instance_table + " where " + conditions
        rquery = "select ownerId from instance where " + conditions
        rquery = "select concat(first_name, \" \", last_name) as fullname from (select ownerId, first_name, last_name from userinfo) as t1 join (select ownerId from instance where %s) as t2 on t1.ownerid=t2.ownerid" % conditions

        cursor = cherrypy.thread_data.db.cursor() 
        #cursor = self.instances.eucadb.cursor
        try:
            cursor.execute(rquery)
        except MySQLdb.OperationalError, e:
            print e
            if e[0] == 2006:
                #self.do_loaddb()
                pass

        except MySQLdb.Error:
            print sys.exc_info()
            pass

        rows = cursor.fetchall()
        return rows

    def do_loaddb(self):
        self.users = {}
        self.instances = Instances()
        # Gets also userinfo data from the database
        self.instances.read_userinfo_from_db()

    def do_loadnovadb(self):
        self.nova = FGNovaMetric()
        # gets also data from the database
        self.nova.read_from_db()
