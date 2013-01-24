import paramiko
from datetime import datetime
from fgmonitor.FGMongodb import FGMongodb

class FGMonitor:
    def get_clusters(self):
        return [{"sevice": "openstack",
                "hostname": "india.futuregrid.org"}]

    def get_floatingIPs(self):
        '''Displays a list of all floating IP addresses.'''

        clusters = self.get_clusters()
        for cluster in clusters:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
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

        self.data = clusters
        return self.data

if __name__ == "__main__":
    fgmonitor = FGMonitor()
    fgmonitor.get_floatingIPs()
    fgmongodb = FGMongodb()
    fgmongodb.connect()
    fgmongodb.insert("floatingip", fgmonitor.data)
    #print fgmonitor.data


    
