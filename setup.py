#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    print 'Please install setuptools before running this script:'
    print ' sudo pip install setuptools'
    print ' sudo apt-get install python-setuptools'
    print ' sudo yum install python-setuptools'
    exit(1)

setup(name='foreman-host-builder',
      version='1.0',
      description='Build hosts in Foreman from a template file',
      author='Xavier Naveira',
      author_email='xnaveira@gmail.com',
      url='',
      install_requires=['python-foreman','fabric','ConfigParser'],
     )
