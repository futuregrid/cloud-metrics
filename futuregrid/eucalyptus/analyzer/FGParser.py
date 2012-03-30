#! /usr/bin/env python

"""
MANUAL PAGE DRAFT

NAME - fg-euca-log-parser

DESCRIPTION

usage

<TBD>   cat filename.log | fg-euca-log-parser <parameters>


All log entries are included through a pipe into the program

fg-euca-log-parser

<TBD>  --nodb
      does not use the internal database, but just files

  --conf filename

      configuraton file of the database to be used. The configuration file has the following format

      [EucaLogDB]
      host=HOST
      port=PORT
      user=USER
      passwd=PASS
      db=DB

  if this parameter is not specified and a database is used the default location for this file is in

      ~/.futuregrid/futuregrid.cfg
      
  --cleardb

     This command without any parameter deletes the entire database.
     Be careful with this

<TBD>  --backup filename

     backups the database into a named file

<TBD>  --restore filename

      restores the database from the named file

  --parse type1 type2 ...

       if one of more types separated with space ar used, those types are
       parsed and included into the database, this parameter is optional and
       by default all types of interest are parsed. they are case insensitive

       types are print_ccInstance, refresh_resources

       BUG: Note the code does not yet analyse or store data
            from refresh resources. This was not our highest priority
       
       types we have not yet included include
          terminate_instances
          ....
          put all the other once we ignore here

  --from date_from --to date_to

     If a from and to date are specified in the following format: 2011-11-06 00:13:15
     all entries outside of these dates are ignored as part of the parsing step
     If no from and to are specified, all data is parsed

  
Usage tip:

using fgrep to search for the types before piping it into this program could
speed up processing. multiple files, can be concatenated simply with cat.
"""

from pygooglechart import PieChart3D, StackedHorizontalBarChart, Axis

import re
import json
import pprint
import sys
import os
from datetime import * 

import FGEucaMetricsDB
import FGGoogleMotionChart
        
class Instances:
    
    def __init__(self):
        self.clear()
        self.data

        self.in_the_future = datetime.strptime("3000-01-01 00:00:00", '%Y-%m-%d %H:%M:%S')
        self.pp = pprint.PrettyPrinter(indent=0)
        self.data = {}
        self.eucadb = FGEucaMetricsDB.FGEucaMetricsDB("futuregrid.cfg")
        self.withSQL = False
        self.first_date  = datetime.strptime("3000-01-01 00:00:00", '%Y-%m-%d %H:%M:%S')
        self.last_date = datetime.strptime("1981-01-01 00:00:00", '%Y-%m-%d %H:%M:%S')

    def clear(self):
        self.data = {}
        return

    def set_conf(filename):
	self.eucadb = FGEucaMetricsDB.FGEucaMetricsDB(filename)
	return

    def get(self):
        return self.data

    def getdata(self, i):
        return self.data[i]

    def print_total(self):
        print "total instances = " + self.count()

    def count(self):
        return str(len(self.data))

    def todatetime (self,instance):
        instance["trace"]["teardown"]["start"] = value_todate(instance["trace"]["teardown"]["start"])
        instance["trace"]["teardown"]["stop"] = value_todate(instance["trace"]["teardown"]["stop"])
        instance["trace"]["extant"]["start"] = value_todate(instance["trace"]["extant"]["start"])
        instance["trace"]["extant"]["stop"] = value_todate(instance["trace"]["extant"]["stop"])
        instance["trace"]["pending"]["start"] = value_todate(instance["trace"]["pending"]["start"])
        instance["trace"]["pending"]["stop"] = value_todate(instance["trace"]["pending"]["stop"])
        instance["t_start"] = value_todate(instance["t_start"])
        instance["date"] = value_todate(instance["date"])
        instance["t_end"] = value_todate(instance["t_end"])
        instance["ts"] = value_todate(instance["ts"])

    def tostr(self,instance):
        instance["trace"]["teardown"]["start"] = str(instance["trace"]["teardown"]["start"])
        instance["trace"]["teardown"]["stop"] = str(instance["trace"]["teardown"]["stop"])
        instance["trace"]["extant"]["start"] = str(instance["trace"]["extant"]["start"])
        instance["trace"]["extant"]["stop"] = str(instance["trace"]["extant"]["stop"])
        instance["trace"]["pending"]["start"] = str(instance["trace"]["pending"]["start"])
        instance["trace"]["pending"]["stop"] = str(instance["trace"]["pending"]["stop"])
        instance["ts"] = str(instance["ts"])
        instance["t_start"] = str(instance["t_start"])
        instance["date"] = str(instance["date"])
        instance["t_end"] = str(instance["t_end"])

    def value_todate(self,string):
        return datetime.strptime(string, '%Y-%m-%d %H:%M:%S')

    def dump(self,index = "all"):

        if index == "all" or (index == "") :
            for key in self.data:
                print "------------------------"
                pp.pprint(self.data[key])
            print "------------------------"
            self.print_total()
            print "------------------------"
        elif (index >= 0) and (index < len(str)):
            pp.pprint(self.data[index])
        else:
            print "ERROR printing of index " + index

    def print_list(self,index = "all"):

        if (index == "all") or (index == "") :
            for key in self.data:
                print(self.data[key]["instanceId"])
            print "------------------------"
            self.print_total()
            print "------------------------"
        elif (index >= 0) and (index < len(str)):
            print(self.data[index]["instanceId"])
        else:
            print "ERROR printing of index " + index

    def json_dump(self):
         string = ""
         for key in all:
            self.tostr (all[key])
         string = json.dumps(all, sort_keys=False, indent=4)
         for key in all:
             print all[key]
         self.todatetime (all[key])
         return string 

