#! /usr/bin/env python

from pygooglechart import PieChart3D
from pygooglechart import StackedHorizontalBarChart
from pygooglechart import Axis


import re
import json
import sys
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta

users = {}
instance = {}

def clear():
    users = {}
    instance = {}

    
######################################################################
# PRINT DATA 
######################################################################

def instance_json_dump(all):
    string = ""
    for key in all:
        instance_tostr_data (all[key])
    string = json.dumps(all, sort_keys=False, indent=4)
    for key in all:
        instance_todate_data(all[key])
    
    return string 

 
def value_todate(string):
   return datetime.strptime(string, '%Y-%m-%d %H:%M:%S')

def instance_todate_data(data):
    data["trace"]["teardown"]["start"] = value_todate(data["trace"]["teardown"]["start"])
    data["trace"]["teardown"]["stop"] = value_todate(data["trace"]["teardown"]["stop"])
    data["trace"]["extant"]["start"] = value_todate(data["trace"]["extant"]["start"])
    data["trace"]["extant"]["stop"] = value_todate(data["trace"]["extant"]["stop"])
    data["trace"]["pending"]["start"] = value_todate(data["trace"]["pending"]["start"])
    data["trace"]["pending"]["stop"] = value_todate(data["trace"]["pending"]["stop"])
    data["t_start"] = value_todate(data["t_start"])
    data["date"] = value_todate(data["date"])
    data["t_end"] = value_todate(data["t_end"])
    data["ts"] = value_todate(data["ts"])
    #return data

def instance_tostr_data(data):
    data["trace"]["teardown"]["start"] = str(data["trace"]["teardown"]["start"])
    data["trace"]["teardown"]["stop"] = str(data["trace"]["teardown"]["stop"])
    data["trace"]["extant"]["start"] = str(data["trace"]["extant"]["start"])
    data["trace"]["extant"]["stop"] = str(data["trace"]["extant"]["stop"])
    data["trace"]["pending"]["start"] = str(data["trace"]["pending"]["start"])
    data["trace"]["pending"]["stop"] = str(data["trace"]["pending"]["stop"])
    data["ts"] = str(data["ts"])
    data["t_start"] = str(data["t_start"])
    data["date"] = str(data["date"])
    data["t_end"] = str(data["t_end"])
    #return data
        
######################################################################
# GENERATE INSTANCE STATISTICS
######################################################################

#instance_c = {"id": null }

#def instance_cache(id):
#    if id == instance_c["id"]:
#        skip
#    else:
#        # witre instance_c[id] to db
#        # instance_c[id] = get instance with id from db
        
    

def minmax_time (t_a, t_b):
    if t_a < t_b:
        return (t_a,t_b)
    else:
        return (t_b,t_a)
    
def generate_instance_info (data):
    """prints the information for each instance"""
    if data["linetype"] == "print_ccInstance":
        instanceId = data["instanceId"] 
        ownerId = data["ownerId"]
        timestamp = data["ts"]
        status = data["state"].lower()
        t = data["date"]


        
        id = instanceId + " " + ownerId + " " + str(timestamp)

        try:
            current = instance[id]
            # if were wereto do a data base this line needs to be replaced
        except:
            current = data
            
#        current["ts"] = timestamp

        if not ("t_end" in current):
        #time in the future
            f = data["date"] + relativedelta( year = +10 )

            current["trace"] = { "pending" : {"start" : f, "stop": t}, "teardown" : {"start" : f, "stop": t}, "extant" : {"start" : f, "stop": t} }
            current["t_end"] = current["date"]
            current["t_start"] = current["ts"] # for naming consitency
            current["duration"] = 0.0
            
        (tmp, current["t_end"]) = minmax_time(current["t_end"], t)
        (current["trace"][status]["start"],b) = minmax_time(current["trace"][status]["start"],t)
        (a,current["trace"][status]["stop"]) = minmax_time(current["trace"][status]["stop"],t)
        

        instance[id] = current



def calculate_delta (instances):
    """calculates how long each instance runs in seconds"""
    for i in instances:
        values = instances[i]
        t_delta = values["t_end"] - values["ts"]
        instances[i]["duration"] = str(t_delta.total_seconds())

######################################################################
# GENERATE USER STATISTICS
######################################################################




# Create a chart object of 250x100 pixels

