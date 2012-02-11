#! /usr/bin/env python

import os, glob

# NOTE THIS WILL NOT WORK AS SYNTAX NOT OK, JUST USED TO CATCH IDEAS, ANYONE CAN IMPROVE

#
def sort_euca_log (input,output):
    '''sorts the input file and writes it to the output file with given arguments'''
    return

def merge_euca_log (input1, input2, output):
    '''merges the two input files and writes it to the output file with given arguments'''
    return


def merge_euca_log_files_in_dir (dirpath, output):
    ''' merges all logfiles in the dir'''

    logfiles = glob.glob( os.path.join(dirpath, '*.log*') 
     
    # PSEUDO CODE
    current_log = pop (logfiles)
    for file in logfiles
       merge_euca_log (current_log, files, tmp)
       os.remove (current_log)
       os.move (tmp, current_log)
    os.move (current_log, output)



