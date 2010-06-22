#!/usr/bin/env python
""" 
Commandline API for Apache Virtual Hosts

Version 0.01
Author David Miller
"""
import os
import sys
import argparse

perms_fail = """
###################################

Modifying VirtualHosts requires root privileges
because there are a bunch of files in root owned
directories that need modifying or creating

Try running the %s command with sudo

###################################\n"""

def has_root_perms( context ):
    """ Check to see that we have permission to edit root owned files"""
    if os.environ['USER'] != 'root':
        print perms_fail % context
        sys.exit()
    else: 
        return True


def apache_restart():
    """ Restarts the apache server """
    import subprocess
    subprocess.call( ['apache2ctl', 'restart'] )


def enable( conf_loc, conf_name ):
    """ Enable a site by creating a symlink """
    if has_root_perms( 'enable' ):
        if os.path.isfile( conf_loc ):
            os.chdir( '/etc/apache2/sites-enabled' )
            os.symlink( conf_loc, conf_name )
        else:
            print """Sorry, but there doesn't seem to be an apache VirtualHost
configuration file for %s 
You might like to check the spelling or perhaps create the site
            """ % conf_loc
            sys.exit()
    return True


def disable( name ):
    """ Disable a virtualhost by removing the symlink """
    if has_root_perms( 'disable' ):
        name += '.conf'
        link = os.path.join( '/etc/apache2/sites-enabled', name )
        if os.path.islink( link ):
            os.unlink( link )
        else:
            print """Sorry, but the site '%s' doesn't seem to be enabled.
You might like to check your spelling""" % name
            sys.exit()
    return True


class VirtualHost:
    """ Models a VirtualHost"""


    def __init__( self, name = None, enabled = None ):
        self.name = name
        self.enabled = enabled


class Vhosts:
    """ Dispatcher class for main program """


    def list( self ):
        """" List the vhosts """
        import list
        self.do_list = list.List()
        print self.do_list.list_sites()


    def create( self ):
        """ Create a new Virtual Host """
        import create
        self.do_create = create.Create( args )


    def enable( self ):
        """ Enable a VirtuaHost """
        filename = args.site + '.conf'
        location = os.path.join( '/etc/apache2/sites-available', filename )
        enable( location, filename )
        apache_restart()
        print "\n%s enabled!\n" %args.site


    def disable( self ):
        """ Disable a VirtualHost """
        disable( args.site )
        apache_restart()
        print "\n%s disabled!\n" % args.site

        
if __name__ == '__main__':


    # Initialize class
    vhosts = Vhosts()


    # Set arguments
    program = 'Vhosts'
    parser = argparse.ArgumentParser( prog = program )
    parser.add_argument( '--debug',
                         action='store_true',
                         help='Turn on debugging notices')
    subparsers = parser.add_subparsers( help = 'sub command help' )


    parser_list = subparsers.add_parser( 'list',
                                          help = 'List VirtualHosts' )
    parser_list.set_defaults( func = vhosts.list )


    parser_create = subparsers.add_parser( 'create', help = 'Create a VirtualHost' )
    parser_create.add_argument( '-s', '--structure',
                                action='store_true',
                                help='create boilerplate directory structure' )
    parser_create.add_argument( 'name',
                                help='Name of the site' )
    parser_create.add_argument( '-d', '--dir',
                                help='Absolute path to the site directory' )
    HANDLER_HELP = 'Add an application-x handler for common languages'
    HANDLER_CHOICES = ['php']
    parser_create.add_argument( '-a', '--add-handler',
                                help=HANDLER_HELP, choices=HANDLER_CHOICES )
    parser_create.set_defaults( func = vhosts.create )


    parser_disable = subparsers.add_parser( 'disable',
                                            help = 'Disable a VirtualHost' )
    parser_disable.add_argument( 'site',
                                 help = 'Name of the site to disable e.g. example.com' )
    parser_disable.set_defaults( func = vhosts.disable )                                            


    parser_enable = subparsers.add_parser( 'enable',
                                           help = 'Enable a VirtualHost' )
    parser_enable.add_argument( 'site',
                                help = 'Name of the site to enable e.g. example.com' )
    parser_enable.set_defaults( func = vhosts.enable )


    args = parser.parse_args()
    args.func()
