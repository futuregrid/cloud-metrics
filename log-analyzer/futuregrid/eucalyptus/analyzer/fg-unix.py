#! /usr/bin/env python

# NOTE THIS WILL NOT WORK AS SYNTAX NOT OK, JUST USED TO CATCH IDEAS, ANYONE CAN IMPROVE

#
def sort_euca_log (input,output):
    '''sorts the input file and writes it to the output file with given arguments'''
    return

def merge_euca_log (input1, input2, output):
    '''merges the two input files and writes it to the output file with given arguments'''
    return

def merge_euca_log_dir_files (dir, output):
    ''' merges all logfiles in the dir'''
    # PSEUDO CODE
    # logfiles = *.log *.log.?
    # if logfiles empty nothing to do
    # current_log = pop (logfiles)
    # while logfiles is not empty
    #   logfile = pop(logfiles)
    #   merge_euca_log (current_log, logfiles, tmp)
    #   rm current_logfile
    #   current_logfile = tmp
    # output = current_logfile



