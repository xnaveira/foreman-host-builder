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
      version='2.1',
      description='Build hosts in Foreman from a template file',
      author='Xavier Naveira',
      author_email='xnaveira@gmail.com',
      url='https://github.com/xnaveira/foreman-host-builder',
      install_requires=['python-foreman','fabric','ConfigParser'],
      scripts=['foreman-host-builder.py'],
      packages=['fhb'],
     )