######################################################################
# SQL
######################################################################

    def read_from_db(self):
        key = 0 
        instance_list = self.eucadb.read()

        for element in instance_list:
            key += 1
            self.data[key] = element
        
    def write_to_db(self):
        for key_current in self.data:
            self.eucadb.write(self.data[key_current])

    def add (self,datarecord):
        """prints the information for each instance"""
        if datarecord["linetype"] == "print_ccInstance":
            instanceId = datarecord["instanceId"] 
            ownerId = datarecord["ownerId"]
            timestamp = datarecord["ts"]
            status = datarecord["state"].lower()
            t = datarecord["date"]

            id = instanceId + " " + ownerId + " " + str(timestamp)

            try:
                current = instance[id]
                # if were wereto do a data base this line needs to be replaced
            except:
                current = datarecord

            if not ("t_end" in current):
            #time in the future
                f = self.in_the_future

                current["trace"] = {
                    "pending" : {"start" : f, "stop": t},
                    "teardown" : {"start" : f, "stop": t},
                    "extant" : {"start" : f, "stop": t}
                    }
                current["t_end"] = current["date"]
                current["t_start"] = current["ts"] # for naming consitency
                current["duration"] = 0.0

            current["t_end"] = min(current["t_end"], t)
            current["trace"][status]["start"] = min(current["trace"][status]["start"],t)
            current["trace"][status]["stop"] = max(current["trace"][status]["stop"],t)

            instance[id] = current

            #        was calculate delta
    def refresh(self):
        """calculates how long each instance runs in seconds"""
        for i in self.data:
            values = self.data[i]
            t_delta = values["t_end"] - values["ts"]
            self.data[i]["duration"] = str(t_delta.total_seconds())

    def getDateRange(self):
	for i in self.data:
            element = self.data[i]
            if self.first_date > element["date"]:
                self.first_date = element["date"]
            if self.last_date < element["date"]:
                self.last_date = element["date"]
        return (str(self.first_date), str(self.last_date))

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
    try:
	    m = re.search( r'\[(.*)\]\[(.*)\]\[(.*)\](.*)', line, re.M|re.I)
	    data['date'] = datetime.strptime(m.group(1), '%a %b %d %H:%M:%S %Y')
	    data['id']   = m.group(2)
	    data['msgtype'] = m.group(3)
	    rest =  m.group(4)
	    rest = re.sub(' +}','}',rest).strip()
	    if rest.startswith("running"):
		    data['linetype'] = "running"
		    return rest 
	    elif rest.startswith("calling"):
		    data['linetype'] = "calling"
		    return rest 
	    else:
		    location = rest.index(":")
		    linetype = rest[0:location]
		    data['linetype'] = re.sub('\(\)','',linetype).strip()
		    rest = rest[location+1:].strip()
		    return rest
    except (ValueError, AttributeError):
	    data['linetype'] = "IGNORE"
	    return
    except:
	    data['linetype'] = "IGNORE"
	    return

