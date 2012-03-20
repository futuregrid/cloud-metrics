#! /usr/bin/env python

#
# LOG = ...
# BIN = ...
#
source log-analyzer.cfg
#

# cp $BIN/crontab.template euca-log-analyzer.crontab
# perl -p -i -e 's/LOG/${LOG}/g'  euca-log-analyzer.crontab
# perl -p -i -e 's/BIN/${BIN}/g'  euca-log-analyzer.crontab
# cat euca-log-analyzer.crontab

import arparse
import ConfigParser
import string





if __name__ == "__main__":
    main()

#####################################################################
# MAIN
#####################################################################
def main():
    
    #---------------------------------------------------------------------
    # READING THE CONFIGURATION PARAMETERS from
    # etc/fg-log-analyzer.cfg
    #---------------------------------------------------------------------
    config = ConfigParser.ConfigParser()
    config.read("etc/fg-log-analyzer.cfg")
    crontab_file = config.get("crontab", "filename")
    crontab_template = config.get("crontab", "template")
    log_dir = config.get("environment", "log_dir")
    bin_dir = config.get("environment", "bin_dir")

    #---------------------------------------------------------------------
    # generating the crontab file
    #---------------------------------------------------------------------
    os.remove (crontab_file)
    generate_crontab(crontab_tempalte, crontab_file, log_dir, bin_dir)
    

def generate_crontab (input_file, output_file, log_replace_text, bin_replace_text):
# replaces the BIN and LOG text in a file
f = open("file")
    o = open("output","a")
    while 1:
        line = f.readline()
        if not line: break
        line = line.replace("LOG",log_replace_text)
        line = line.replace("BIN",bin_replace_text)
        o.write(line + "\n")
    o.close()



#
