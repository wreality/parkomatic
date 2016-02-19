#!/bin/bash
SCRIPTSYMLINK="/usr/local/bin/parkomaticd"
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi
if [ -e $SCRIPTSYMLINK ]; then
	echo "Script symlink already exists.  Delete the file before running this script to reinstall"
else
	echo "Symlinking python script file to: $SCRIPTSYMLINK"
	ln -s $PWD/parkomatic.py $SCRIPTSYMLINK
	chmod +x $SCRIPTSYMLINK
fi
mkdir -p /etc/parkomatic
if [ -e /etc/parkomatic/parkomatic.conf ]; then
	echo "OOPS, config file already exists. NOT overwriting"
else
	echo "Copying config file to: /etc/parkomatic/parkomatic.conf"
	cp etc/parkomatic/parkomatic.conf /etc/parkomatic/parkomatic.conf
fi
if [ -e /etc/init ]; then
	echo "Copying upstart script to: /etc/init/parkomatic.conf"
	cp etc/init/parkomatic.conf /etc/init/parkomatic.conf
	echo "All done.  You can use 'sudo service parkomatic start' to start the parkomatic"
else
	echo "Upstart doesn't seem to be installed.  You'll have to set the script to start automatically on your own."
	echo "Or, install upstart (sudo apt-get install upstart) and rerun this install script"
fi