def display_user_stats(users,type="pie"):
    """displays the number of VMs a user is running"""
    values = []
    label_values = []

    max_v = 0
    for name in users:
        count = users[name][0]
        values.append(count)
        label_values.append(name + ":" + str(count))
        max_v = max(max_v, count)

    print values
    print label_values

    if type == "pie": 
        chart = PieChart3D(500, 200)
        chart.set_pie_labels(label_values)
    if type == "bar":
        chart = StackedHorizontalBarChart(500,200,
                                        x_range=(0, max_v))
        # the labels seem wrong, not sure why i have to call reverse
        chart.set_axis_labels('y', reversed(label_values))
        # setting the x axis labels
        left_axis = range(0, max_v + 1, 1)
        left_axis[0] = ''
        chart.set_axis_labels(Axis.BOTTOM, left_axis)

        chart.set_bar_width(10)
        chart.set_colours(['00ff00', 'ff0000'])

    # Add some data
    chart.add_data(values)

    # Assign the labels to the pie data


    # Print the chart URL
    url = chart.get_url()


    os.system ("open -a /Applications/Safari.app " + '"' + url + '"')

def calculate_user_stats (instances,users):
    """calculates some elementary statusticks about the instances per user: count, min time, max time, avg time, total time"""
    for i in instances:
        values = instances[i]
        name = values["ownerId"]
        t_delta = float(values["duration"])
        try:
            users[name][0] = users[name][0] + 1 # number of instances
        except:
            #          count,sum,min,max,avg
            users[name] = [1,0.0,t_delta,t_delta,0.0]

        users[name][1] = users[name][1] + t_delta  # sum of time 
        if t_delta < users[name][2]: # min
            users[name][2] = t_delta
        if t_delta > users[name][3]: # mmax
            users[name][3] = t_delta
    for name in users:
        users[name][4] = float(users[name][1]) / float(users[name][0])
 
######################################################################
# CONVERTER 
######################################################################


        
def convert_data_to_list(data,attribute):
    rest = data[attribute]
    rest = re.sub(" ","' , '", rest)
    rest = "['" + rest[1:-1] + "']"
    restdata = eval(rest)
    data[attribute] = restdata

def convert_data_to_dict(data,attribute):
    rest = data[attribute]
    rest = convert_str_to_dict_str(rest[1:-1])
    restdata = eval(rest)
    data[attribute] = restdata

def convert_str_to_dict_str(line):
    line = re.sub(' +',' ',line)
    line = line.strip(" ")
    line = re.sub(' ',',',line)

    # more regular dict
    line = re.sub('=','\'=\'',line)
    line = re.sub(',','\',\'',line)
    line = re.sub('=',' : ',line)
    return '{\'' + line + '\'}'

def parse_type_and_date(line,data):
    # split line after the third ] to (find date, id, msgtype)
    # put the rest in the string "rest"
    m = re.search( r'\[(.*)\]\[(.*)\]\[(.*)\](.*)', line, re.M|re.I)
    data['date'] = datetime.strptime(m.group(1), '%a %b %d %H:%M:%S %Y')
    data['id']   = m.group(2)
    data['msgtype'] = m.group(3)
    rest =  m.group(4)
    rest = re.sub(' +}','}',rest).strip()

    if rest.startswith("running"):
        data['linetype'] = "running"
        return rest 
    elif rest.startswith("calling"):
        data['linetype'] = "calling"
        return rest 
    else:
        location = rest.index(":")
        linetype = rest[0:location]
        data['linetype'] = re.sub('\(\)','',linetype).strip()
        rest = rest[location+1:].strip()
    return rest


def ccInstance_parser(rest,data):
    """parses the line and returns a dict"""

    # replace print_ccInstance(): with linetype=print_ccInstance
    #rest = rest.replace("print_ccInstance():","linetype=print_ccInstance")
    # replace refreshinstances(): with calltype=refresh_instances


    #RunInstances():
    rest = rest.replace("RunInstances():","calltype=run_instances")   # removing multiple spaces
    rest = rest.replace("refresh_instances():","calltype=refresh_instances")   # removing multiple spaces

    #separate easy assignments from those that would contain groups, for now simply put groups as a string
    # all others are merged into a string with *=* into rest
    m = re.search( r'(.*)keyName=(.*)ccnet=(.*)ccvm=(.*)ncHostIdx=(.*)volumes=(.*)groupNames=(.*)', rest, re.M|re.I)
    data['keyName'] = m.group(2).strip()
    data["ccnet"] = m.group(3).strip()
    data["ccvm"] = m.group(4).strip()
    data["volumes"] = m.group(6).strip()
    data["groupNames"] = m.group(7).strip()
    # assemble the rest string
    rest = m.group(1) + "ncHostIdx=" +m.group(5)

    # GATHER ALL SIMPLE *=* assignments into a single rest line and add each entry to dict via eval
    rest = convert_str_to_dict_str(rest)
    restdata = eval (rest)
    data.update(restdata)

    # convert ccvm and ccnet to dict
    convert_data_to_dict(data,"ccvm")
    convert_data_to_dict(data,"ccnet")

    # converts volumes and groupNAmes to list
    convert_data_to_list(data,"groupNames")
    convert_data_to_list(data,"volumes")

    # convert the timestamp
    data["ts"] = datetime.fromtimestamp(int(data["ts"]))


    return data

