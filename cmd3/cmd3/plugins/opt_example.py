import textwrap
from docopt import docopt
import inspect
import sys
import importlib
from  cyberaide.decorators import help_method
from  cyberaide.decorators import command_method
from  cyberaide.decorators import _get_doc_args

class opt_example:
    
    def activate_opt_example(self):
        pass
    
    @help_method
    def help_opt_example(self):
        """
        Usage:
               opt_example [-vr] [FILE] ...

        Process FILE and optionally apply some options

        Arguments:
          FILE        optional input file

        Options:
          -v       verbose mode
          -r       make report

        """

    def do_opt_example(self, args):
        arguments = _get_doc_args(self.help_opt_example,args)

        print(arguments)
    
    def do_neu(self, args):
        arguments = _get_doc_args(self.help_opt_example,args)
        print(arguments)
