from cyberaide.decorators import command

class info:

    @command
    def do_info(self, arg, arguments):
        """
        Usage:
               info

        Prints some internal information about the shell

        """
        for element in dir(self):
            print element

    def do_help(self, arg):
       'List available commands with "help" or detailed help with "help cmd".'
       print "myhelp"
       if arg:
           # XXX check arg syntax
           try:
               func = getattr(self, 'help_' + arg)
           except AttributeError:
               print "AAA"
               try:
                   doc=getattr(self, 'do_' + arg).__doc__
                   if doc:
                       self.stdout.write("%s\n"%str(doc))
                       return
               except AttributeError:
                   pass
               try:
                   exec('self.do_%s("-h")' % arg)
               except:
                   pass
               #self.stdout.write("%s\n"%str(self.nohelp % (arg,)))
               return
           func()
       else:
           names = dir(self)
           cmds_doc = []
           cmds_undoc = []
           help = {}
           for name in names:
               if name[:5] == 'help_':
                   help[name[5:]]=1
           names.sort()
           # There can be duplicates if routines overridden
           prevname = ''
           for name in names:
               if name[:3] == 'do_':
                   if name == prevname:
                       continue
                   prevname = name
                   cmd=name[3:]
                   if cmd in help:
                       cmds_doc.append(cmd)
                       del help[cmd]
                   elif getattr(self, name).__doc__:
                       cmds_doc.append(cmd)
                   else:
                       cmds_undoc.append(cmd)
           self.stdout.write("%s\n"%str(self.doc_leader))
           self.print_topics(self.doc_header,   cmds_doc,   15,80)
           self.print_topics(self.misc_header,  help.keys(),15,80)
           self.print_topics(self.undoc_header, cmds_undoc, 15,80)

