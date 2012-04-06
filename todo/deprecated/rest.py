#
# SQL
#
"""
keynames = ()
values = ()

def getsql(key, values)
    i = index(key,keynames)
    return values[i]

def get(key, values)
    sqlkey = datakey(key)
    return getsql(sqlkey,values)

get(["tarce"]["teardown"]["start"]', values)

value = a
key = ["tarce"]["teardown"]["start"]'
eval (instance key = value)

instance["tarce"]["teardown"]["start"]' = value



def sqlkey(string)
    # '["tarce"]["teardown"]["start"]'
    string = re.sub("][", "_", string)
    string = re.sub("]", "", string)
    string = re.sub("[", "", string)
    string = re.sub('"', "", string)
    string = re.sub("'", "", string)
    return string

def datakey(string)
    # trace_teardown_start
    string = re.sub("_",'"]["', string)
    string = "['" + string + "']"
    return string

data
        'trace': {
            'teardown': {
                'start': '2011-11-10 10:06:58', 
                'stop': '2011-11-10 10:10:02'
            }, 

sql
        trace_teardown_start: '2011-11-10 10:06:58', 
        trace_teardown_start: '2011-11-10 10:10:02'

data
"groupNames": [
            "sharifnew",             "sharifnewa"
        ], 

sql
"groupNames": sharifnew sharifnewa
        

def emptyData():
return data


def writetodb(data):
    return


def finddata (is, timestamp, user):
    #    return object to pass to data_from_db
    return
    
def fromdb(data_from_db):
    data{}
    return data
"""
