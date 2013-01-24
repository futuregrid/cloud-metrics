import sys
import pymongo

class FGMongodb:
    def __init__(self):
        # If your database server is running in auth mode, you will need user and
        # database info. Ex:
        #    mongodb_uri = 'mongodb://username:password@localhost:27017/dbname'
        #
        self.mongodb_uri = 'mongodb://fgcloudadmin:fg-metric@ds035167.mongolab.com:35167/fgcloudmetrics'
        self.db_name = 'fgcloudmetrics'

    def connect(self):
        # pymongo.Connection creates a connection directly from the URI, performing
        # authentication using the provided user components if necessary.
        #
        try:
            self.connection = pymongo.Connection(self.mongodb_uri)
            self.database = self.connection[self.db_name]
        except:
            print('Error: Unable to connect to database.')
            self.connection = None

    def insert(self, collection, data):
        # What follows is insert, update, and selection code that can vary widely
        # depending on coding style.
        #
        if self.connection is not None:
            
            # To begin with, we'll add a few adventurers to the database. Note that
            # nothing is required to create the adventurers collection--it is
            # created automatically when we insert into it. These are simple JSON 
            # objects.
            #
            func = getattr(self.database, collection)
            func.insert(data)
            '''{'service': 'openstack',
                                        'cluster': 'india',
                                        'list': { data },
                                        'date': now })
            '''

    def update(self, collection, data):
        if self.connection is not None:
        # Because it seems we forgot to equip Mordo, we'll need to get him 
        # ready. Note the dot notation used to address the 'main-hand' key.
        # Don't send a JSON object describing the 'main-hand' key in the 
        # context of the 'equipment' key, or MongoDB will overwrite the other 
        # keys stored under 'equipment'. Mordo would be embarassed without 
        # armor.
        #
        # Note that in python, MongoDB $ operators should be quoted.
        #
        #database.adventurers.update({'name': 'Mordo' },
        #                            {'$set': {'equipment.main-hand': 'staff'}})
        
        # Now that everyone's ready, we'll send them off through standard 
        # output. Unfortunately this adventure is is for adventurers level 10 
        # or higher. We pass a JSON object describing our query as the value
        # of the key we'd like to evaluate.
        #
            return

    def find(self, query):

        #party = database.adventurers.find({'level': {'$gte': 10}})
    
        # Our query returns a Cursor, which can be counted and iterated 
        # normally.
        #
        if party.count() > 0:
            print('The quest begins!')
            for adventurer in party:
                print('%s, level %s %s, departs wearing %s and wielding a %s and %s.'
                       % ( adventurer['name'], adventurer['level'],
                           adventurer['class'],
                           adventurer['equipment']['armor'],
                           adventurer['equipment']['main-hand'],
                           adventurer['equipment']['off-hand'] ))
            print('Good luck, you %s brave souls!' % party.count())
        else:
            print('No one is high enough level!')
       
    def drop(self, collection):
        # Since this is an example, we'll clean up after ourselves.
        #database.drop_collection('adventurers')
        return
