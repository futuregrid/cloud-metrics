THIS DOCUMENT IS TO BE COMPLETED, JUST A START

import argparse

"""
from cmd2 import Cmd
from cmd2 import make_option
from cmd2 import options
from cmd2 import Cmd2TestCase

import unittest, sys

class CmdLineAnalyzeEucaData(Cmd):
    multilineCommands = ['orate']
    Cmd.shortcuts.update({'&': 'speak'})
    maxrepeats = 3
    Cmd.settable.append('maxrepeats')

    @options([make_option('-p', '--piglatin', action="store_true", help="atinLay"),
              make_option('-s', '--shout', action="store_true", help="N00B EMULATION MODE"),
              make_option('-r', '--repeat', type="int", help="output [n] times")
             ])
    def do_speak(self, arg, opts=None):
        """Repeats what you tell me to."""
        arg = ''.join(arg)
        if opts.piglatin:
            arg = '%s%say' % (arg[1:], arg[0])
        if opts.shout:
            arg = arg.upper()
        repetitions = opts.repeat or 1
        for i in range(min(repetitions, self.maxrepeats)):
            self.stdout.write(arg)
            self.stdout.write('\n')
            # self.stdout.write is better than "print", because Cmd can be
            # initialized with a non-standard output destination

    do_say = do_speak     # now "say" is a synonym for "speak"
    do_orate = do_speak   # another synonym, but this one takes multi-line input

class TestMyAppCase(Cmd2TestCase):
    CmdApp = CmdLineApp
    transcriptFileName = 'exampleSession.txt'

parser = optparse.OptionParser()
parser.add_option('-t', '--test', dest='unittests', action='store_true', default=False, help='Run unit test suite')
(callopts, callargs) = parser.parse_args()
if callopts.unittests:
    sys.argv = [sys.argv[0]]  # the --test argument upsets unittest.main()
    unittest.main()
else:
    app = CmdLineApp()
    app.cmdloop()
"""

class AnalyzeEucaData:

    instances = None
    users = None

    def __init(self, configuration_file):
        self.users = {}
        self.instances = Instances()
        self.instances.set_conf(configureation_file)
        self.instances.read_from_db()



    
def main():
    if sys.version_info < (2, 7):
        print "ERROR: you must use python 2.7 or greater"
        exit (1)
    else:
        print "Python version: " + str(sys.version_info)

    parser = argparse.ArgumentParser()


    #
    # configuration file 
    #
    parser.add_argument("--conf",
                        dest="configuration_file",
                        help="configuraton file that includes information on how to contact the database")


    # TODO: be able to also have optionally specify the time not just teh date
    #
    # specification of the interval in which the analysis is performed.
    #
    
    parser.add_argument("-s", "--from",
                        dest="start_date",
                        default=def_s_date,
                        help="start date of information  included in the analyzis (type: YYYYMMDD)")
    parser.add_argument("-e", "--to",
                        dest="eend_date",
                        default=def_e_date,
                        help="end date of information  included in the analyzis (type: YYYYMMDD)")


    #
    # handle the configuration filr 
    #
    if args.conf:
        AnalyzeEucaData (configuration_file)
