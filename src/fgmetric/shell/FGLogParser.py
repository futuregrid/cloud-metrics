#! /usr/bin/env python
'''FGLogParser'''

''' This is a log parser.
    [Platforms] Plan to support Nimbus, openstack, eucalyptus, etc
    [log type] Plan to support various log files
    [log functions] Plan to support various log formats

    Current version has supported
    1. eucalytptus, cc.log*, prince_ccInstance()
'''

import sys
import os
import re
from datetime import *
import argparse
import fileinput

from fgmetric.shell.FGInstances import FGInstances
import fgmetric.util.FGTimeZone

manual = """
MANUAL PAGE DRAFT

NAME - fg-log-parser

DESCRIPTION

usage

<TBD>   cat filename.log | fg-log-parser <parameters>

All log entries are included through a pipe into the program

fg-log-parser

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


class FGLogParser:

    debug = False
    progress = True

    args = None
    instances = None

    def __init__(self):
        self.instances = FGInstances()

    def convert_data_to_list(self, data, attribute):
        rest = data[attribute]
        rest = re.sub(" ", "' , '", rest)
        rest = "['" + rest[1:-1] + "']"
        restdata = eval(rest)
        data[attribute] = restdata

    def convert_data_to_dict(self, data, attribute):
        rest = data[attribute]
        rest = self.convert_str_to_dict_str(rest[1:-1])
        restdata = eval(rest)
        data[attribute] = restdata

    def convert_str_to_dict_str(self, line):
        line = re.sub(' +', ' ', line)
        line = line.strip(" ")
        line = re.sub(',', '%2C', line)  # , value converts '%2C'
        line = re.sub(' ', ',', line)

        # more regular dict
        line = re.sub('=', '\'=\'', line)
        line = re.sub(',', '\',\'', line)
        line = re.sub('=', ' : ', line)
        line = re.sub('%2C', ',', line)  # Back to , value
        return '{\'' + line + '\'}'

    def parse_type_and_date(self, line, data):
        # split line after the third ] to (find date, id, msgtype)
        # put the rest in the string "rest"
        try:
                m = re.search(
                    r'\[(.*)\]\[(.*)\]\[(.*)\](.*)', line, re.M | re.I)
                data['date'] = datetime.strptime(
                    m.group(1), '%a %b %d %H:%M:%S %Y')
                data['date'] = fgmetric.util.FGTimeZone.convert_timezone(
                    data['date'], self.args.timezone, "EST")
                data['id'] = m.group(2)
                data['msgtype'] = m.group(3)
                rest = m.group(4)
                rest = re.sub(' +}', '}', rest).strip()
                if rest.startswith("running"):
                        data['linetype'] = "running"
                        return rest
                elif rest.startswith("calling"):
                        data['linetype'] = "calling"
                        return rest
                else:
                        location = rest.index(":")
                        linetype = rest[0:location]
                        data['linetype'] = re.sub('\(\)', '', linetype).strip()
                        rest = rest[location+1:].strip()
                        return rest
        except (ValueError, AttributeError):
                data['linetype'] = "IGNORE"
                return
        except:
                data['linetype'] = "IGNORE"
                # print sys.exc_info()
                return

    def ccInstance_parser(self, rest, data):
        """parses the line and returns a dict"""

        # replace print_ccInstance(): with linetype=print_ccInstance
        # rest = rest.replace("print_ccInstance():","linetype=print_ccInstance")
        # replace refreshinstances(): with calltype=refresh_instances

        # RunInstances():
        rest = rest.replace(
            "RunInstances():", "calltype=run_instances")   # removing multiple spaces
        rest = rest.replace(
            "refresh_instances():", "calltype=refresh_instances")   # removing multiple spaces

        # separate easy assignments from those that would contain groups, for now simply put groups as a string
        # all others are merged into a string with *=* into rest
        m = re.search(
            r'(.*)keyName=(.*)ccnet=(.*)ccvm=(.*)ncHostIdx=(.*)volumes=(.*)groupNames=(.*)', rest, re.M | re.I)

        # Version 3.0.2
        # Deleted: emiId, kernelId, ramdiskId, emiURL, kernelURL and ramdiskURL
        # Added: accountId, platform, and bundleTaskStateName
        # Changed: value of ownerId is changed

        try:
                data['keyName'] = m.group(2).strip()
                data["ccnet"] = m.group(3).strip()
                data["ccvm"] = m.group(4).strip()
                data["volumes"] = m.group(6).strip()
                data["groupNames"] = m.group(7).strip()
                # assemble the rest string
                rest = m.group(1) + "ncHostIdx=" + m.group(5)
        except:
                return

        # GATHER ALL SIMPLE *=* assignments into a single rest line and add
        # each entry to dict via eval
        rest = self.convert_str_to_dict_str(rest)
        try:
            restdata = eval(rest)
        except:
            print "eval failed:(" + str(sys.exc_info()[0]) + "), (" + str(rest) + ")"
            return

        data.update(restdata)

        # convert ccvm and ccnet to dict
        self.convert_data_to_dict(data, "ccvm")
        self.convert_data_to_dict(data, "ccnet")

        # converts volumes and groupNAmes to list
        self.convert_data_to_list(data, "groupNames")
        self.convert_data_to_list(data, "volumes")

        # convert the timestamp
        data["ts"] = datetime.fromtimestamp(int(data["ts"]))

        return data

    def refresh_resource_parser(self, rest, data):
        #[Wed Nov  9 19:50:08 2011][008128][EUCADEBUG ] refresh_resources(): received data from node=i2 mem=24276/22740 disk=306400/305364 cores=8/6
        if (rest.find("received") > -1):
            rest = re.sub("received data from", "", rest).strip()
        # node=i2 mem=24276/22740 disk=306400/305364 cores=8/6
            m = re.search(
                r'node=(.*) mem=(.*)[/](.*) disk=(.*)/(.*) cores=(.*)/(.*)', rest, re.M | re.I)
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

    def terminate_instances_param_parser(self, rest, data):

        rest = rest.strip()
        if rest.startswith("params"):
            # params: userId=(null), instIdsLen=1, firstInstId=i-417B07B2
            rest = re.sub("params:", "", rest).strip()
            # node=i2 mem=24276/22740 disk=306400/305364 cores=8/6
            m = re.search(
                r'userId=(.*) instIdsLen=(.*) firstInstId=(.*)', rest, re.M | re.I)
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

    def print_counter(self, label, counter):
        print label + " = " + str(counter)

    def set_argparser(self):
        def_s_date = "19700101"
        def_e_date = "29991231"
        def_conf = "futuregrid.cfg"
        def_linetypes = [
            "TerminateInstances", "refresh_resources", "print_ccInstance"]
        def_platform = "eucalyptus"
        def_platform_version = "3.0.2"

        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-s", "--from", dest="from_date", default=def_s_date,
            help="start date to begin parsing (type: YYYYMMDD)")
        parser.add_argument("-e", "--to", dest="to_date", default=def_e_date,
                            help="end date to finish parsing (type: YYYYMMDD)")
        parser.add_argument("-i", "--input_dir", dest="dirname", required=True,
                            help="Absolute path where the files (e.g. 2012-02-16-00-21-17-cc.log generated by fg-unix) exist")
        parser.add_argument("--conf", dest="conf",
                            help="configuraton file of the database to be used")
        parser.add_argument(
            "-l", "--parse", nargs="+", dest="linetypes", default=def_linetypes,
            help="specify function names which you want to parse (types: print_ccInstance, refresh_resources)")
        parser.add_argument("-z", "--gzip", action="store_true", default=False,
                            help="gzip compressed files will be loaded")
        parser.add_argument(
            "-d", "--debug", action="store_true", default=False,
            help="debug on|off")
        parser.add_argument("-p", "--platform", default=def_platform,
                            help="Cloud platform name, required. (e.g. nimbus, openstack, eucalyptus, etc)")
        parser.add_argument(
            "-pv", "--platform_version", default=def_platform_version,
            help="Cloud platform version. (e.g. 2.9 for nimbus, essex for openstack, and  2.0 or 3.1 for eucalyptus)")
        parser.add_argument("-n", "--nodename", required=True,
                            help="Hostname of the cloud platform, required. (e.g., hotel, sierra, india, alamo, foxtrot)")
        parser.add_argument(
            "-tz", "--timezone", dest="timezone", default="local()",
            help="gzip compressed files will be loaded")

        args = parser.parse_args()
        print args

        '''
        How we can use argparse in this file?
        -------------------------------------
        1) fg-parser.py -s start date -e end date; will parse logs between the period that specified by -s and -e options
           ex) fg-parser.py -s 20120216 -e 20120216
               => 2012-02-16-00-21-17-cc.log ~ 2012-02-16-23-47-16-cc.log will be parsed
        2) fg-parser.py -f filename; Only parse the file that specified by -f option
           ex) fg-parser.py -f 2012-02-16-00-21-17-cc.log
               => Only that file will be parsed
        '''

        self.args = args

    def check_argparser(self):
        if self.args.conf:
            self.instances.db.set_conf(self.args.conf)
            self.instances.db.update_conf()

        if self.args.gzip:
            import zlib
            CHUNKSIZE = 1024
            self.gz = zlib.decompressobj(16+zlib.MAX_WBITS)

        if self.args.debug:
            self.debug = True

    def read_compressed_line(self, line):
        if self.args.gzip:
            return self.gz.decompress(line)
        else:
            return line

    def read_logs(self):
        if self.args.dirname == "-":
            self.read_stdin()
        else:
            self.read_files()

    def read_files(self):

        from_date = datetime.strptime(
            self.args.from_date + " 00:00:00", '%Y%m%d %H:%M:%S')
        to_date = datetime.strptime(
            self.args.to_date + " 23:59:59", '%Y%m%d %H:%M:%S')
        dirname = self.args.dirname

        try:
            listdir = os.listdir(dirname)
        except:
            listdir = ""

        for filename in listdir:
            try:
                single_date = datetime.strptime(str(
                    filename).split(".")[0], '%Y-%m-%d-%H-%M-%S-cc')
                if from_date <= single_date <= to_date:
                    print "Processing file is: " + filename
                    self.parse_log(
                        dirname + "/" + filename, self.instances.update_traceinfo)
            except (ValueError):
                print "error occured parsing for: " + filename
                self.debug_output(sys.exc_info())
                continue
            except:
                print "error occured parsing for: " + filename
                print sys.exc_info()
                self.debug_output(sys.exc_info())
                continue

    def read_stdin(self):
        try:
            print "Processing stdin... "
            self.parse_log(None, self.instances.update_traceinfo)
        except:
            print sys.exc_info()
            pass

    def parse_log(self, filename, analyze):

        lines_total = lines_ignored = count_terminate_instances = count_refresh_resource = count_ccInstance_parser = read_bytes = 0
        parse_types = self.args.linetypes

        print filename

        if filename:
            file_size = os.path.getsize(filename)
            self.debug_output("SIZE>:" + str(file_size))

        for line in fileinput.input(filename, openhook=fileinput.hook_compressed):
            # line = self.read_compressed_line(line)
            line = line.rstrip()
            ignore = False
            lines_total += 1
            read_bytes += len(line)
            data = {}
            if (self.debug or self.progress) and filename and ((lines_total % 1000) == 0):
                percent = int(100 * read_bytes / file_size)
                sys.stdout.write("\r%2d%%" % percent)
                sys.stdout.flush()
            # self.debug_output("DEBUG " + str(lines_total) +"> " + line)
            rest = self.parse_type_and_date(line, data)

            '''
            Temporarily prince_ccInstance is only available to parse

            if data["linetype"] == "TerminateInstances" and "TerminateInstances" in parse_types:
                count_terminate_instances += 1
                terminate_instances_param_parser(rest, data)
            elif data["linetype"] == "refresh_resources" and "refresh_resources" in parse_types:
                count_refresh_resource += 1
                refresh_resource_parser(rest, data)
            el'''
            if data["linetype"] == "print_ccInstance" and "print_ccInstance" in parse_types:
                count_ccInstance_parser += 1
                if not self.ccInstance_parser(rest, data):
                    ignore = True
                else:
                    # cloudplatformid
                    data["cloudPlatformIdRef"] = self.cloudplatform_id

                    analyze(data)
            else:
                ignore = True

            if ignore:
                lines_ignored += 1
                # self.debug_output("IGNORED LAST LINE> ")

            # For Debugging to make it faster terminate at 5
            # if self.debug and (len(self.instances.data) > 5):
            #    break

        fileinput.close()

        self.print_counter("lines total", lines_total)
        self.print_counter("lines ignored = ", lines_ignored)
        self.print_counter(
            "count_terminate_instances", count_terminate_instances)
        self.print_counter("count_refresh_resource", count_refresh_resource)
        self.print_counter("count_ccInstance_parser ", count_ccInstance_parser)

    def store_parsed(self):
        self.instances.db.connect()
        self.instances.write_to_db()
        self.instances.set_userinfo()
        self.instances.write_userinfo_to_db()

        self.print_counter("======================", "")
        self.print_counter("instance stored total", len(
            self.instances.instance))
        self.print_counter("userinfo stored total", len(
            self.instances.userinfo))

    def get_cloudplatform_info(self):
        self.instances.db.conf()
        self.instances.db.connect()
        whereclause = {"platform": self.args.platform, "hostname":
                       self.args.nodename, "version": self.args.platform_version}
        self.cloudplatform_id = self.instances.get_cloudplatform_id(
            whereclause)

    def debug_output(self, msg):
        if not self.debug:
            return
        print msg

    def test_file_read(self, filename):
        parse_log(filename, self.instances.update_traceinfo)
        self.instances.dump()

    def test_sql_read(self):
        self.instances.read_from_db()
        self.instances.dump()

    def test_sql_write(self, filename):
        parse_log(filename, self.instances.update_traceinfo)
        instances.write_to_db()


def main():
    parser = FGLogParser()
    parser.set_argparser()
    parser.check_argparser()
    parser.get_cloudplatform_info()
    parser.read_logs()
    parser.store_parsed()

if __name__ == "__main__":
    main()
