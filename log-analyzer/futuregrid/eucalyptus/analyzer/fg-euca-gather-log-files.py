#! /usr/bin/env python

"""
Manual Page Draft

NAME - fg-euca-gather-log-files

DESCRIPTION
===========

Eucalyptus 2.0 provides a number of log files that are written into a
directory. The log files are maintained with the rrd tool, thus they
will be overwritten after a particular time period. This tool copies
the log files that end with .log.?  and copies them into a backup
directory. A log file will only be copied into backup if it is not
already there. This avoids unnecessary operations and allows the
integration of this script into cron.

USAGE
=====

fg-euca-gather-log-files <from_dir> <backup_dir>

The program has a number of parameters by default it takes two
directories. The first directory is the directory from which all
log files are copied. The second is the directory to which the
files are to be copied (e.g our BAckup directory). If the backup
directory does not exists it is being utomatically created.

One thing is important to not that the current script looks
recuresively through all subdirectories starting from the from dir.
This is due to the fact that our initial script backed up all files
into various subdirectories. All files will be renamed to

   YYYY-MM-DD-HH-mm-ss-cc.log

Specific arguments can be controlled as follows

  --recursive

      switches on recursive search of the log files starting from
      <from_dir>

  --norecursive

      switches on recursive search of the log files starting from
      <from_dir>

  --backup <dir>

    specifies the backup directory

  --source <dir>

    specifies the source directory.

If any of the parameters are used the specification of any
parameters without named parameters is not allowed. Calling

fg-euca-gather-log-files --recurseive --source <from_dir> --backup <backup_dir>

is equicvalent to

fg-euca-gather-log-files <from_dir> <backup_dir>


In a production environment we recommend using explicit parameter naming
in order to be more transparent.

TODO: decide if we should eliminate arguments without parameters alltogether.
Hyungro can decide, may be easier to implement and thus saves time.


INSTALATION
===========

Download
--------
Download the code from Git

git@github.com:futuregrid/eucalyptus-cloud-metrics.git

describe here.

Deploy
------

After download, please go into the directory xyzand say

pip install setup

This will install the program(s) into

/usr/loal/bin

There you will find the program

fg-euca-gather-log-files


Cron Setup
----------
Describe here what to do (Lee or Sharif)


Update
------

At times there may be updates made to this program. In order to update
the already deployed script, the following steps are recommended:

(probably just like the first time, but we must make sure taht we just document
 it here or refer to the instalation instructions.

e.g. you could decide if a git pull should be called followed by a new pip install setup

Easy install/Pip
----------------

In future we intent to host this program in pypi and the administrator will be able to call

  pip install fg-metrics

or

   easyinstall install fg-metrics

without needing to get the code from github

Contribution
------------

If you like to contribute to the code, please contact Gregor von Laszewski
at laszewski@gmail.com. The code is located on github at

 https://github.com/futuregrid/eucalyptus-cloud-metrics

in the directory cloud-metrics

License
The code is distributed under Apache 2.0 License
Authors: Gregor von Laszewski, H. Lee
E-mail: laszewski@gmail.com

"""


import os, glob
import re
import shutil
from datetime import datetime
import fnmatch

######################################################################
# TAIL
######################################################################
def tail(f, window=20):
    """
    Returns the last `window` lines of file `f` as a list.
    f - is the file descriptor 
    window - is the number of lines that will be returned from the end
    """
    # from 
    # http://stackoverflow.com/questions/136168/get-last-n-lines-of-a-file-with-python-similar-to-tail

    BUFSIZ = 1024
    f.seek(0, 2)
    bytes = f.tell()
    size = window + 1
    block = -1
    data = []
    while size > 0 and bytes > 0:
        if bytes - BUFSIZ > 0:
            # Seek back one whole BUFSIZ
            f.seek(block * BUFSIZ, 2)
            # read BUFFER
            data.insert(0, f.read(BUFSIZ))
        else:
            # file too small, start from begining
            f.seek(0,0)
            # only read what was not read
            data.insert(0, f.read(bytes))
        linesFound = data[0].count('\n')
        size -= linesFound
        bytes -= BUFSIZ
        block -= 1
    return ''.join(data).splitlines()[-window:]


"""
#
def sort_euca_log (input,output):
    '''sorts the input file and writes it to the output file with given arguments'''
    # TODO:
    os.system ("sort -u -k5n -k2M -k3n -k4 " + input + " > " + output)
    return

def merge_euca_log (input1, input2, output):
    '''merges the two input files and writes it to the output file with given arguments'''
    os.system ("sort -m -k5n -k2M -k3n -k4 " + input + " > " + output)
    return

#def merge_euca_log_files_in_dir (dirpath, output):
#    ''' merges all logfiles in the dir'''

#    logfiles = glob.glob( os.path.join(dirpath, '*.log*') 
     
    # PSEUDO CODE
    #current_log = logfiles.pop ()
    #for file in logfiles
    #   merge_euca_log (current_log, files, tmp)
    #   os.remove (current_log)
    #   os.move (tmp, current_log)
    #os.move (current_log, output)
    #return                     

#def concat_euca_log_files (input1,input2,output):
#    '''checks and concatenates to output files'''
    # check if the last line of input1 <= input2, assumes asscending order 
#    os.system ('cat ' + input1 + " " + input2 + " > " + output)
#    return

#def sort_accending_euca_log (input, output):
#    '''this function will revert the eucalyptus log file'''
    # maes sure that the input file is in acending order
    # date_start = date from first line
    # date_end = date from last line
#    invert_needed = date_start > date_end
#    if inverted_needed
#       os.system("rev " + input + " > " + output)

#
# based on how euca creates logfiles, I guess we can just combine all logfiles with a .?+ at the end
# we must make sure the order is ok to not effect the date ordering
#
"""

