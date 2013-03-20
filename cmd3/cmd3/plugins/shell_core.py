import sys

class shell_core:

    def do_EOF(self, args):
        return True

    def do_quit(self, args):
        sys.exit()
