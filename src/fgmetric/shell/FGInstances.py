import re
import json
import pprint
import sys
import os
import re
import subprocess
from datetime import *
from collections import deque
import argparse

from fgmetric.shell.FGDatabase import FGDatabase

manual = """
MANUAL PAGE DRAFT

NAME - FutureGrid instances

DESCRIPTION

This class provides a main data structure for the FutureGrid Cloud
Metrics framework.  This class should be used when VM instance
information is collected by the log parser or the metrics analyzer to
support unified data formats.

"""


class FGInstances:

    instance = {}
    userinfo = []
    projectinfo = {}

    default_projectinfo = {"ProjectId": None,
                           "Title": None,
                           "Institution": None,
                           "ProjectLead": None,
                           "Discipline": None}

                           # "Completed":None,
                           #"Department":None",
                           #"Keywords":None,
                           #"Results":None}
    pp = None
    db = None
    in_the_future = None
    in_the_past = None
    first_date = None
    last_date = None
    cloudplatform = None

    def __init__(self):

        self.db = FGDatabase()
        self.in_the_future = datetime.strptime(
            "3000-01-01 00:00:00", '%Y-%m-%d %H:%M:%S')
        self.in_the_past = datetime.strptime(
            "1970-01-01 00:00:00", '%Y-%m-%d %H:%M:%S')
        self.pp = pprint.PrettyPrinter(indent=0)
        self.first_date = datetime.strptime(
            "3000-01-01 00:00:00", '%Y-%m-%d %H:%M:%S')
        self.last_date = datetime.strptime(
            "1981-01-01 00:00:00", '%Y-%m-%d %H:%M:%S')

    def clear(self, opts=None):
        if not opts or opts == "instance":
            self.instance = {}
        if not opts or opts == "userinfo":
            self.userinfo = []
        if not opts or opts == "projectinfo":
            self.projectinfo = {}

    def get_instance(self, index=None):
        return self.get_data(index)

    def get_data(self, index=None, withInfo=False):
        return self.get_instance_with_info(index, withInfo)

    def get_instance_with_info(self, index, withInfo):

        # This should be returned with same type but this isn't. if
        # index comes with it, returns 'dict' and without it, returns
        # list. what a unconsistent.
        if isinstance(index, (int, long)):
            instances = [self.instance[index]]
        else:
            instances = self.instance

        if not withInfo:
            return instances

        res = []
        for ins in instances:
            try:
                userinfo = self.get_userinfo({"ownerid": ins["ownerId"],
                                              "username": ins["ownerId"]})
                if userinfo:
                    ins = dict(userinfo.items() + ins.items())

                    # Extension for project information
                    prj_id = userinfo["project"]
                    if prj_id:
                        if prj_id.startswith("fg"):
                            prj_id = int(prj_id[2:])
                        #else:
                        #    if prj_id.startswith("member"):
                        #        userinfo = self.get_userinfo({"ownerid":
                        #                                  ins["ownerId"],"username":
                        #                                  ins["ownerId"]}, 
                        #                                 " and project!='member' ")
                        #    if prj_id == "member":
                        #    prj_id = userinfo['project']
                        #    if prj_id:
                        #        if prj_id.startswith('fg'):
                        #            prj_id = int(prj_id[2:])

                        projectinfo = self.get_projectinfo(
                            prj_id)  # Remove 'fg' prefix
                        if projectinfo:
                            ins = dict(projectinfo.items() + ins.items())
                else:
                    ins = dict(ins.items() + self.default_projectinfo.items())

                res.append(ins)
            except:
                pass

        # MISSING error exception for empty res return. it may occur
        # index error of the call in FGMetrics. i.e. ... [0]
        return res

    """

    REPLACEMENT FOR get_userinfo get_projectinfo

    def _get_info(self, type, index=None):
        if isinstance(index, (int, long)):
            return type[index]
        elif isinstance(index, (dict)):
            # Search
            for key, val in index.iteritems():
                for element in type:
                    if key in element and type[key] == val:
                        return element
        elif index in None:
            return type
        else:
            return None

    def get_userinfo(self, index=None):
        return _get_info(self.userinfo, index):

    def get_projectinfo(self, index=None):
        return _get_info(self.projectinfo, index):

    """

    def get_userinfo(self, index=None):
        """should be replaced with above code"""
        if isinstance(index, (int, long)):
            return self.userinfo[index]
        elif isinstance(index, (dict)):
            # Search
            for key, val in index.iteritems():
                for userinfo in self.userinfo:
                    if key in userinfo and userinfo[key] == val:
                        return userinfo
        elif index is None:
            if not self.userinfo:
                self.read_userinfo_from_db()
            return self.userinfo
        else:
            return None

    def get_projectinfo(self, index=None):
        """should be replaced with above code"""
        if isinstance(index, (int, long)):
            return self.projectinfo[index]
        elif isinstance(index, (dict)):
            for key, val in index.iteritems():
                for projectinfo in self.projectinfo:
                    if key in projectinfo and projectinfo[key] == val:
                        return projectinfo
        elif index is None:
            if not self.projectinfo:
                self.read_projectinfo_from_db()
            return self.projectinfo
        else:
            return None

    def count(self):
        return len(self.instance)

    def read_from_db(self):
        self.read_instances()

    def read_instances(self, querydict={}, optional=""):
        self.clear("instance")
        self.instance = self.db.read(querydict, optional)

    def read_projectinfo_from_db(self):

        res = {}
        self.clear("projectinfo")
        prjinfo_list = self.db.read_projectinfo()
        res = {element["ProjectId"]: element for element in prjinfo_list}
        self.projectinfo = res

    def read_userinfo_from_db(self):
        self.read_userinfo()

    def read_userinfo(self, querydict={}, optional=""):

        self.clear("userinfo")
        self.userinfo = self.db.read_userinfo(querydict, optional)

    def read_userinfo_detail(self):
        self.clear("userinfo")
        self.userinfo = self.db.get_userinfo_detail()

    def read_cloudplatform(self, refresh=False):
        if not self.cloudplatform or refresh:
            self.cloudplatform = self.db.read_cloudplatform()
        return self.cloudplatform

    def get_cloudplatform_id(self, querydict={}):
        class ContinueOutOfALoop(Exception):
            pass
        for row in self.read_cloudplatform():
            try:
                for key in querydict:
                    if row[key] != querydict[key]:
                        raise ContinueOutOfALoop
                return row["cloudPlatformId"]
            except ContinueOutOfALoop:
                continue
        return None

    def write_to_db(self):
        for key_current in self.instance:
            self.db.write(self.instance[key_current])

    def write_userinfo_to_db(self):
        for key_current in self.userinfo:
            self.db.write_userinfo(key_current)

    def add(self, datarecord):
        """prints the information for each instance"""
        if datarecord["linetype"] == "print_ccInstance":
            instanceId = datarecord["instanceId"]
            ownerId = datarecord["ownerId"]
            timestamp = datarecord["ts"]
            status = datarecord["state"].lower()
            t = datarecord["date"]

            id = instanceId + " " + ownerId + " " + str(timestamp)

            instance = self.instance

            try:
                current = instance[id]
                # if were wereto do a data base this line needs to be
                # replaced
            except:
                current = datarecord

            # if not ("t_end" in current):
            try:
                current["t_end"]
            except:
            # time in the future
                f = self.in_the_future

                current["trace"] = {
                    "pending": {"start": f, "stop": t},
                    "teardown": {"start": f, "stop": t},
                    "extant": {"start": f, "stop": t}
                }
                current["t_end"] = current["date"]
                current["t_start"] = current["ts"]  # for naming consitency
                current["duration"] = 0.0

            current["t_end"] = max(current["t_end"], t)
            current["trace"][status]["start"] = min(
                current["trace"][status]["start"], t)
            current["trace"][status]["stop"] = max(
                current["trace"][status]["stop"], t)

            instance[id] = current

    def update_traceinfo(self, row):
        ''' New version of add function  '''
        res = self.set_datetime(row)
        updated_res = self.update_to_list(res)
        return updated_res

    def set_datetime(self, row):

        future = self.in_the_future
        past = self.in_the_past
        # Set datetime
        row["t_start"] = row["ts"]
        row["t_end"] = self.get_t_end(row)
        row["duration"] = self.get_t_delta(row)
        row["trace"] = {
            "pending": {"start": future, "stop": past, "queue": deque("", 10)},
            "extant": {"start": future, "stop": past, "queue": deque("", 10)},
            "teardown": {"start": future, "stop": past, "queue": deque("", 10)}
        }

        return row

    def update_to_list(self, row):
        ''' Reflect to the current list '''

        instanceId = row["instanceId"]
        ownerId = row["ownerId"]
        ts = row["ts"]
        key = instanceId + " " + ownerId + " " + str(ts)

        res = self.update_trace_datetime(key, row)
        # Update - this needs to be changed.
        if row["date"] > res["date"]:
            res["state"] = row["state"]
            res["date"] = row[
                "date"]  # max(res["date"], row["date"]) # we don't need date column
            res["duration"] = row[
                "duration"]  # max(res["duration"], row["duration"])
            res["t_end"] = row["t_end"]  # min(res["t_end"], row["t_end"])
        self.instance[key] = res

        return res

    def update_trace_datetime(self, key, new):

        if key in self.instance:
            old = self.instance[key]
        else:
            old = new

        state = new["state"].lower()
        old["trace"][state]["queue"].append(new["date"])
        queue = old["trace"][state]["queue"]
        old["trace"][state]["start"] = min(
            queue)  # min(old["trace"][state]["start"], new["date"])
        old["trace"][state]["stop"] = max(
            queue)  # max(old["trace"][state]["stop"], new["date"])

        return old

    def get_previous_state(self, state):
        state = state.lower()
        if state == "pending":
            return state
        elif state == "extant":
            return "pending"
        elif state == "teardown":
            return "extant"

    def get_t_end(self, row):
        return row["date"]
        '''
        if row["state"] == "Teardown":
                return row["date"]
        else:
                return self.in_the_future
        '''

    def get_t_delta(self, row):

        start = row["t_start"]
        last = row["date"]

        if row["state"] == "Teardown":
            if row["t_end"]:
                last = max(row["date"], row["t_end"])

        t_delta = (last - start).total_seconds()
        if t_delta < 0:
            t_delta = timedelta(0).total_seconds()
        return t_delta

    def refresh(self):
        """calculates how long each instance runs in seconds"""
        for i in self.instance:
            values = self.instance[i]
            if values["state"] == "Teardown":
                t_delta = values["t_end"] - values["ts"]
            else:
                t_delta = values["date"] - values["ts"]

            if t_delta.total_seconds() < 0:
                t_delta = values["t_end"] - values["t_end"]
            values["duration"] = str(t_delta.total_seconds())

    def set_userinfo(self):
        for i in self.instance:
            ownerid = self.instance[i]["ownerId"]
            try:
                new_userinfo = retrieve_userinfo_ldap(ownerid)
                self.add_userinfo(new_userinfo)
            except:
                continue

    def add_userinfo(self, new_userinfo):
        if self.userinfo.count(new_userinfo) == 0:
            self.userinfo.append(new_userinfo)

    '''
    need to be redefined...

    def todatetime (self,instance):
        instance["trace"]["teardown"]["start"] = value_todate(instance["trace"]["teardown"]["start"])
        instance["trace"]["teardown"]["stop"] = value_todate(instance["trace"]["teardown"]["stop"])
        instance["trace"]["extant"]["start"] = value_todate(instance["trace"]["extant"]["start"])
        instance["trace"]["extant"]["stop"] = value_todate(instance["trace"]["extant"]["stop"])
        instance["trace"]["pending"]["start"] = value_todate(instance["trace"]["pending"]["start"])
        instance["trace"]["pending"]["stop"] = value_todate(instance["trace"]["pending"]["stop"])
        instance["t_start"] = value_todate(instance["t_start"])
        instance["date"] = value_todate(instance["date"])
        instance["t_end"] = value_todate(instance["t_end"])
        instance["ts"] = value_todate(instance["ts"])

    def tostr(self,instance):
        instance["trace"]["teardown"]["start"] = str(instance["trace"]["teardown"]["start"])
        instance["trace"]["teardown"]["stop"] = str(instance["trace"]["teardown"]["stop"])
        instance["trace"]["extant"]["start"] = str(instance["trace"]["extant"]["start"])
        instance["trace"]["extant"]["stop"] = str(instance["trace"]["extant"]["stop"])
        instance["trace"]["pending"]["start"] = str(instance["trace"]["pending"]["start"])
        instance["trace"]["pending"]["stop"] = str(instance["trace"]["pending"]["stop"])
        instance["ts"] = str(instance["ts"])
        instance["t_start"] = str(instance["t_start"])
        instance["date"] = str(instance["date"])
        instance["t_end"] = str(instance["t_end"])

    def value_todate(self,string):
        return datetime.strptime(string, '%Y-%m-%d %H:%M:%S')

    def dump(self,index = "all"):

        if index == "all" or (index == "") :
            for key in self.data:
                print "------------------------"
                pp.pprint(self.data[key])
            print "------------------------"
            self.print_total()
            print "------------------------"
        elif (index >= 0) and (index < len(str)):
            pp.pprint(self.data[index])
        else:
            print "ERROR printing of index " + index

    def print_list(self,index = "all"):

        if (index == "all") or (index == "") :
            for key in self.data:
                print(self.data[key]["instanceId"])
            print "------------------------"
            self.print_total()
            print "------------------------"
        elif (index >= 0) and (index < len(str)):
            print(self.data[index]["instanceId"])
        else:
            print "ERROR printing of index " + index

    def json_dump(self):
         string = ""
         for key in all:
            self.tostr (all[key])
         string = json.dumps(all, sort_keys=False, indent=4)
         for key in all:
             print all[key]
         self.todatetime (all[key])
         return string

    def getDateRange(self):
        for i in self.data:
            element = self.data[i]
            if self.first_date > element["date"]:
                self.first_date = element["date"]
            if self.last_date < element["date"]:
                self.last_date = element["date"]
        return (str(self.first_date), str(self.last_date))

    '''
