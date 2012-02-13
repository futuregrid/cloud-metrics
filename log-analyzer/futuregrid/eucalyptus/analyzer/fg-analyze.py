#! /usr/bin/env python
import fg-parser




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