def ccInstance_parser(rest,data):
    """parses the line and returns a dict"""

    # replace print_ccInstance(): with linetype=print_ccInstance
    #rest = rest.replace("print_ccInstance():","linetype=print_ccInstance")
    # replace refreshinstances(): with calltype=refresh_instances

    #RunInstances():
    rest = rest.replace("RunInstances():","calltype=run_instances")   # removing multiple spaces
    rest = rest.replace("refresh_instances():","calltype=refresh_instances")   # removing multiple spaces

    #separate easy assignments from those that would contain groups, for now simply put groups as a string
    # all others are merged into a string with *=* into rest
    m = re.search( r'(.*)keyName=(.*)ccnet=(.*)ccvm=(.*)ncHostIdx=(.*)volumes=(.*)groupNames=(.*)', rest, re.M|re.I)
    try:
	    data['keyName'] = m.group(2).strip()
	    data["ccnet"] = m.group(3).strip()
	    data["ccvm"] = m.group(4).strip()
	    data["volumes"] = m.group(6).strip()
	    data["groupNames"] = m.group(7).strip()
	    # assemble the rest string
	    rest = m.group(1) + "ncHostIdx=" +m.group(5)
    except:
	    return

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

    # convert the timestamp
    data["ts"] = datetime.fromtimestamp(int(data["ts"]))

    return data

def refresh_resource_parser(rest,data):
    #[Wed Nov  9 19:50:08 2011][008128][EUCADEBUG ] refresh_resources(): received data from node=i2 mem=24276/22740 disk=306400/305364 cores=8/6
    if (rest.find("received") > -1):
        rest = re.sub("received data from","",rest).strip()
    # node=i2 mem=24276/22740 disk=306400/305364 cores=8/6
        m = re.search( r'node=(.*) mem=(.*)[/](.*) disk=(.*)/(.*) cores=(.*)/(.*)', rest, re.M|re.I)
        data["node"] = m.group(1)
        data["mem"] = m.group(2)
        data["mem_max"] = m.group(3)
        data["disk"] = m.group(4)
        data["disk_max"] = m.group(5)
        data["cores"] = m.group(6)
        data["cores_max"] = m.group(7)
    else:
        data["calltype"] = "ignore" 
    return data

def terminate_instances_param_parser(rest,data):

    rest = rest.strip()
    if rest.startswith("params"):
	#params: userId=(null), instIdsLen=1, firstInstId=i-417B07B2
        rest = re.sub("params:","",rest).strip()
    	# node=i2 mem=24276/22740 disk=306400/305364 cores=8/6
        m = re.search( r'userId=(.*) instIdsLen=(.*) firstInstId=(.*)', rest, re.M|re.I)
        userid = m.group(1)
        if userid == "(null),":
            data["userId"] = "null"
        else:
            data["userId"] = m.group(1)
        data["instIdsLen"] = m.group(2)
        data["firstInstId"] = m.group(3)
    else:
        data["calltype"] = "ignore" 
    return data



def print_counter (label,counter):
    print label + " = " + str(counter)

