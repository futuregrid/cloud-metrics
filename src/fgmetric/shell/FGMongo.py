import yaml
from pymongo import MongoClient

class FGMongo:
    def load_db_info(self):
        """Read database information such as hostname, user id, password, and
        database name"""
        stream = open("dbinfo.yaml", "r")
        self.dbinfo = yaml.load(stream)

    def connect_pymongo(self, hostname="localhost", port_number=27017):
        return MongoClient(host=hostname, port=port_number)

    def connect(self):
        self.client = self.connect_pymongo(self.dbinfo["mongodb_hostname"],
                                         self.dbinfo["mongodb_port"])

    def open_pymongodb(self, conn, db_name):
        return conn[db_name]

    def open_db(self):
        self.db = self.open_pymongodb(self.client, self.dbinfo["mongodb_dbname"])

    def open_pymongo_collection(self, db_conn, collection_name):
        return db_conn[collection_name]

    def open_collection(self):
        self.collection = self.open_pymongo_collection(self.db,
                                                       "instance_faults")
        # For test, I use instance_faults collection to look at

    def get_single(self, _dict={}):
        return self.collection.find_one(_dict)

    def get_(self, _dict={}):
        return self.collection.find(_dict)

    def get_count(self, _dict={}):
        if _dict:
            return self.collection.find(_dict).count()
        return self.collection.count()
