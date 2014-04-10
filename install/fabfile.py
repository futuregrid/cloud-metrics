#!/usr/bin/env python
from fabric.api import task, local
import sys
import platform
import os

def is_ubuntu():
    """test sif the platform is ubuntu"""
    return platform.dist()[0] == 'Ubuntu'

def is_centos():
    """test if the platform is centos"""
    (centos, version, release) = platform.dist()
    if centos == "centos" and version != "6.4":
        print "Warning: centos %s is not tested" % version
    return centos == "centos"

def is_osx():
    return platform.system().lower() == 'darwin'

@task
def deploy():
    """deploys the system on supported distributions"""
    # download()
    (major, minor, micro, releaselevel, serial) = sys.version_info
    if major != 2 or (major == 2 and minor < 7):
        print "Your version of python is not supported.  Please install python 2.7"
        sys.exit()
    if not hasattr(sys, 'real_prefix'):
        print "You do not appear to be in a vitualenv.  Please create and/or activate a virtualenv"
        sys.exit()
    if is_ubuntu():
        ubuntu()
    elif is_centos():
        centos()
    elif is_osx():
        osx()
    else:
        print "OS distribution not supported; please see documatation for manual installation instructions."
        sys.exit()

@task
def download():
    '''downloads'''
    local("git clone git@github.com:futuregrid/cloud-metrics.git")

@task
def install():
    sphinx_updates()
    local("pip install -r requirements.txt")
    local("python setup.py install")

@task
def install_mongodb():
    local("fab mongo.install")

def install_package(package):
    if is_ubuntu():
        local ("sudo apt-get -y install {0}".format(package))
    if is_centos():
        local("sudo yum -y install {0}".format(package))
    elif sys.platform == "darwin":
        print "Not yet supported"
        sys.exit()
    elif sys.platform == "win32":
        print "Windows is not supported"
        print "Use Linux instead"
        sys.exit()

@task
def install_packages(packages):
    for package in packages:
        install_package (package)

@task
def ubuntu():
    '''prepares an system and installs all 
    needed packages before we install cloudmesch'''

    local ("sudo apt-get update")
    install_packages(["git",
                      "python-dev",
                      "libmysqlclient-dev"])    
    install()
    install_mongodb()#important that mongo_db installation be done only after all we install all needed python packages(as per requiremnts.txt)

def centos():
    install_packages (["git",
                       "wget",
                       "gcc",
                       "make",
                       "python-dev",
		       "libmysqlclient-dev"])
    
    install()
    install_mongodb() 

def osx():
    local('brew install wget')
    
    install()
    install_mongodb()