def parse_file (filename, analyze, parse_types, debug=False, progress=True):
    print filename
    f = open(filename, 'r')
    lines_total = 0
    lines_ignored = 0
    count_terminate_instances = 0
    count_refresh_resource = 0
    count_ccInstance_parser = 0 
    read_bytes = 0
    file_size = os.path.getsize(filename)
    if debug:
        print "SIZE>:" + str(file_size)

    progress_step = file_size / 100
    for line in f:
        ignore = False
        lines_total += 1
        read_bytes += len(line)
        if (debug or progress) and ((lines_total % 1000) == 0):
            percent = int(100 * read_bytes / file_size ) 
            sys.stdout.write("\r%2d%%" % percent)
            sys.stdout.flush()
        if debug:
            print "DEBUG " + str(lines_total) +"> " + line
        data = {}
        rest = parse_type_and_date (line, data)
        if data["linetype"] == "TerminateInstances" and "TerminateInstances" in parse_types:
            count_terminate_instances += 1
            terminate_instances_param_parser(rest, data)
        elif data["linetype"] == "refresh_resources" and "refresh_resources" in parse_types:
            count_refresh_resource += 1
            refresh_resource_parser(rest, data)
        elif data["linetype"] == "print_ccInstance" and "print_ccInstance" in parse_types:
            count_ccInstance_parser += 1
	    if not ccInstance_parser(rest, data):
		    ignore = True
        else:
            ignore = True
        if ignore:
            lines_ignored +=1
            if debug:
                print "IGNORE> " + line
        else:
            analyze(data)


        # For Debugging to make it faster terminate at 5
        if debug and (len(instance) > 5):
            break

    print_counter("lines total",lines_total)
    print_counter ("lines ignored = ", lines_ignored)
    print_counter("count_terminate_instances",count_terminate_instances)
    print_counter("count_refresh_resource",count_refresh_resource)
    print_counter("count_ccInstance_parser ",count_ccInstance_parser )

           
    return

#
#####################################################################
# MAIN
#####################################################################
def parse_test(f, line):
    print "------------------------------------------------------------"
    print "- parsetest: " + str(f)
    print "------------------------------------------------------------"
    print "INPUT>"
    print line
    data = {}
    # parse_type_and_date(line,data,rest)
    rest = parse_type_and_date (line, data)
    print "REST>"
    print rest
    f(rest, data)
    print "OUTPUT>"
    print pp.pprint(data)


def test1():
    parse_test(ccInstance_parser, 
               "[Wed Nov  9 19:58:12 2011][008128][EUCADEBUG ] print_ccInstance(): refresh_instances():  instanceId=i-42BA06B1 reservationId=r-3D3306BC emiId=emi-0B951139 kernelId=eki-78EF12D2 ramdiskId=eri-5BB61255 emiURL=http://149.165.146.135:8773/services/Walrus/centos53/centos.5-3.x86-64.img.manifest.xml kernelURL=http://149.165.146.135:8773/services/Walrus/xenkernel/vmlinuz-2.6.27.21-0.1-xen.manifest.xml ramdiskURL=http://149.165.146.135:8773/services/Walrus/xeninitrd/initrd-2.6.27.21-0.1-xen.manifest.xml state=Extant ts=1320693195 ownerId=sharif keyName=ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCp13CbKJLtKG5prGiet/VHct36CXzcpBKVgYsh/lxIXWKuositayvvuKux+I5GZ9bFWzMF71xAjmFinmAT3FXFKMd54FebPKZ2kBPCRqtmxz2jT1SG4hy1g1eDPzVX+qt5w8metAs7W//BCaBvWpU5IBuKSNqxO5OUIjIKkw3xkSswRpqSzrUBAmQP7e4dzQvmhqIxq4ZWqcEIWsAik0fSODTipa+Z6DvVKe02f5OtdUsXzz7pIivZ3qRGQveI5SOTdgFPqG+VglMsPURLbFFVWW1l51gCmRUwTf9ClySshSpkpAtaOx/OApQoII/vJxgr/EdYPOu1QLkubS4XH6+Z sharif@eucalyptus ccnet={privateIp=10.0.4.4 publicIp=149.165.159.130 privateMac=D0:0D:42:BA:06:B1 vlan=10 networkIndex=4} ccvm={cores=1 mem=512 disk=5} ncHostIdx=24 serviceTag=http://i1:8775/axis2/services/EucalyptusNC userData= launchIndex=0 volumesSize=0 volumes={} groupNames={sharifnew }")

    return

