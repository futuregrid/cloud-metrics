import paramiko
from datetime import datetime
from fgmetric.realtime.FGMongodb import FGMongodb

class FGMonitor:

    def __init__(self):
        self.data = {}
    def get_clusters(self):
        return [{"service": "openstack",
                "hostname": "india.futuregrid.org"}]

    def get_floatingIPs(self):
        '''Display a list of all floating IP addresses.'''

        clusters = self.get_clusters()
        for cluster in clusters:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.WarningPolicy())
            ssh.connect(hostname=cluster["hostname"], username="hrlee", key_filename="/home/hyungro/.ssh/.i")
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("ssh i50 sudo nova-manage floating list")

            for line in ssh_stdout.readlines():
                column = line.split("\t")
                try:
                    res.append({"ip":column[1], "instanceid":column[2]})
                except:
                    res = [{"ip":column[1], "instanceid":column[2]}]

            cluster["data"] = res
            cluster["time"] = datetime.now()

        self.data['floatingIPs'] = clusters
        return clusters

    def get_computenodes(self):
        '''Display a list of all compute nodes.'''

        clusters = list(self.get_clusters()) # copy new list
        for cluster in clusters:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.WarningPolicy())
            ssh.connect(hostname=cluster["hostname"], username="hrlee", key_filename="/home/hyungro/.ssh/.i")
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("ssh i50 sudo nova-manage service list|grep nova-compute")

            for line in ssh_stdout.readlines():
                column = line.split()
                try:
                    res.append({"node":column[1], "status":column[3], "state": column[4]})
                except:
                    res = [{"node":column[1], "status":column[3], "state": column[4]}]

            cluster["data"] = res
            cluster["time"] = datetime.now()

        self.data['computenodes'] = clusters
        return clusters

if __name__ == "__main__":
    fgmonitor = FGMonitor()
    fgmongodb = FGMongodb()
    fgmongodb.connect()
    res = fgmonitor.get_floatingIPs()
    fgmongodb.insert("floatingip", res)
    res = fgmonitor.get_computenodes()
    fgmongodb.insert("computenodes", res)

