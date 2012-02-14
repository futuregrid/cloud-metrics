#! /usr/bin/env python

# sudo easy_install -U GChartWrapper
from GChartWrapper import Pie3D
from GChartWrapper import HorizontalBarGroup
# http://code.google.com/p/google-chartwrapper/

import re
import json
import sys
import os
from datetime import datetime

users = {}
instance = {}



def print_instance_info (data):

    if data["linetype"] == "print_ccInstance":
        instanceId = data["instanceId"] 
        ownerId = data["ownerId"]
        timestamp = str(datetime.fromtimestamp(int(data["ts"])))

        id = instanceId + " " + ownerId
        try:
            end_t = instance[id](0)
            if end_t < data["date"]:
                end_t = data["date"]
            instance[id] = (data["date"], timestamp, data["instanceId"], data["ownerId"])
            print  end_t
        except:
            instance[id] = (data["date"], timestamp, data["instanceId"], data["ownerId"])

def calculate_delta (instances):
    for i in instances:
        values = instances[i]
        t_start = datetime.strptime(values[1], '%Y-%m-%d %H:%M:%S') # convert to datetime
        t_end = datetime.strptime(values[0], '%Y-%m-%d %H:%M:%S') # convert to datetime
        t_delta = t_end - t_start
        instances[i] += (str(t_delta.total_seconds()),)

def display_user_stats(users,type="pie"):
    values = []
    label_values = []

    for name in users:
        count = users[name][0]
        values.append(count)
        label_values.append(name + ":" + str(count))
    print values

    # cant get the label values to work so I cheat with eval
    # G=  Pie3D(values).title("Number of Instances").color("red","lime").label(label_values)

    label_values_str = str(label_values)[1:-1]
    values_str = str(values)
    if type == "pie": 
        command = "Pie3D(" + values_str + ').title("Number of Instances").color("red","lime").label(' + label_values_str +')'
        print command
        G = eval(command)
        # end of cheat 
        G.color('green')

    os.system ("open -a /Applications/Safari.app " + '"' + str(G) + '"')

def calculate_user_stats (instances,users):
    for i in instances:
        values = instances[i]
        name = values[3]
        t_delta = float(values[4])
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
    data['date'] = str(datetime.strptime(m.group(1), '%a %b %d %H:%M:%S %Y'))
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


def pretty_print(data):
    print json.dumps(data, sort_keys=False, indent=4)            

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

def main():



    if sys.version_info < (2, 7):
        print "ERROR: you must use python 2.7 or greater"
        exit (1)
    else:
        print "Python version: " + str(sys.version_info)

    parse_test(ccInstance_parser, 
               "[Wed Nov  9 19:58:12 2011][008128][EUCADEBUG ] print_ccInstance(): refresh_instances():  instanceId=i-42BA06B1 reservationId=r-3D3306BC emiId=emi-0B951139 kernelId=eki-78EF12D2 ramdiskId=eri-5BB61255 emiURL=http://149.165.146.135:8773/services/Walrus/centos53/centos.5-3.x86-64.img.manifest.xml kernelURL=http://149.165.146.135:8773/services/Walrus/xenkernel/vmlinuz-2.6.27.21-0.1-xen.manifest.xml ramdiskURL=http://149.165.146.135:8773/services/Walrus/xeninitrd/initrd-2.6.27.21-0.1-xen.manifest.xml state=Extant ts=1320693195 ownerId=sharif keyName=ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCp13CbKJLtKG5prGiet/VHct36CXzcpBKVgYsh/lxIXWKuositayvvuKux+I5GZ9bFWzMF71xAjmFinmAT3FXFKMd54FebPKZ2kBPCRqtmxz2jT1SG4hy1g1eDPzVX+qt5w8metAs7W//BCaBvWpU5IBuKSNqxO5OUIjIKkw3xkSswRpqSzrUBAmQP7e4dzQvmhqIxq4ZWqcEIWsAik0fSODTipa+Z6DvVKe02f5OtdUsXzz7pIivZ3qRGQveI5SOTdgFPqG+VglMsPURLbFFVWW1l51gCmRUwTf9ClySshSpkpAtaOx/OApQoII/vJxgr/EdYPOu1QLkubS4XH6+Z sharif@eucalyptus ccnet={privateIp=10.0.4.4 publicIp=149.165.159.130 privateMac=D0:0D:42:BA:06:B1 vlan=10 networkIndex=4} ccvm={cores=1 mem=512 disk=5} ncHostIdx=24 serviceTag=http://i1:8775/axis2/services/EucalyptusNC userData= launchIndex=0 volumesSize=0 volumes={} groupNames={sharifnew }")


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

    #
    # TerminateInstance Parser
    #
    parse_test(terminate_instances_param_parser,
               "[Thu Nov 10 10:14:37 2011][021251][EUCADEBUG ] TerminateInstances(): params: userId=(null), instIdsLen=1, firstInstId=i-417B07B2")

    parse_test(terminate_instances_param_parser,
               "[Thu Nov 10 13:04:16 2011][016124][EUCADEBUG ] TerminateInstances(): done.")

    parse_test(terminate_instances_param_parser,
               "[Thu Nov 10 13:04:16 2011][016168][EUCAINFO  ] TerminateInstances(): called")


#    parse_file ("/tmp/cc.log.4",pretty_print,debug=False)

    parse_file ("/tmp/cc.log.prints_cc",print_instance_info,debug=False)

    print json.dumps(instance, sort_keys=False, indent=4)

    calculate_delta (instance)

    print json.dumps(instance, sort_keys=False, indent=4)
    print "total instances = " + str(len(instance))


    calculate_user_stats (instance,users)
    print json.dumps(users, sort_keys=False, indent=4)
    print "total users = " + str(len(users))
    #   

    display_user_stats (users)



if __name__ == "__main__":
    main()
