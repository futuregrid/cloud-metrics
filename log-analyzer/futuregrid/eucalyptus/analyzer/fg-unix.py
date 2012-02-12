#! /usr/bin/env python

import os, glob
import re
from datetime import datetime

# NOTE THIS WILL NOT WORK AS SYNTAX NOT OK, JUST USED TO CATCH IDEAS, ANYONE CAN IMPROVE


#
# from 
# http://stackoverflow.com/questions/136168/get-last-n-lines-of-a-file-with-python-similar-to-tail
#
#

def tail(f, window=20):
    """
    Returns the last `window` lines of file `f` as a list.
    """
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

def head(file, lines_2find=1):
   file.seek(0)                            #Rewind file
   return [file.next() for x in xrange(lines_2find)]


def getdate_from_euca_log_line(line):
   tmp = re.split ('\]', line.pop())
   return datetime.strptime(tmp[0][1:], '%a %b %d %H:%M:%S %Y')

def generate_filename (date_object, postfix):
  name = str(date_object).replace(" ","-").replace(":","-")
  return name + postfix 

#####################################################################
# MAIN
#####################################################################
def main():
  FILE = open("/tmp/cc.log.4", "r", 0) 
  print "---- head ----\n"
  print head(FILE,1)
  print "---- tail ----\n"
  line = tail(FILE,1)
  print line
  date_object = getdate_from_euca_log_line(line)
  print date_object
  print generate_filename (date_object,'-cc.log')


  return
  
if __name__ == "__main__":
    main()
