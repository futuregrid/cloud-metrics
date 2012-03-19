#! /usr/bin/env python
import fg-parser

''' output (CSV type) for 'used minutes by users' and 'number of running instances per user' graphs are expected like below.

Year, Month, Day, ownerId, used minutes, number of running instances, instances
2012,02,11,admin,1440,1,i-51230A25
2012,02,11,inca,25,3,i-3F11078B;i-50230963;i-593009E3
2012,02,11,jiaazeng,11520,8,i-274B0603;i-34B706F0;i-355906E0;i-3F81078E;i-4A390892;i-4CC608BE;i-523C0905;i-547008E6
2012,02,11,vahi,2880,2,i-457108AE;i-4F9D0896
2012,02,11,xiuwyang,1440,1,i-37F00737
2012,02,12,admin,1413,1,i-51230A25
2012,02,12,inca,49,7,i-349A0753;i-3F4607A3;i-400B0740;i-402F07B3;i-4162081F;i-48ED0853;i-4BFE07F0
2012,02,12,jiaazeng,11303,8,i-274B0603;i-34B706F0;i-355906E0;i-3F81078E;i-4A390892;i-4CC608BE;i-523C0905;i-547008E6
2012,02,12,vahi,2826,2,i-457108AE;i-4F9D0896
2012,02,12,xiuwyang,2374,5,i-37F00737;i-393D0638;i-448707B6;i-48660854;i-4BA708F7

How to get the result above from cc.log?
----------------------------------------
1) Collect lines that have 'print_ccInstance(): refresh_instances():'
2) if an instance is down (state=Teardown), get minutes by (endtime - start time)
* start time => (ts=)
* end time => log date time which occurs first in the order of lines
3) Save the minutes (result array -> date -> ownerId -> used minutes)
4) if an instance is alive (state=Extant), get minutes by (current time or last time of log - start time)
5) add the minutes to the result array
6) instance ids are collected (instanceId=) for displaying a number of running instances.
'''



data =
{
    "calltype": "refresh_instances", 
    "userData": "", 
    "kernelId": "eki-78EF12D2", 
    "emiURL": "http://149.165.146.135:8773/services/Walrus/centos53/centos.5-3.x86-64.img.manifest.xml", 
    "serviceTag": "http://i1:8775/axis2/services/EucalyptusNC", 
    "instanceId": "i-42BA06B1", 
    "ts": "1320693195", 
    "groupNames": [
        "sharifnew"
    ], 
    "keyName": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCp13CbKJLtKG5prGiet/VHct36CXzcpBKVgYsh/lxIXWKuositayvvuKux+I5GZ9bFWzMF71xAjmFinmAT3FXFKMd54FebPKZ2kBPCRqtmxz2jT1SG4hy1g1eDPzVX+qt5w8metAs7W//BCaBvWpU5IBuKSNqxO5OUIjIKkw3xkSswRpqSzrUBAmQP7e4dzQvmhqIxq4ZWqcEIWsAik0fSODTipa+Z6DvVKe02f5OtdUsXzz7pIivZ3qRGQveI5SOTdgFPqG+VglMsPURLbFFVWW1l51gCmRUwTf9ClySshSpkpAtaOx/OApQoII/vJxgr/EdYPOu1QLkubS4XH6+Z sharif@eucalyptus", 
    "msgtype": "EUCADEBUG ", 
    "volumesSize": "0", 
    "linetype": "print_ccInstance", 
    "ownerId": "sharif", 
    "date": "2011-11-09 19:58:12", 
    "id": "008128", 
    "ncHostIdx": "24", 
    "ccvm": {
        "mem": "512", 
        "cores": "1", 
        "disk": "5"
    }, 
    "emiId": "emi-0B951139", 
    "ccnet": {
        "publicIp": "149.165.159.130", 
        "privateMac": "D0:0D:42:BA:06:B1", 
        "networkIndex": "4", 
        "vlan": "10", 
        "privateIp": "10.0.4.4"
    }, 
    "ramdiskURL": "http://149.165.146.135:8773/services/Walrus/xeninitrd/initrd-2.6.27.21-0.1-xen.manifest.xml", 
    "state": "Extant", 
    "kernelURL": "http://149.165.146.135:8773/services/Walrus/xenkernel/vmlinuz-2.6.27.21-0.1-xen.manifest.xml", 
    "ramdiskId": "eri-5BB61255", 
    "volumes": [
        ""
    ], 
    "launchIndex": "0", 
    "reservationId": "r-3D3306BC"
}


counter = 0

def analyze_ccInstances(data):
    counter += 1
    db[counter] = data
    return


def main:
    parse_file(cc.log,analyze_ccInsces)


Instance = {}

array of instances

f = file contains all log entries

while line in f
   data = parse line

   if thi happens 
     put data from line into the instance

acuumulated time [user]


def print accumulated time for users
   for user in users
     print accumuluated time [user]


for instance in instances {

    instance["start vm"] = time a
    instance["end vm"] = time b
    instance["userid"]="gergor"

}

printnicely (instance)
  print instance["start vm"], instance["end vm"],  instance["userid"]

