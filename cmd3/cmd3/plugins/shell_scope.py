#! /usr/bin/env python
import cmd
import string
import textwrap
import glob
import datetime
import os

class shell_scope():

    echo = True
    scope = ""
    scopes = []
    #scopeless = ['info', 'var', 'use', 'quit', 'q', 'EOF', 'eof', 'help']
    scopeless = ['info', 'var', 'use', 'quit', 'q', 'help']
    prompt = 'cm> '
    scripts = {}
    variables = {}
    
    def __init__(self):
        self.scripts = {}
        self._import_scripts("scripts/script_*.txt")
        self.variables = {}
        self.prompt = 'cm> '
        self.echo = True
        self.scope = ""
        self.scopes = []
        self.scopeless = ['info', 'var', 'use', 'quit', 'q', 'help']
        #self.scopeless = ['use', 'quit', 'q', 'EOF', 'eof', 'help']

    def help_use(self):
        msg = """
        DESCRIPTION
        -----------
           often we have to type in a command multiple times. To save
           us typng the name of the commonad, we have defined a simple
           scope thatcan be activated with the use command

        USAGE
        -----
            use list           - lists the available scopes

            use add <scope>    - adds a scope <scope>

            use delete <scope> - removes the <scope>

            use                - without parameters allows an
                                 interactive selection
            
        """
        print textwrap.dedent(msg)

    help_scope = help_use

    ######################################################################
    # Scope and use commands
    ######################################################################
        
    def _add_scope(self, name):
        print "ADDING SCOPE", name
        self.scopes.append(name)
        self._list_scope()

    def _delete_scope(self, name):
        print "DELETE SCOPE", name
        self.scopes.remove(name)
        self._list_scope()
            
    def _list_scope(self):
        print 10 * "-"
        print 'Scope'
        print 10 * "-"
        for s in self.scopes:
            print s

    def do_use(self, arg):
        if arg == 'list':
            self._list_scope()
            return
        elif arg.startswith('add'):
            scope = arg.split(' ')[1]
            self._add_scope(scope)
            return
        elif arg.startswith('delete'):
            # delete does not work
            scope = arg.split(' ')[1]
            self._delete_scope(scope)
            return
        elif arg == "cm":
           self.scope = ""
        elif arg == "/":
           self.scope = ""
        elif arg in self.scopes:
            self.scope = arg
        else:
            self.scope = self.select([""] + self.scopes, 'Which scope? ')

        if self.scope == "":
            print "Switched scope to:", 'cm'
            self.prompt = self.scope + 'cm> '
        else:
            print "Switched scope to:", self.scope
            self.prompt = self.scope + '> '

    do_scope = do_use

    def emptyline(self):
        return
    
    def precmd(self, line):
        if line != "hist":
            self._hist += [ line.strip() ]

        line = line.strip()
        if line == "":
            print
            return line

        if line.startswith("#"):
            print line
            return ""

        time = datetime.datetime.now().strftime("%H:%M:%S")
        date = datetime.datetime.now().strftime("%Y-%m-%d")

        line = line.replace("$time",time)
        line = line.replace("$date",date)
        for v in self.variables:
            line = line.replace("$"+v,self.variables[v])
        for v in os.environ:
            line = line.replace("$"+v,os.environ[v])

        try:
            (start, rest) = line.split(" ")
        except:
            start = line
        
        if (start in self.scopeless) or (self.scope == ""):
            line = line
        else:
            line = self.scope + " " + line

        if self.echo:
            print line

        return line

    

    ######################################################################
    # Echo
    ######################################################################

    def do_echo(self, boolean):
        self.echo = boolean == 'True'

    def help_echo(self):
        msg = """
        DESCRIPTION

           If set to True prints the command befor execution.
           In interactive mode you may want to set it to False.
           When using scripts we recommend to set it to True.

           The default is set to True
            
        """
        print textwrap.dedent(msg)

    ######################################################################
    # Echo
    ######################################################################



    def help_var(self):
        msg = """
        DESCRIPTION
        -----------
           often we have to type in a command that may need to use some repeated variables
           

        USAGE
        -----
            var name=value is this
            
        """
        print textwrap.dedent(msg)


    ######################################################################
    # Scope and use commands
    ######################################################################
        
    def _add_variable(self, name, value):
        self.variables[name] = value
        #self._list_variables()

    def _delete_variable(self, name):
        self._list_variables()
        del self.variables[name]
        #self._list_variables()
            
    def _list_variables(self):
        print 10 * "-"
        print 'Variables'
        print 10 * "-"
        for v in self.variables:
            print v, '=', self.variables[v]

    def do_var(self, arg):
        if arg == 'list':
            self._list_variables()
            return
        elif '=' in arg:
            (variable, value) = arg.split('=',1)
            if value == "time":
                value = datetime.datetime.now().strftime("%H:%M:%S")
            elif value == "date":
                value = datetime.datetime.now().strftime("%Y-%m-%d")
            self._add_variable(variable, value)
            return
        elif arg.startswith('delete'):
            variable = arg.split(' ')[1]
            self._delete_variable(variable)
            return

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
