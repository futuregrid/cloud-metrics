import os

class clear:

    ########################################
    # CLEAR
    ########################################

    def help_clear(self):
        """Documentation for the clear command."""

        print "Clears the screen."

    def do_clear(self, arg):
        """Clears the screen."""

        sys.stdout.write(os.popen('clear').read())