def refresh_resource_parser(rest,data):
    #[Wed Nov  9 19:50:08 2011][008128][EUCADEBUG ] refresh_resources(): received data from node=i2 mem=24276/22740 disk=306400/305364 cores=8/6
    if (rest.find("received") > -1):
        rest = re.sub("received data from","",rest).strip()
    # node=i2 mem=24276/22740 disk=306400/305364 cores=8/6
        m = re.search( r'node=(.*) mem=(.*)[/](.*) disk=(.*)/(.*) cores=(.*)/(.*)', rest, re.M|re.I)
        data["node"] = m.group(1)
        data["mem"] = m.group(2)
        data["mem_max"] = m.group(3)
        data["disk"] = m.group(4)
        data["disk_max"] = m.group(5)
        data["cores"] = m.group(6)
        data["cores_max"] = m.group(7)
    else:
        data["calltype"] = "ignore" 
    return data

    return data


def terminate_instances_param_parser(rest,data):

    rest = rest.strip()
    if rest.startswith("params"):
#params: userId=(null), instIdsLen=1, firstInstId=i-417B07B2

        rest = re.sub("params:","",rest).strip()
    # node=i2 mem=24276/22740 disk=306400/305364 cores=8/6
        m = re.search( r'userId=(.*) instIdsLen=(.*) firstInstId=(.*)', rest, re.M|re.I)
        userid = m.group(1)
        if userid == "(null),":
            data["userId"] = "null"
        else:
            data["userId"] = m.group(1)
        data["instIdsLen"] = m.group(2)
        data["firstInstId"] = m.group(3)
    else:
        data["calltype"] = "ignore" 
    return data



def print_counter (label,counter):
    print label + " = " + str(counter)

def parse_file (filename,analyze,debug=False,progress=True):
    f = open(filename, 'r')
    lines_total = 0
    lines_ignored = 0
    count_terminate_instances = 0
    count_refresh_resource = 0
    count_ccInstance_parser = 0 
    read_bytes = 0
    file_size = os.path.getsize(filename)
    if debug:
        print "SIZE>:" + str(file_size)

    progress_step = file_size / 100
    for line in f:
        ignore = False
        lines_total += 1
        read_bytes += len(line)
        if (debug or progress) and ((lines_total % 1000) == 0):
            percent = int(100 * read_bytes / file_size ) 
            sys.stdout.write("\r%2d%%" % percent)
            sys.stdout.flush()
        if debug:
            print "DEBUG " + str(lines_total) +"> " + line
        data = {}
        rest = parse_type_and_date (line, data)
        if data["linetype"] == "TerminateInstances":
            count_terminate_instances += 1
            terminate_instances_param_parser(rest, data)
        elif data["linetype"] == "refresh_resources":
            count_refresh_resource += 1
            refresh_resource_parser(rest, data)
        elif data["linetype"] == "print_ccInstance":
            count_ccInstance_parser += 1
            ccInstance_parser(rest, data)
        else:
            ignore = True
        if ignore:
            lines_ignored +=1
            if debug:
                print "IGNORE> " + line
        else:
            analyze(data)

    print_counter("lines total",lines_total)
    print_counter ("lines ignored = ", lines_ignored)
    print_counter("count_terminate_instances",count_terminate_instances)
    print_counter("count_refresh_resource",count_refresh_resource)
    print_counter("count_ccInstance_parser ",count_ccInstance_parser )

           
    return

#
#####################################################################
# MAIN
#####################################################################
def parse_test(f, line):
    print "------------------------------------------------------------"
    print "- parsetest: " + str(f)
    print "------------------------------------------------------------"
    print "INPUT>"
    print line
    data = {}
    # parse_type_and_date(line,data,rest)
    rest = parse_type_and_date (line, data)
    print "REST>"
    print rest
    f(rest, data)
    print "OUTPUT>"
    print json.dumps(data, sort_keys=False, indent=4)


