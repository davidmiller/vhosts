""" Lists current vhosts """
import os
import re 
import vlogging
from vhosts import VirtualHost


class List:
    """ gets list of vhosts """


    def get_vhosts( self ):
        """Builds the list of Virtual Hosts"""
        self.sites_available = []
        self.created_RE = re.compile( '#VirtualHost created by localsite.py' )
        vlogging.ret_logger.debug( 'listing localsites now' )
        available_dir = '/etc/apache2/sites-available'
        sites_available = os.listdir( available_dir )
        vlogging.ret_logger.info( sites_available )
        sites_enabled = os.listdir( '/etc/apache2/sites-enabled' )        
        for item in sites_available:
            file_path = os.path.join( available_dir, item )
            if os.path.isfile( file_path ):
                f = open( file_path, 'rb' )
                # Check to see if the site was created by vhosts.py
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


if __name__ == "__main__":
    list = List()
    print(list.list_sites())