def test2():
    #
    # RESOURCE PARSER
    #

    parse_test(refresh_resource_parser, 
               "[Wed Nov  9 22:52:10 2011][008128][EUCAERROR ] refresh_resources(): bad return from ncDescribeResource(i23) (1)")
    parse_test(refresh_resource_parser, 
               "[Wed Nov  9 22:52:11 2011][008128][EUCADEBUG ] refresh_resources(): done")
    parse_test(refresh_resource_parser, 
               "[Wed Nov  9 22:52:19 2011][008128][EUCAINFO  ] refresh_resources(): called")
    parse_test(refresh_resource_parser, 
               "[Wed Nov  9 19:50:08 2011][008128][EUCADEBUG ] refresh_resources(): received data from node=i2 mem=24276/22740 disk=306400/305364 cores=8/6")


    return

def test3():
    #
    # TerminateInstance Parser
    #
    parse_test(terminate_instances_param_parser,
               "[Thu Nov 10 10:14:37 2011][021251][EUCADEBUG ] TerminateInstances(): params: userId=(null), instIdsLen=1, firstInstId=i-417B07B2")

    parse_test(terminate_instances_param_parser,
               "[Thu Nov 10 13:04:16 2011][016124][EUCADEBUG ] TerminateInstances(): done.")

    parse_test(terminate_instances_param_parser,
               "[Thu Nov 10 13:04:16 2011][016168][EUCAINFO  ] TerminateInstances(): called")
    return

def make_html (prefix,output_dir, title):
    page_template = """
        <!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML//EN">
        <html> <head>
        <title> %(title)s TEST </title>
        </head>
        
        <body>

        <img src="fg-logo.png" alt="FutureGrid" /> Eucalyptus Monitor
        
        <h1> %(title)s </h1>
        <p>
        <img src="%(prefix)s.pie.png" alt="chart" /><img src="%(prefix)s.bar.png" alt="chart" />

        <hr>
        <address>Author Gregor von Laszewski, laszewski@gmail.com</address>
        <!-- hhmts start -->Last modified: %(now)s <!-- hhmts end -->
        </body> </html>
    """
    print "========"
    now = datetime.now()
    now = "%s-%s-%s %s:%s:%s" %  (now.year, now.month, now.day, now.hour, now.minute, now.second)
    filename = output_dir+"/"+prefix+".html";
    f = open(filename, "w")
    f.write(page_template % vars())
    #print>>f, page_template % vars()

    f.close()

def test4():
    parse_file ("/tmp/cc.log.4",jason_dump,debug=False)
    return

# Convert 2012-01-28-04-13-04-cc.log to datetime
def filename_todate(str):
    return datetime.strptime(str, '%Y-%m-%d-%H-%M-%S-cc.log')


def test_file_read(filename,progress=True, debug=False):
    parse_file (filename,instances.add,debug,progress)
    instances.calculate_delta ()
    instances.dump()

    return

def test_sql_read():
    instances.read_from_db()
    instances.calculate_delta ()
    instances.dump()

    return

def test_sql_write(filename,progress=True, debug=False):
    parse_file (filename,instances.add,debug,progress)
    instances.calculate_delta ()
    instances.write_to_db()

def display(users, prefix, output_dir):
    a = output_dir+"/"+prefix+".pie.png"
    b = output_dir+"/"+prefix+".bar.png"
    display_user_stats (users, filename=a)
    display_user_stats (users, type="bar", filename=b)
    make_html(prefix, output_dir, "VMs used by users")
    #os.system ("open sample.html")

def test_user_stats():
    users = {}
    instances.calculate_user_stats (users)
    instances.write_to_db()
    print pp.pprint(users)
    display(users)
    """
    users = {}
    instances.calculate_user_stats (users, "2011-11-06 00:13:15", "2011-11-08 14:13:15")
    instances.write_to_db()
    display(users)

    print pp.pprint(users)

    users = {}

    a = datetime.strptime("2011-11-06 00:13:15",'%Y-%m-%d %H:%M:%S')
    b = datetime.strptime("2011-11-08 14:13:15",'%Y-%m-%d %H:%M:%S')
        
    instances.calculate_user_stats (users, a, b)
    instances.write_to_db()
    print pp.pprint(users)
    display(users)
    """

    return