def test1():
    parse_test(ccInstance_parser, 
               "[Wed Nov  9 19:58:12 2011][008128][EUCADEBUG ] print_ccInstance(): refresh_instances():  instanceId=i-42BA06B1 reservationId=r-3D3306BC emiId=emi-0B951139 kernelId=eki-78EF12D2 ramdiskId=eri-5BB61255 emiURL=http://149.165.146.135:8773/services/Walrus/centos53/centos.5-3.x86-64.img.manifest.xml kernelURL=http://149.165.146.135:8773/services/Walrus/xenkernel/vmlinuz-2.6.27.21-0.1-xen.manifest.xml ramdiskURL=http://149.165.146.135:8773/services/Walrus/xeninitrd/initrd-2.6.27.21-0.1-xen.manifest.xml state=Extant ts=1320693195 ownerId=sharif keyName=ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCp13CbKJLtKG5prGiet/VHct36CXzcpBKVgYsh/lxIXWKuositayvvuKux+I5GZ9bFWzMF71xAjmFinmAT3FXFKMd54FebPKZ2kBPCRqtmxz2jT1SG4hy1g1eDPzVX+qt5w8metAs7W//BCaBvWpU5IBuKSNqxO5OUIjIKkw3xkSswRpqSzrUBAmQP7e4dzQvmhqIxq4ZWqcEIWsAik0fSODTipa+Z6DvVKe02f5OtdUsXzz7pIivZ3qRGQveI5SOTdgFPqG+VglMsPURLbFFVWW1l51gCmRUwTf9ClySshSpkpAtaOx/OApQoII/vJxgr/EdYPOu1QLkubS4XH6+Z sharif@eucalyptus ccnet={privateIp=10.0.4.4 publicIp=149.165.159.130 privateMac=D0:0D:42:BA:06:B1 vlan=10 networkIndex=4} ccvm={cores=1 mem=512 disk=5} ncHostIdx=24 serviceTag=http://i1:8775/axis2/services/EucalyptusNC userData= launchIndex=0 volumesSize=0 volumes={} groupNames={sharifnew }")

    return

def test2():
    #
    # RESOURCE PARSER
    #

    parse_test(refresh_resource_parser, 
               "[Wed Nov  9 22:52:10 2011][008128][EUCAERROR ] refresh_resources(): bad return from ncDescribeResource(i23) (1)")
    parse_test(refresh_resource_parser, 
               "[Wed Nov  9 22:52:11 2011][008128][EUCADEBUG ] refresh_resources(): done")
    parse_test(refresh_resource_parser, 
               "[Wed Nov  9 22:52:19 2011][008128][EUCAINFO  ] refresh_resources(): called")
    parse_test(refresh_resource_parser, 
               "[Wed Nov  9 19:50:08 2011][008128][EUCADEBUG ] refresh_resources(): received data from node=i2 mem=24276/22740 disk=306400/305364 cores=8/6")


    return

def test3():
    #
    # TerminateInstance Parser
    #
    parse_test(terminate_instances_param_parser,
               "[Thu Nov 10 10:14:37 2011][021251][EUCADEBUG ] TerminateInstances(): params: userId=(null), instIdsLen=1, firstInstId=i-417B07B2")

    parse_test(terminate_instances_param_parser,
               "[Thu Nov 10 13:04:16 2011][016124][EUCADEBUG ] TerminateInstances(): done.")

    parse_test(terminate_instances_param_parser,
               "[Thu Nov 10 13:04:16 2011][016168][EUCAINFO  ] TerminateInstances(): called")
    return

def test4():
    parse_file ("/tmp/cc.log.4",jason_dump,debug=False)
    return

def test5(filename,progress=True):
    parse_file (filename,generate_instance_info,debug=False,progress=progress)
    calculate_delta (instance)
    print instance
    print instance_json_dump (instance)
    print json.dumps(instance, sort_keys=False, indent=4)
    print "total instances = " + str(len(instance))
    return

def test6():
    calculate_user_stats (instance,users)
    print json.dumps(users, sort_keys=False, indent=4)
    print "total users = " + str(len(users))
    return

def test_display():
    display_user_stats (users)
    display_user_stats (users, type="bar")

def main():



    if sys.version_info < (2, 7):
        print "ERROR: you must use python 2.7 or greater"
        exit (1)
    else:
        print "Python version: " + str(sys.version_info)

    clear()
    
    # test1()
    # test2()
    # test3()


    test5("/tmp/cc.log.4",progress=True)
    #test5("/tmp/cc.log.prints_cc",progress=True)
    
    #test6()
    #    test_display()
    #   




if __name__ == "__main__":
    main()
