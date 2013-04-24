import os
from novaclient.v1_1 import client
#from novaclient import extension
#from novaclient.v1_1.contrib import instance_action

class NovaClientTest:

    def __init__(self):
        try:
            USER = os.environ["OS_USERNAME"]
            PASS = os.environ["OS_PASSWORD"]
            TENANT = os.environ["OS_TENANT_NAME"]
            AUTH_URL = os.environ["OS_AUTH_URL"]
        except:
            print "missing credential information in novarc"
            raise

        #extensions = [
        #        extension.Extension(instance_action.__name__.split(".")[-1],
        #                                                    instance_action),
        #]

        self.nt = client.Client(USER, PASS, TENANT, AUTH_URL,
                                service_type="compute")#, #extensions = extensions)

    def list_images(self):
        self.nt.images.list()

    def list_servers(self):
        servers = self.nt.servers.list()
        for server in servers:
            # server is a class in v1.1/server
            try:
                vars_dict = vars(server)
                print vars_dict
            except:
                pass
                #print vars(server)
