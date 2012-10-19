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

from fgmetric.FGDatabase import FGDatabase

manual="""
MANUAL PAGE DRAFT

NAME - FutureGrid instances

DESCRIPTION

This class provides a main data structure for the FutureGrid Cloud Metrics framework.
This class should be used when VM instance information is collected by the log parser or the metrics analyzer to support unified data formats.

"""

class FGInstances:
 
    data = {}
    userinfo_data = []
    pp = None
    db = None
    in_the_future = None
    in_the_past = None
    first_date = None
    last_date = None
    cloudplatform = None
    
    def __init__(self):

        self.db = FGDatabase()
        self.in_the_future = datetime.strptime("3000-01-01 00:00:00", '%Y-%m-%d %H:%M:%S')
        self.in_the_past = datetime.strptime("1970-01-01 00:00:00", '%Y-%m-%d %H:%M:%S')
        self.pp = pprint.PrettyPrinter(indent=0)
        self.first_date  = datetime.strptime("3000-01-01 00:00:00", '%Y-%m-%d %H:%M:%S')
        self.last_date = datetime.strptime("1981-01-01 00:00:00", '%Y-%m-%d %H:%M:%S')

    def clear(self):
        self.data = {}
        self.userinfo_data = []

    def get_data(self, index=None):
        if isinstance(index, (int, long)):
            return self.data[index]
        else:
            return self.data

    def count(self):
        return len(self.data)

    def read_from_db(self):
        key = 0 
        self.clear()
        instance_list = self.db.read()

        for element in instance_list:
            self.data[key] = element
            key += 1

    def read_userinfo_from_db(self):

        self.clear()
        userinfo_list = self.db.read_userinfo()

        for element in userinfo_list:
            self.userinfo_data.append(element)

    def read_cloudplatform(self, refresh=False):
        if not self.cloudplatform or refresh:
            self.cloudplatform = self.db.read_cloudplatform()
        return self.cloudplatform

    def get_cloudplatform_id(self, querydict={}):
        class ContinueOutOfALoop(Exception): pass
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
        for key_current in self.data:
            self.db.write(self.data[key_current])

    def write_userinfo_to_db(self):
        for key_current in self.userinfo_data:
            self.db.write_userinfo(key_current)

    def add (self,datarecord):
        """prints the information for each instance"""
        if datarecord["linetype"] == "print_ccInstance":
            instanceId = datarecord["instanceId"] 
            ownerId = datarecord["ownerId"]
            timestamp = datarecord["ts"]
            status = datarecord["state"].lower()
            t = datarecord["date"]

            id = instanceId + " " + ownerId + " " + str(timestamp)

            instance = self.data

            try:
                current = instance[id]
                # if were wereto do a data base this line needs to be replaced
            except:
                current = datarecord

            if not ("t_end" in current):
            #time in the future
                f = self.in_the_future

                current["trace"] = {
                    "pending" : {"start" : f, "stop": t},
                    "teardown" : {"start" : f, "stop": t},
                    "extant" : {"start" : f, "stop": t}
                    }
                current["t_end"] = current["date"]
                current["t_start"] = current["ts"] # for naming consitency
                current["duration"] = 0.0

            current["t_end"] = min(current["t_end"], t)
            current["trace"][status]["start"] = min(current["trace"][status]["start"],t)
            current["trace"][status]["stop"] = max(current["trace"][status]["stop"],t)

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
                "pending" : { "start" : future, "stop" : past, "queue" : deque("",10)},
                "extant" : { "start" : future, "stop" : past, "queue" : deque("",10)},
                "teardown" : { "start" : future, "stop" : past, "queue" : deque("",10)}
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
            res["date"] = row["date"] #max(res["date"], row["date"]) # we don't need date column
            res["duration"] = row["duration"]#max(res["duration"], row["duration"])
            res["t_end"] = row["t_end"]#min(res["t_end"], row["t_end"])
	self.data[key] = res

        return res

    def update_trace_datetime(self, key, new):

        if key in self.data:
            old = self.data[key]
        else:
            old = new

        state = new["state"].lower()
        old["trace"][state]["queue"].append(new["date"])
        queue = old["trace"][state]["queue"]
        old["trace"][state]["start"] = min(queue) #min(old["trace"][state]["start"], new["date"])
        old["trace"][state]["stop"] = max(queue) #max(old["trace"][state]["stop"], new["date"])

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
	if row["state"] == "Teardown":
		return row["date"]
	else:
		return self.in_the_future

    def get_t_delta(self, row):

	start = row["t_start"]
	last = row["date"]

	if row["state"] == "Teardown":
		if row["t_end"]:
			last = min(row["date"], row["t_end"])

	t_delta = (last - start).total_seconds()
	if t_delta < 0:
		t_delta = timedelta(0).total_seconds()
	return t_delta

    def refresh(self):
        """calculates how long each instance runs in seconds"""
        for i in self.data:
            values = self.data[i]
            if values["state"] == "Teardown":
                t_delta = values["t_end"] - values["ts"]
            else:
                t_delta = values["date"] - values["ts"]

            if t_delta.total_seconds() < 0:
                t_delta = values["t_end"] - values["t_end"]
            values["duration"] = str(t_delta.total_seconds())

    def set_userinfo(self):
        for i in self.data:
            ownerid = self.data[i]["ownerId"]
            try:
                new_userinfo = retrieve_userinfo_ldap(ownerid)
                self.add_userinfo(new_userinfo)
            except:
                continue

    def add_userinfo(self, new_userinfo):
        if self.userinfo_data.count(new_userinfo) == 0:
            self.userinfo_data.append(new_userinfo)

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
