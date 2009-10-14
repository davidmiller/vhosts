#!/usr/bin/env python
""" 
Commandline API for Apache Virtual Hosts

Version 0.01
Author David Miller
"""
import sys
import argparse


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
                                          help = 'List localsites' )
    parser_list.set_defaults( func = vhosts.list )


    parser_create = subparsers.add_parser( 'create', help = 'Create a localsite' )
    parser_create.add_argument( '-s', '--structure',
                                action='store_true',
                                help='create boilerplate directory structure' )
    parser_create.add_argument( 'name',
                                help='Name of the site' )
    parser_create.add_argument( '-d', '--dir',
                                help='Absolute path to the site directory' )
    parser_create.set_defaults( func = vhosts.create )
    args = parser.parse_args()
    args.func()
