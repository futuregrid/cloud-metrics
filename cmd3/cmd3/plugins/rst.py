import string
import textwrap
from docopt import docopt
import inspect
import sys
import importlib
from  cyberaide.decorators import help_method
from  cyberaide.decorators import command_method
from  cyberaide.decorators import _get_doc_args

class rst:
    
    def activate_rst(self):
        pass
    
    @help_method
    def help_rst(self):
        """
        Usage:
               rst COMMAND 

        Prints out the comand for inclusion into rst

        Arguments:
          COMMAND    The name of the command

        """

    def do_rst(self, args):
        arguments = _get_doc_args(self.help_rst,args)

        what = arguments['COMMAND']
        print
        print "Commnad - %s::" % what
        exec("h = self.help_%s.__doc__" % what)
        h = textwrap.dedent(h).replace("\n", "\n    ")
        print h

    def do_man(self, args):

        print
        print "Commands"
        print 70 * "="
        
        commands = [k for k in dir(self) if k.startswith("do_")]
        commands.sort()

        for command in commands:
            what = command.replace("do_","")
            try:
                print what
                print 70 * "-"
                self.do_rst(what)
            except:
                print "\n    Command documentation %s missing, help_%s" % (what, what)
            print
