''' Command Line Interface for setting up Open Letters stores
Derived from open shakespeare - needs to include Redis details in model
'''

import os
import cmd

def __init__(self, config=None, verbose=False):
        # cmd.Cmd is not a new style class
        cmd.Cmd.__init__(self)
        self.config = config
        self.verbose = verbose
        
def do_load (cmd, line=''):
    args = line.split()
    action = args[0]
    if not action in self.db_actions:
            self.help_db()
            return 1
    self._register_config()
    import openletters.model as model
    #need to define the actions
    

def do_quit(self, line=None):
    sys.exit()