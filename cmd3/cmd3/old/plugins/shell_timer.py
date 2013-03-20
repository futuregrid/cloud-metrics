class timer:

    """
    needs to be integrated in pre post command
    """
    ##########################################################################
    # TIMER
    ##########################################################################

    def do_timer(self, line):
        line = line.lower()

        if line in ("on", "off"):
            self.with_timers = (line == "on")
            print "Timers are now:", self.with_timers
        else:
            self.help_timer()

    def help_timer(self):
        print "Timer toggle used to control whether to timestamp the log."
        print
        print "Syntax:"
        print "   timer <on|off>"