def read_all_log_files_and_store_to_db (path, args):
    """
    we assume thet the dir has only files of the form. All files have been gathere there from the fg-unix command
    <name>.log
    # hungruies job
    """
    listing = os.listdir(path)
    count = 0
    for filename in listing:
        count =+ 1
        print "Processing file is: " + filename
        #parse_file (path + "/" + filename,instances.add,debug=False,progress=True)
	parse_file(path + "/" + filename, instances.add, args.linetypes, debug=False, progress=True)
    instances.calculate_delta ()
    instances.write_to_db()

    
def main():

    users = {}
    instances = Instances()
    instance = instances.data
    pp = pprint.PrettyPrinter(indent=4)

    if sys.version_info < (2, 7):
        print "ERROR: you must use python 2.7 or greater"
        exit (1)
    else:
        print "Python version: " + str(sys.version_info)
    
    # test1()
    # test2()
    # test3()

    #    test_file_read("/tmp/cc.log.4",progress=True)
    #    test_file_read("/tmp/cc.log.prints_cc",progress=False, debug=False)

    # ONLY FILE READ TEST

    # test_file_read("/tmp/cc.log.prints_cc",progress=True, debug=True)
    # test_user_stats()

    # SQL TEST
    
    #test_sql_write("/tmp/cc.log.prints_cc",progress=True, debug=True)
    #test_sql_read()
    #test_user_stats()

    # MONSTER TEST

    #dir_path = os.getenv("HOME") + "/Desktop/BACKUP"
    #    read_all_log_files_and_store_to_db (dir_path)
   
    def_s_date = "19700101"
    def_e_date = "29991231"
    def_conf = "futuregrid.cfg"
    def_linetypes = ["TerminateInstances", "refresh_resources", "print_ccInstance"]
    ''' argument parser added '''

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--from", dest="s_date", default=def_s_date,
		    help="start date to begin parsing (type: YYYYMMDD)")
    parser.add_argument("-e", "--to", dest="e_date", default=def_e_date,
		    help="end date to finish parsing (type: YYYYMMDD)")
    parser.add_argument("-i", dest="input_dir", required=True,
		    help="Absolute path where the files (e.g. 2012-02-16-00-21-17-cc.log generated by fg-unix) exist")
    parser.add_argument("-o", dest="output_dir", required=True,
		    help="output directory")
    parser.add_argument("--conf", dest="conf",
		    help="configuraton file of the database to be used")
    parser.add_argument("--cleandb", action="store_true", dest="cleandb", default=False,
		    help="This command without any parameter deletes the entire database. *Be careful with this")
    parser.add_argument("--parse", nargs="+", dest="linetypes", default=def_linetypes,
		    help="if one of more types separated with space ar used, those types are parsed and included into the database (types are print_ccInstance, refresh_resources)")
    args = parser.parse_args()
    print args
    
    '''
    Parameters
    ----------
    dest=variable name
    - 'dest' in parser.add_argument sets a variable name where the input to be allocated
    required=True
    - To set an argument is mandatory (required=False is default)
    help=text
    - Description for the argument

    How we can use argparse in this file?
    -------------------------------------
    1) fg-parser.py -s start date -e end date; will parse logs between the period that specified by -s and -e options
       ex) fg-parser.py -s 20120216 -e 20120216
           => 2012-02-16-00-21-17-cc.log ~ 2012-02-16-23-47-16-cc.log will be parsed
    2) fg-parser.py -f filename; Only parse the file that specified by -f option
       ex) fg-parser.py -f 2012-02-16-00-21-17-cc.log
           => Only that file will be parsed
    '''

    #    read_all_log_files_and_store_to_db (args.input_dir, args)
 
    #test_sql_read()
    #test_user_stats()

    # change conf file by --conf filename
    if args.conf:
	    instances.set_conf(args.conf)

    # Clean database if -cleandb is true
    if args.cleandb:
	    import FGCleanupTable
	    FGCleanupTable.main()

    #    make_report(args, ["png", "csv", "gmc"]) 
    
if __name__ == "__main__":
    main()
