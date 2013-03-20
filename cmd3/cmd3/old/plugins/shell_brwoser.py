import webbrowser
import platform

class browser:

    #####################################
    # Browser
    #####################################
   
    def help_open(self):
        """
              open [OPTIONS] filename
        """

    def do_open(self, arguments):
        """Opens the given URL in a browser window."""
        webbrowser.open("file://%s" % filename)