######################################################################
# HEAD
######################################################################
def head(file, n=1):
    """
    Returns the first n lines in a file.
    file - is the file descriptor
    n - number of lines to be returned from the begining of the file
    """
    file.seek(0)                            #Rewind file
    return [file.next() for x in xrange(n)]



######################################################################
# getdate_from_euca_log_line
######################################################################
def getdate_from_euca_log_line(line):
    """
    Eucalyptus log files have a time stamp at the beginning of the
    file. This function returns the date from that line as a datetime
    object.
    return - datetime object of the timestamp in the line
    """
    tmp = re.split ('\]', line.pop())
    return datetime.strptime(tmp[0][1:], '%a %b %d %H:%M:%S %Y')

######################################################################
# generate_filename 
######################################################################
def generate_filename (date_object, postfix):
    """
    This function is an internal helper function that converts a date
    object to a string in which all : and " " are replaced with "-"
    """
    name = str(date_object).replace(" ","-").replace(":","-")
    return name + postfix 

######################################################################
# rename_euca_log_file 
######################################################################
def rename_euca_log_file (path,name):
    """
    This function renames a given eucalyptus file located in
    "path/name" based on the timestamp that can be found in the last
    line of the file.
    """
    old_name = os.path.join(path,name)
    print " renaming "  + old_name
    new_name = generate_euca_log_filename(path,name)
    print new_name
    if not os.path.exists(new_name):
        os.rename (old_name, new_name)
    else:
        print "file existed already: " + new_name, ", deleting: " + old_name   
        os.remove(old_name)
    return

######################################################################
# generate_euca_log_filename 
######################################################################
def generate_euca_log_filename (path,name):
    """
    Given the location of a eucalyptus log file as "path/name", a new
    name is generated and returned based on the time stamp in the last
    line of the logfile. The name will be date-time.cc.log where all
    items are separated with "-". The file will not be renamed with
    that function.
    """
    old_name = os.path.join(path,name)
    FILE = open(old_name, "r", 0) 
    line = tail(FILE,1)
    date_object = getdate_from_euca_log_line(line)
    new_name = generate_filename (date_object,'-cc.log')
    new_name = os.path.join(path,new_name)
    return new_name



######################################################################
# ls
######################################################################
def ls(path):
    """
    simply does a unix ls on the path. It is used for debugging.
    """
    print "----"
    os.system ("ls " + path)
    print "----"

######################################################################
# all_euca_log_files 
######################################################################
def all_euca_log_files (path):
    """
    returns a list of all eucalyptus logfiles that are located in all
    subdirectories starting from "path".
    """
    all_files = []
    for dirname, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if fnmatch.fnmatch(filename, '*cc.log.*'):
                all_files.append(os.path.join(dirname, filename))
    return all_files

######################################################################
# gather_all_euca_log_files 
######################################################################
def gather_all_euca_log_files (from_path,backup):
    """
    this function gathers all eucalyptus log files that are located in
    all subdirectories starting from "from_path" and copies them into
    the specified backup directory. In addition all log file will be
    renamed based on the timestap in the last line of the log
    file. The fileame is date-time.cc.log where all items are
    separated with a "-". E.g. YYYY-MM-DD-HH-mm-ss-cc.log. If a
    logfile already exists with that name it will not be overwritten
    and the next file in the subdirectory will be attempted to be
    copied to backup.
    """
    if not os.path.exists (backup):
        os.makedirs (backup)

    print from_path
    for file in all_euca_log_files(from_path):
        path = os.path.dirname(file)
        name = os.path.basename(file)
        new_name = os.path.basename(generate_euca_log_filename (path,name))
        new_location = os.path.join(backup,new_name)
        if not os.path.exists(new_location):
            print new_name
            shutil.copy2 (file, new_location)
        else:
            print new_name + ", WARNING: file exists, copy ignored"
    return

######################################################################
# code for testing that works
######################################################################
def works():
  FILE = open("/tmp/cc.log.4", "r", 0) 
  print "---- head ----\n"
  print head(FILE,1)
  print "---- tail ----\n"
  line = tail(FILE,1)
  print line
  date_object = getdate_from_euca_log_line(line)
  print date_object
  print generate_filename (date_object,'-cc.log')

  shutil.copy2('/tmp/cc.log.4', '/tmp/cc.log.5')
  ls("/tmp")
  rename_euca_log_file("/tmp", "cc.log.5")
  ls("/tmp")
  return

#####################################################################
# main
#####################################################################
def main():

   def_input_dir = "/tmp/uncompressed-euca-logbackup/"
   def_output_dir = "/var/log/eucalyptus/BACKUP"
   import argparse

   # Parse arguments
   # ---------------
   parser = argparse.ArgumentParser()
   parser.add_argument("-i", dest="input_dir", default=def_input_dir,
		   help="Absolute path where (unparsed) cc.logs files exist")
   parser.add_argument("-o", dest="output_dir", default=def_output_dir,
		   help="Absolute path where (parsed & renamed) output cc.logs files to be saved")
   args = parser.parse_args()
   #print args.input_dir, args.output_dir

   gather_all_euca_log_files (args.input_dir, args.output_dir)

   return

if __name__ == "__main__":
	main()