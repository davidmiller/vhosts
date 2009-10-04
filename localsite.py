#!/usr/bin/env python
""" Manages sites on the local machine for
development purposes.

Retrieve is just a placeholder for now

Version 0.01
Author David Miller
"""
import logging
import logging.handlers
import os
import pwd
import re
import subprocess
import argparse


class LocalSite:
    """LocalSite Class """

    def create(self):
        """Creates a site"""
        create_logger.debug('Trying to create %s' % args.name)
        # Check for Create mode

        if args.dir:
            if args.dir[-1:] == '/': args.dir = args.dir[:-1]
            #clean up the Document root
            abs_dir = os.path.join(args.dir,args.name)

        # Create an entry in /etc/hosts
        host_instance = self.host_tpl % {'files': abs_dir, 'site':args.name}
        file = open('/etc/hosts', 'a')
        file.write(host_instance)
        file.close()

        # Create the vhosts conf file for the new site
        conf_filename = args.name+'.conf'
        conf_location = os.path.join('/etc/apache2/sites-available/',conf_filename)
        file = open(conf_location, 'w')
        file.write(self.virtualhost_tpl % {'site': args.name, 'dir': abs_dir})
        file.close()

        # create the symlink in sites enabled
        os.chdir('/etc/apache2/sites-enabled')
        os.symlink(conf_location, conf_filename)

        # Restart apache
        subprocess.call(['apache2ctl', 'restart'])

        # Drop the permissions down to create the Document root
        uid = pwd.getpwnam( os.getlogin() )[2]
        gid = pwd.getpwnam( os.getlogin() )[3]
        os.setgid( gid )
        os.setuid( uid )

        # Check for the directory, create if it doesn't exist yet
        if os.path.isdir( abs_dir ):
            pass
        else:
            os.mkdir( abs_dir )

        # Create boilerplate structure if selected
        if args.structure:
            os.mkdir( os.path.join( abs_dir,'css' ) )
            os.mkdir( os.path.join( abs_dir,'js' ) )    
            os.mkdir( os.path.join( abs_dir,'images' ) )      

        # Create the index file for the new site
        file = open( abs_dir+'/index.html', 'w' )
        file.write( 'Hello Beautful World' )
        file.close()
        print 'site created'

    def enable_multiple_sites( self ):
        return False


    def get_vhosts( self ):
        """Builds the list of Virtual Hosts"""
        self.sites_available = []
        self.created_RE = re.compile( '#VirtualHost created by localsite.py' )
        ret_logger.debug( 'listing localsites now' )
        available_dir = '/etc/apache2/sites-available'
        sites_available = os.listdir( available_dir )
        ret_logger.info( sites_available )
        sites_enabled = os.listdir( '/etc/apache2/sites-enabled' )        
        for item in sites_available:
            file_path = os.path.join( available_dir, item )
            if os.path.isfile( file_path ):
                f = open( file_path, 'rb' )
                if self.created_RE.match( f.read( 36 ) ):
                    if item in sites_enabled:
                        enabled = True
                    else:
                        enabled = False
                    vhost = VirtualHost( item, enabled )
                    self.sites_available.append( vhost )
                f.close()
        return self.sites_available


    def list_sites( self ):
        """Lists local sites"""
        self.get_vhosts()
        vhost_fmt = "Enabled? %s || Name: %s \n"
        vhost_list = []
        for site in self.sites_available:
            vhost_list.append( vhost_fmt % ( site.enabled, site.name ) )
        return "".join( vhost_list )


    def __init__( self ):
        self.host_tpl = """
# Local development site created by localsite
# files stored at %(files)s
127.0.0.1    %(site)s
127.0.0.1    www.%(site)s
        """

        self.virtualhost_tpl ="""#VirtualHost created by localsite.py
<VirtualHost 127.0.0.1:80>
ServerName %(site)s
ServerAdmin webmaster@localhost
ServerAlias www.%(site)s
DocumentRoot %(dir)s
CustomLog /var/log/apache2/%(site)s.log combined
</VirtualHost>"""


class VirtualHost:
    """ Models a VirtualHost"""


    def __init__( self, name = None, enabled = None ):
        self.name = name
        self.enabled = enabled

        
if __name__ == '__main__':
    package_description = """Create a development site on your local apache"""
    parser = argparse.ArgumentParser( description=package_description )
    parser.add_argument( '-s', '--structure',
                         action='store_true',
                         help='create boilerplate directory structure' )
    parser.add_argument( '-l', '--list',
                         action='store_true',
                         help='List all current LocalSites' )
    parser.add_argument( '-n', '--name',
                         help='Name of the site' )
    parser.add_argument( '-d', '--dir',
                         help='Absolute path to the site directory' )
    parser.add_argument( '--debug',
                         action='store_true',
                         help='Turn on debugging notices')
    args = parser.parse_args()


    #  Define logging behaviour
    LOG_FILENAME = '.localsite.log'
    if args.debug:
        console_level = logging.DEBUG
    else:
        console_level = logging.ERROR

    ret_logger = logging.getLogger( 'retrieve' )
    create_logger = logging.getLogger( 'create' )

    logformat = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter( logformat )

    create_logger.setLevel( logging.DEBUG )
    ret_logger.setLevel( logging.DEBUG )

    file_handler = logging.FileHandler( LOG_FILENAME )
    file_handler.setFormatter( formatter )
    file_handler.setLevel( logging.ERROR )
    console_handler = logging.StreamHandler()
    console_handler.setFormatter( formatter )
    console_handler.setLevel( console_level )

    create_logger.addHandler( file_handler )
    create_logger.addHandler( file_handler )
    create_logger.addHandler( console_handler )
    ret_logger.addHandler( file_handler )
    ret_logger.addHandler( console_handler )


    # Initialize class
    site = LocalSite()

    # Check for Retrive mode
    if args.list == True:
        print site.list_sites()
        ret_logger.debug( site.sites_available )
        
    # Check for Create mode
    if args.dir and args.name:
        site.create()
