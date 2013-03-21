from  cyberaide.decorators import command
import os
import sys
from sh import open
import platform

class edit:

    ########################################
    # EDIT
    ########################################

    def activate_edit(self):
        pass

    @command
    def do_edit(self, arg, arguments):
        """Ussage:
             edir FILENAME
        Arguments:
            FILENAME  the file to edit

        Edits a file."""

        filename = arg

        if platform.system() == 'Darwin':

            # touch filename
            if not os.path.exists(filename):
                file(filename, 'w+').close()

            editors = ["/Applications/Aquamacs.app", "/Applications/Emacs.app","/usr/bin/emacs"]

            for editor in editors:
                if os.path.exists(editor):
                    open("-a", editor, filename)
                    return

            print "ERROR: Could not find working editor in", editors
            
