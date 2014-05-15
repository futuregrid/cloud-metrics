import sys
import os
from flask import Flask, jsonify
from flask.views import View
from FGMimerender import mimerender
from fgmetric.shell.FGDatabase import FGDatabase
from dateutil import parser

app = Flask(__name__)

@app.route('/')
def get_index_page():
    print "The server is running"
    return "The server is running\n"

@app.route('/metric/<cloudname>/<hostname>/<userid>/<metric>/<timestart>/<timeend>/<period>')
def get_metric(cloudname,hostname,userid,metric,timestart,timeend,period):

    search = SearchSettings()

    search.set_cloud(cloudname)
    search.set_date(timestart,timeend)
    search.set_metric(metric)
    search.set_userid(userid)
    search.set_period(period)
    search.set_host(hostname)
    if metric.lower() == "vmcount" or metric == "None":
        metrics = VMCount()
        metrics.set_search_settings(search)
    elif metric.lower() in ["walltime", "runtime", "wallclock"]:
        metrics = WallTime()
        metrics.set_search_settings(search)
    elif metric.lower() in ["usercount", "user"]:
        metrics = UserCount()
        metrics.set_search_settings(search)

    result = metrics.dispatch_request()
    #print result
    return result
   
@app.route('/metric/list_vms')
def get_list_vms():

    lvms = ListVMs()
    result = lvms.dispatch_request()
    print result
    return result

################################
# classes for metric api
################################

class SearchSettings:
    '''
    SearchSettings class
    collects user inputs to refine results
    '''
    def __init__(self):
        self.from_date = None # datetime
        self.to_date = None # datetime
        self.period = None
        self.metric = None
        self.host = None
        self.iaas = None
        self.userid = None

    def __str__(self):
        result = ""
        result += "from_date: %s\n" % self.from_date
        result += "to_date:   %s\n" % self.to_date
        result += "period:    %s\n" % self.period
        result += "metric:    %s\n" % self.metric
        result += "host:    %s\n" % self.host
        result += "iaas:      %s\n" % self.iaas
        result += "userid:      %s\n" % self.userid
        return result

    def set_date(self, from_date, to_date):
        if from_date != "None":
            self.from_date = parser.parse(from_date)
        if to_date != "None":
            self.to_date = parser.parse(to_date)

    def set_period(self, period):
        self.period = period

    def set_metric(self, metric):
        self.metric = metric

    def set_host(self, host):
        self.host = host

    def set_iaas(self, cloud):
        self.iaas = cloud

    def set_cloud(self, cloud):
        ''' link to set_iaas '''
        self.set_iaas(cloud)

    def set_userid(self, userid):
        self.userid = userid

class CloudMetric(View):

    def __init__(self):
        self.db = FGDatabase()
        self.db.conf()
        self.db.connect()
        self.cloudservice = None
        self.data = None
        #self.search = SearchSettings()

    @mimerender
    def dispatch_request(self):
        self.read_cloud_service()
        self.read_vms()
        res = self.data
        return {"message": res}

    def read_cloud_service(self):
        res = self.db.read_cloudplatform()
        new_res = {}
        for cloud in res:
            new_res[cloud['cloudPlatformId']] = cloud
            self.cloudservice = new_res

    def get_where_clause(self):
        self.generate_where_clause()
        return self.where_clause

    def generate_where_clause(self):
        where = []

        # basic for join table
        where.append("cloudplatform.cloudplatformid = \
                     instance.cloudplatformidref")

        if self.search.metric.lower() == "usercount":
            where.append("(userinfo.ownerid = instance.ownerid \
                         or userinfo.username = instance.ownerid)")

        if self.search.iaas:
            iaas_ids = self.get_iaas_ids(self.search.iaas)
            if iaas_ids:
                ids = ', '.join(map(str, iaas_ids))
                where.append("cloudplatformidref in (%s)" % ids)

        if self.search.host:
            host_ids = self.get_host_ids(self.search.host)
            if host_ids:
                ids = ', '.join(map(str, host_ids))
                where.append("cloudplatformidref in (%s)" % ids)

        if self.search.userid:
            owner_ids = self.get_owner_ids(self.search.userid)
            if owner_ids:
                ids = "'" + "', '".join(map(str, owner_ids)) + "'"
            else: # there is no such user
                ids = "'" + self.search.userid + "'"
                where.append("ownerid in (%s)" % ids)

        if self.search.from_date:
            where.append("t_start >= '%s'" % str(self.search.from_date))
        if self.search.to_date:
            where.append("t_end <= '%s'" % str(self.search.to_date))
            
        self.where_clause = " where " + " and ".join(map(str,where))
        return self.where_clause

    def get_owner_ids(self, name):
        ids = []
        self.db.cursor.execute("select ownerid from %s where username='%s'" \
                               % (self.db.userinfo_table, name))
        results = self.db.cursor.fetchall()
        ids = map(lambda x: x['ownerid'],results)
        return ids
    
    def get_host_ids(self, name):

        ids = []

        self.db.cursor.execute("select cloudPlatformId from cloudplatform" \
                               + " where hostname = '%s'" % name)
        results = self.db.cursor.fetchall()
        for row in results:
            ids.append(row['cloudPlatformId'])
        return ids


    def get_iaas_ids(self, name):
        ids = []

        self.db.cursor.execute("select cloudPlatformId from cloudplatform" \
                               + " where platform = '%s'" % name)
        results = self.db.cursor.fetchall()
        for row in results:
            ids.append(row['cloudPlatformId'])
        return ids

    def set_search_settings(self, searchObject):
        self.search = searchObject

    def map_cloudname(self):
        for record in self.data:
            try: 
                cloudname = self.cloudservice[record['cloudplatformidref']]
            except:
                print record

