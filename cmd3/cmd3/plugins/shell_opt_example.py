import textwrap
from docopt import docopt
import inspect
import sys
import importlib
from  util.decorators import help_method
from  util.decorators import _get_doc_args

class shell_opt_example:

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
