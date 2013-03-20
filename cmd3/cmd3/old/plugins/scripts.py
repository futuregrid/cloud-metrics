class scripts:

    ######################################################################
    # Scripts
    ######################################################################

    scripts = {}

    def _import_scripts(self, regex):
        scripts = glob.glob(regex)
        if scripts:
            for filename in scripts:
                (dir, script) = filename.split("/")
                (script,ext) = script.split(".")
                script = script.replace("script_", "")
                print "Import Script", script, "from", filename
                self.scripts[script] = filename
                
    
    def do_script(self, name):
        if name == "load":
            self.scripts = {}
            self._import_scripts("scripts/script_*.txt")
            self._list_scripts()
        elif name == "list":
            self._list_scripts()
        elif name in self.scripts:
            filename = self.scripts[name]
            print filename
            file = open(filename, "r")
            for line in file:
                line = self.precmd(line)
                line = self.onecmd(line)
            file.close()
        else:
            print "script execution not yet defined"

    def _list_scripts(self):
        print 10 * "-"
        print 'Scripts'
        print 10 * "-"
        for v in self.scripts:
            print v, '=', self.scripts[v]