class VMCount(CloudMetric):

    def __init__(self):
        CloudMetric.__init__(self)

    def read_vms(self):
        cursor = self.db.cursor
        table = self.db.instance_table
        table2 = self.db.cloudplatform_table
        where_clause = self.get_where_clause()
        query = "select DATE_FORMAT(date,'%%Y %%b') as 'YEAR MONTH', \
                %(table2)s.platform as 'CLOUDNAME', \
                count(*) as 'VMCOUNT' \
                from %(table)s, %(table2)s \
                %(where_clause)s \
                group by %(table2)s.platform, \
                YEAR(date), MONTH(date)" % vars()
        try:
            cursor.execute(query)
            self.data = cursor.fetchall()
        except:
            print sys.exc_info()

class WallTime(CloudMetric):

    def __init__(self):
        CloudMetric.__init__(self)

    def read_vms(self):
        cursor = self.db.cursor
        table = self.db.instance_table
        table2 = self.db.cloudplatform_table
        where_clause = self.get_where_clause()
        query = "select DATE_FORMAT(date,'%%Y %%b') as 'YEAR MONTH', \
                %(table2)s.platform as 'CLOUDNAME', \
                FORMAT(SUM(time_to_sec(timediff(t_end,t_start))/60/60),2) \
                as 'WallTime (Hrs)' \
                from %(table)s, %(table2)s \
                %(where_clause)s \
                group by %(table2)s.platform, \
                YEAR(date), MONTH(date)" % vars()
        try:
            cursor.execute(query)
            self.data = cursor.fetchall()
        except:
            print sys.exc_info()

class UserCount(CloudMetric):

    def __init__(self):
        CloudMetric.__init__(self)

    def read_vms(self):
        cursor = self.db.cursor
        table = self.db.instance_table
        table2 = self.db.cloudplatform_table
        table3 = self.db.userinfo_table
        where_clause = self.get_where_clause()
                #CONCAT(first_name, " ", last_name) as 'NAME', \
        query = "select DATE_FORMAT(date,'%%Y %%b') as 'YEAR MONTH', \
                %(table2)s.platform as 'CLOUDNAME', \
                COUNT(userinfo.username) as 'USERCOUNT' \
                from %(table)s, %(table2)s, %(table3)s \
                %(where_clause)s \
                group by %(table2)s.platform, \
                YEAR(date), MONTH(date)" % vars()
        try:
            print "Be patient, it takes about 10 to 30 seconds ..."
            cursor.execute(query)
            self.data = cursor.fetchall()
        except:
            print sys.exc_info()



#app.add_url_rule('/list_vms.json', view_func = ListVMs.as_view('list_vms'))

if __name__ == "__main__":
    app.run(host=os.environ["FG_HOSTING_IP"],
            port=int(os.environ["FG_HOSTING_PORT"]),debug=True)
