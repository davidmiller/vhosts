""" Creates an apache VirtiualHost instance """
import os
import subprocess
import sys
import vlogging

            
host_tpl = """
# Local development site created by localsite
# files stored at %(files)s
127.0.0.1    %(site)s
127.0.0.1    www.%(site)s
        """

virtualhost_tpl ="""#VirtualHost created by localsite.py
<VirtualHost 127.0.0.1:80>
ServerName %(site)s
ServerAdmin webmaster@localhost
ServerAlias www.%(site)s
DocumentRoot %(dir)s
CustomLog /var/log/apache2/%(site)s.log combined
</VirtualHost>"""


class Create:
    """ Creates an apache VirtiualHost instance """


    def create( self ):
        """Creates a site"""
        vlogging.create_logger.debug( 'Trying to create %s' % self.args.name )
        import vhosts
        if vhosts.has_root_perms( 'create' ):
            self.get_web_root()
            self.make_hosts_entry()
            self.make_conf()

            vhosts.enable( self.conf_loc, self.conf_name )
            vhosts.apache_restart()

            self.drop_perms()
            self.make_web_root()
            print "\nYeah! %s created!" % self.args.name


    def get_web_root( self ):
        """ Determine the web root """
        if self.args.dir:
            print 'yes to args.dir'
            #clean up the Document root
            if args.dir[-1:] == '/': args.dir = args.dir[:-1]
        else:
            self.args.dir = os.getcwd()            
        self.web_root = os.path.join( self.args.dir, self.args.name )


    def make_hosts_entry( self ):
        """ Adds an entry to /etc/hosts for local development """
        host_entry = host_tpl % {'files': self.web_root, 
                                 'site': self.args.name}
        file = open( '/etc/hosts', 'a' )
        file.write( host_entry )
        file.close()


    def make_conf( self ):
        """ Create the vhost.conf file """
        self.conf_name = self.args.name + '.conf'
        self.conf_loc = os.path.join( '/etc/apache2/sites-available/', self.conf_name )
        file = open( self.conf_loc, 'w' )
        file.write( virtualhost_tpl % {'site': self.args.name, 
                                       'dir': self.web_root } )
        file.close()


    def drop_perms( self ):
        """ Drop the permissions down from root """
        import pwd
        uid = pwd.getpwnam( os.getlogin() )[2]
        gid = pwd.getpwnam( os.getlogin() )[3]
        os.setgid( gid )
        os.setuid( uid )


    def make_web_root( self ):
        """ Make sure the web root dir exists. Create if not """
        if os.path.isdir( self.web_root ):
            pass
        else:
            os.mkdir( self.web_root )
        # Create boilerplate structure if selected
        if self.args.structure:
            os.mkdir( os.path.join( self.web_root,'css' ) )
            os.mkdir( os.path.join( self.web_root,'js' ) )    
            os.mkdir( os.path.join( self.web_root,'images' ) )      
        # Create the index file for the new site
        file = open( os.path.join( self.web_root + '/index.html' ), 'w' )
        file.write( 'Hello Beautful World' )
        file.close()


    def __init__( self, args ):
        self.args = args
        self.create()