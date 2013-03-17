from method_decorator import method_decorator
import textwrap
from docopt import docopt

# using decorator http://stackoverflow.com/questions/306130/python-decorator-makes-function-forget-that-it-belongs-to-a-class

class help_method(method_decorator):
    def __call__(self, *args, **kwargs):
        print 70 * "-"
        print textwrap.dedent(self.__doc__)
        print 70 * "-"

def _get_doc_args(help,args):
    arguments = docopt(textwrap.dedent(help.__doc__), argv=args)
    return arguments


"""
class docopts(method_decorator):

    def __call__(self, *args, **kwargs):


        method_name=self.__name__
        class_name=(self.cls.__name__ if self.cls else None),
        help_name = method_name.replace("do_", "help_")

        method = getattr(self.cls, help_name)

        arguments = _get_doc_args(method,args)
        print 70 * "-"
        print arguments
        print 70 * "-"
"""
