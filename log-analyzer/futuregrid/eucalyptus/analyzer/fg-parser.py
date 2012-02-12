#! /usr/bin/env python
import re

def print_ccInstance_parser(line):
    """parses the line and returns a dict"""
    data = {}
    data['test'] = "Hallo world"

    # split line after the third ]
    
    m = re.search( r'\[(.*)\]\[(.*)\]\[(.*)\](.*)', line, re.M|re.I)

    data['date'] = m.group(1)
    data['id']   = m.group(2)
    data['msgtype'] = m.group(3)
    rest =  m.group(4)
    # replace print_ccInstance(): with linetype=print_ccInstance
    rest = rest.replace("print_ccInstance():","linetype=print_ccInstance")
    # replace refreshinstances(): with calltype=refresh_instances
    rest = rest.replace("refresh_instances():","calltype=refresh_instances")   # removing multiple spaces
    rest = re.sub(' +',' ',rest)
    # replace " }" with "}"
    rest = re.sub(' +}','}',rest)
    # fix empty assignments with "= "
    rest = re.sub('= +','={} ',rest)
    
    print "----"
    print "RRRR" + rest
    print "----"
    # replace " " with ,
    # put { } around 
    # assign to the data via eval? not sure if things such as ccvm={ } would work, also groupnames and volumes are probably arrays 
    # this intermediate structure may be easier to parse

    return data


#####################################################################
# MAIN
#####################################################################
def main():
    line = "[Wed Nov  9 19:58:12 2011][008128][EUCADEBUG ] print_ccInstance(): refresh_instances():  instanceId=i-42BA06B1 reservationId=r-3D3306BC emiId=emi-0B951139 kernelId=eki-78EF12D2 ramdiskId=eri-5BB61255 emiURL=http://149.165.146.135:8773/services/Walrus/centos53/centos.5-3.x86-64.img.manifest.xml kernelURL=http://149.165.146.135:8773/services/Walrus/xenkernel/vmlinuz-2.6.27.21-0.1-xen.manifest.xml ramdiskURL=http://149.165.146.135:8773/services/Walrus/xeninitrd/initrd-2.6.27.21-0.1-xen.manifest.xml state=Extant ts=1320693195 ownerId=sharif keyName=ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCp13CbKJLtKG5prGiet/VHct36CXzcpBKVgYsh/lxIXWKuositayvvuKux+I5GZ9bFWzMF71xAjmFinmAT3FXFKMd54FebPKZ2kBPCRqtmxz2jT1SG4hy1g1eDPzVX+qt5w8metAs7W//BCaBvWpU5IBuKSNqxO5OUIjIKkw3xkSswRpqSzrUBAmQP7e4dzQvmhqIxq4ZWqcEIWsAik0fSODTipa+Z6DvVKe02f5OtdUsXzz7pIivZ3qRGQveI5SOTdgFPqG+VglMsPURLbFFVWW1l51gCmRUwTf9ClySshSpkpAtaOx/OApQoII/vJxgr/EdYPOu1QLkubS4XH6+Z sharif@eucalyptus ccnet={privateIp=10.0.4.4 publicIp=149.165.159.130 privateMac=D0:0D:42:BA:06:B1 vlan=10 networkIndex=4} ccvm={cores=1 mem=512 disk=5} ncHostIdx=24 serviceTag=http://i1:8775/axis2/services/EucalyptusNC userData= launchIndex=0 volumesSize=0 volumes={} groupNames={sharifnew }"

    print line
    print print_ccInstance_parser(line)

if __name__ == "__main__":
    main()
