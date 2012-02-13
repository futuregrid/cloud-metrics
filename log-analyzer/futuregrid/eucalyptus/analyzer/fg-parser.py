#! /usr/bin/env python
import re
import json
import sys
from datetime import datetime

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
    rest = re.sub(' +}','}',rest)
    location = rest.index(":")
    linetype = rest[0:location]
    data['linetype'] = re.sub('\(\)','',linetype).strip()
    rest = rest[location+1:].strip()
    return rest


def ccInstance_parser(line):
    """parses the line and returns a dict"""
    data = {}

    # parse_type_and_date(line,data,rest)
    rest = parse_type_and_date (line, data)

    # replace print_ccInstance(): with linetype=print_ccInstance
    #rest = rest.replace("print_ccInstance():","linetype=print_ccInstance")
    # replace refreshinstances(): with calltype=refresh_instances
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

def refresh_resource_parser(line):
    #[Wed Nov  9 19:50:08 2011][008128][EUCADEBUG ] refresh_resources(): received data from node=i2 mem=24276/22740 disk=306400/305364 cores=8/6
    data = {}
    data["calltype"] = "refresh_resources" 
    rest = parse_type_and_date(line,data)
    rest = re.sub("refresh_resources\(\): received data from","",rest).strip()
    # node=i2 mem=24276/22740 disk=306400/305364 cores=8/6
    m = re.search( r'node=(.*) mem=(.*)[/](.*) disk=(.*)/(.*) cores=(.*)/(.*)', rest, re.M|re.I)
    data["node"] = m.group(1)
    data["mem"] = m.group(2)
    data["mem_max"] = m.group(3)
    data["disk"] = m.group(4)
    data["disk_max"] = m.group(5)
    data["cores"] = m.group(6)
    data["cores_max"] = m.group(7)

    return data


def terminate_instances_param_parser(line):
#[Thu Nov 10 10:14:37 2011][021251][EUCADEBUG ] TerminateInstances(): params: userId=(null), instIdsLen=1, firstInstId=i-417B07B2
    data = {}
    data["calltype"] = "terminate_instances_param" 
    rest = parse_type_and_date(line,data)
    rest = re.sub("TerminateInstances\(\): params:","",rest).strip()
    # node=i2 mem=24276/22740 disk=306400/305364 cores=8/6
    m = re.search( r'userId=(.*) instIdsLen=(.*) firstInstId=(.*)', rest, re.M|re.I)
    userid = m.group(1)
    if userid == "(null),":
        data["userId"] = "null"
    else:
        data["userId"] = m.group(1)
    data["instIdsLen"] = m.group(2)
    data["firstInstId"] = m.group(3)

    return data


#
#####################################################################
# MAIN
#####################################################################
def main():

    line = "[Wed Nov  9 19:58:12 2011][008128][EUCADEBUG ] print_ccInstance(): refresh_instances():  instanceId=i-42BA06B1 reservationId=r-3D3306BC emiId=emi-0B951139 kernelId=eki-78EF12D2 ramdiskId=eri-5BB61255 emiURL=http://149.165.146.135:8773/services/Walrus/centos53/centos.5-3.x86-64.img.manifest.xml kernelURL=http://149.165.146.135:8773/services/Walrus/xenkernel/vmlinuz-2.6.27.21-0.1-xen.manifest.xml ramdiskURL=http://149.165.146.135:8773/services/Walrus/xeninitrd/initrd-2.6.27.21-0.1-xen.manifest.xml state=Extant ts=1320693195 ownerId=sharif keyName=ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCp13CbKJLtKG5prGiet/VHct36CXzcpBKVgYsh/lxIXWKuositayvvuKux+I5GZ9bFWzMF71xAjmFinmAT3FXFKMd54FebPKZ2kBPCRqtmxz2jT1SG4hy1g1eDPzVX+qt5w8metAs7W//BCaBvWpU5IBuKSNqxO5OUIjIKkw3xkSswRpqSzrUBAmQP7e4dzQvmhqIxq4ZWqcEIWsAik0fSODTipa+Z6DvVKe02f5OtdUsXzz7pIivZ3qRGQveI5SOTdgFPqG+VglMsPURLbFFVWW1l51gCmRUwTf9ClySshSpkpAtaOx/OApQoII/vJxgr/EdYPOu1QLkubS4XH6+Z sharif@eucalyptus ccnet={privateIp=10.0.4.4 publicIp=149.165.159.130 privateMac=D0:0D:42:BA:06:B1 vlan=10 networkIndex=4} ccvm={cores=1 mem=512 disk=5} ncHostIdx=24 serviceTag=http://i1:8775/axis2/services/EucalyptusNC userData= launchIndex=0 volumesSize=0 volumes={} groupNames={sharifnew }"

    print line
    data = ccInstance_parser(line)
    print json.dumps(data, sort_keys=False, indent=4)

    line = "[Wed Nov  9 19:50:08 2011][008128][EUCADEBUG ] refresh_resources(): received data from node=i2 mem=24276/22740 disk=306400/305364 cores=8/6"
    print line
    data = refresh_resource_parser(line)
    print json.dumps(data, sort_keys=False, indent=4)

    line = "[Thu Nov 10 10:14:37 2011][021251][EUCADEBUG ] TerminateInstances(): params: userId=(null), instIdsLen=1, firstInstId=i-417B07B2"
    print line
    data = terminate_instances_param_parser(line)
    print json.dumps(data, sort_keys=False, indent=4)

if __name__ == "__main__":
    main()
