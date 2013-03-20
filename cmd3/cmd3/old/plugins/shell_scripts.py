from  util.decorators import help_method
from  util.decorators import _get_doc_args

class shell_scripts:

    @help_method
    def help_script(self):
        """
        Usage:
               script load
               script load NAME FILENAME
               script load FILENAME
               script load REGEXP
               script list
               script NAME

        Process FILE and optionally apply some options

        Arguments:
          FILE        optional input file

        """


    ######################################################################
    # Scripts
    ######################################################################

    script_files = ["scripts/*.txt"]
    scripts = {}
    self._add_scope("script")

    #@ACTIVATE
    def activate_shell_scripts(self):
        self.script_files = ["scripts/*.txt"]
        self.load_shell_scripts(self.script_files)
        self._add_scope("script")

    #@INFO
    def info_shell_scripts (self):
        print "%20s =" % "Script Locations", str(self.scriptfiles)
        print "%20s =" % "Scripts", str(self.scripts)

    def load_shell_scripts(self,script_files):
        self.scripts = {}
        for location in script_files:
            self._import_scripts(location)

    def _import_scripts(self, regex):
        scripts = glob.glob(regex)
        if scripts:
            for filename in scripts:
                (dir, script) = filename.split("/")
                (script,ext) = script.split(".")
                script = script.replace("script_", "")
                print "Import Script", script, "from", filename
                self.scripts[script] = filename

    def _list_scripts(self):
        print 10 * "-"
        print 'Scripts'
        print 10 * "-"
        for v in self.scripts:
            print v, '=', self.scripts[v]

    # logic of load does not work
    # we want load regex and load without that just loads defaul
    # needs docopt

    #@COMMAND
    def do_script(self, args):
        arguments = _get_doc_args(self.help_script,args)

        print(arguments)

        if args == "load":
            self.load_shell_scripts()
            self._list_scripts()
        elif args == "list":
            self._list_scripts()
        elif args in self.scripts:
            filename = self.scripts[args]
            print filename
            file = open(filename, "r")
            for line in file:
                line = self.precmd(line)
                line = self.onecmd(line)
                line = self.postcmd(line)
            file.close()
        else:
            print "script execution not yet defined"

