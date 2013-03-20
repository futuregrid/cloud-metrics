import textwrap

class shell_util:

    def do_quit(self, line):
        return True

    #    do_EOF = do_quit
    #    do_eof = do_quit
    do_q   = do_quit

    def help_help(self):
        msg = """
        DESCRIPTION

           provides some help information
            
        """
        print textwrap.dedent(msg)
        

    def help_quit(self):
        msg = """
        DESCRIPTION

           quits the shell
            
        """
        print textwrap.dedent(msg)
        
    #help_EOF = help_quit
    #help_eof = help_quit
    help_q = help_quit

    # from cmd2
    def select(self, options, prompt='Your choice? '):
        '''Presents a numbered menu to the user.  Modelled after
           the bash shell's SELECT.  Returns the item chosen.
           
           Argument ``options`` can be:

             | a single string -> will be split into one-word options
             | a list of strings -> will be offered as options
             | a list of tuples -> interpreted as (value, text), so 
                                   that the return value can differ from
                                   the text advertised to the user '''
        # copied as is from cmd2
        if isinstance(options, basestring):
            options = zip(options.split(), options.split())
        fulloptions = []
        for opt in options:
            if isinstance(opt, basestring):
                fulloptions.append((opt, opt))
            else:
                try:
                    fulloptions.append((opt[0], opt[1]))
                except IndexError:
                    fulloptions.append((opt[0], opt[0]))
        for (idx, (value, text)) in enumerate(fulloptions):
            self.poutput('  %2d. %s\n' % (idx+1, text))
        while True:
            response = raw_input(prompt)
            try:
                response = int(response)
                result = fulloptions[response - 1][0]
                break
            except ValueError:
                pass # loop and ask again
        return result

    # from cmd2
    def poutput(self, msg):
        '''Convenient shortcut for self.stdout.write(); adds newline if necessary.'''
        if msg:
            self.stdout.write(msg)
            if msg[-1] != '\n':
                self.stdout.write('\n')

