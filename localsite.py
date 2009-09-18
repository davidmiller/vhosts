#!/usr/bin/env python
""" Manages sites on the local machine for
development purposes.
Moved to a CRUD design pattern.

Create completed but not as a class

Retrieve begun

Version 0.01
Author David Miller
"""
import argparse
import os
import pwd
import subprocess

class LocalSite:
    """LocalSite Class """

    def list_sites(self):
        """Lists local sites"""
        print 'Should be listing localsites now'    

    def create(self):
        """Creates a site"""
        print 'should be creating a site now'

    def __init__(self):
        self.data = []

if __name__ == '__main__':
    package_description = """Create a development site on your local apache"""
    parser = argparse.ArgumentParser(description=package_description)
    parser.add_argument('-s', '--structure',
                        action='store_true',
                        help='create boilerplate directory structure')
    parser.add_argument('-l', '--list',
                        action='store_true',
                        help='List all current LocalSites')
    parser.add_argument('-n', '--name',
                        help='Name of the site')
    parser.add_argument('-d', '--dir',
                        help='Absolute path to the site directory')
    args = parser.parse_args()

site = LocalSite()

# Check for Retrive mode
if args.list == True:
    site.list_sites()

# Check for Create mode
if args.dir:
    #clean up the Document root
    if args.dir[-1:] == '/': args.dir = args.dir[:-1]

    abs_dir = os.path.join(args.dir,args.name)


# Create an entry in /etc/hosts
    host_tpl = """
# Local development site created by localsite
# files stored at %(files)s
127.0.0.1    %(site)s
127.0.0.1    www.%(site)s
"""
    host_instance = host_tpl % {'files': abs_dir, 'site':args.name}

    file = open('/etc/hosts', 'a')
    file.write(host_instance)
    file.close()

# Create the vhosts conf file for the new site
    virtualhost_tpl ="""<VirtualHost %(site)s>
ServerAdmin webmaster@localhost
ServerAlias www.%(site)s
DocumentRoot %(dir)s
CustomLog /var/log/apache2/%(site)s.log combined
</VirtualHost>"""

    conf_filename = args.name+'.conf'
    conf_location = os.path.join('/etc/apache2/sites-available/',conf_filename)

    file = open(conf_location, 'w')
    file.write(virtualhost_tpl % {'site': args.name, 'dir': abs_dir})
    file.close()

# create the symlink in sites enabled
    os.chdir('/etc/apache2/sites-enabled')
    os.symlink(conf_location, conf_filename)

# Restart apache
    subprocess.call(['apache2ctl', 'restart'])

# Drop the permissions down to create the Document root
    uid = pwd.getpwnam(os.getlogin())[2]
    gid = pwd.getpwnam(os.getlogin())[3]
    os.setgid(gid)
    os.setuid(uid)

# Check for the directory, create if it doesn't exist yet
    if os.path.isdir(abs_dir):
        pass
    else:
        os.mkdir(abs_dir)


# Create boilerplate structure if selected
if args.structure:
    os.mkdir(os.path.join(abs_dir,'css'))
    os.mkdir(os.path.join(abs_dir,'js'))    
    os.mkdir(os.path.join(abs_dir,'images'))
    
# Create the index file for the new site
    file = open(abs_dir+'/index.html', 'w')
    file.write('Hello Beautful World')
    file.close()

