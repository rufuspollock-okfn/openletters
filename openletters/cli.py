''' Command Line Interface for setting up Open Letters stores
Derived from open shakespeare - needs to include Redis details in model
'''
import os
import sys

import paste.script.command

class BaseCommand(paste.script.command.Command):
    parser = paste.script.command.Command.standard_parser(verbose=True)
    parser.add_option('-c', '--config', dest='config',
            default='development.ini', help='Config file to use (default: development.ini)')
    default_verbosity = 1
    group_name = 'openletters'

    def _load_config(self):
        from paste.deploy import appconfig
        from openletters.config.environment import load_environment
        if not self.options.config:
            msg = 'No config file supplied'
            raise self.BadCommand(msg)
        self.filename = os.path.abspath(self.options.config)
        conf = appconfig('config:' + self.filename)
        load_environment(conf.global_conf, conf.local_conf)

    def _setup_app(self):
        cmd = paste.script.appinstall.SetupCommand('setup-app') 
        cmd.run([self.filename]) 


class ManageDb(BaseCommand):
    '''Perform various tasks on the database.
    
    db create
    db clean
    db rebuild # clean and create
    db init # create and put in default data
    # db upgrade [{version no.}] # Data migrate
    '''
    summary = __doc__.split('\n')[0]
    usage = __doc__
    max_args = None
    min_args = 1

    def command(self):
        self._load_config()
        from openletters import model

        cmd = self.args[0]
        if cmd == 'create':
            model.repo.create_db()
        elif cmd == 'init':
            model.repo.init_db()
        elif cmd == 'clean' or cmd == 'drop':
            model.repo.clean_db()
        elif cmd == 'rebuild':
            model.repo.rebuild_db()
        elif cmd == 'upgrade':
            if len(self.args) > 1:
                model.repo.upgrade_db(self.args[1])
            else:
                model.repo.upgrade_db()
        else:
            print 'Command %s not recognized' % cmd
            sys.exit(1)


class Load(BaseCommand):
    '''Load external data into domain model.

        dickens: Load Dickens data.
    '''
    summary = __doc__.split('\n')[0]
    usage = __doc__
    max_args = None
    min_args = 1

    def command(self):
        self._load_config()
        cmd = self.args[0]
        if cmd == 'dickens':
            print 'TODO'
        else:
            print 'Action not recognized'

