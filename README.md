[![Build Status](https://travis-ci.org/xnaveira/foreman-host-builder.svg?branch=master)](https://travis-ci.org/xnaveira/foreman-host-builder)

# foreman-host-builder

This package contains a script that uses the python-foreman module to build a set of hosts in foreman

IMPORTANT: At the moment it is only tested with vmware and ovirt backends. Amazon and Google are under development.

* foreman-host-builder.py

The configuration resides in the file *config.cfg*.

## Installation

Get the code from this repository:

                git clone https://github.com/xnaveira/foreman-host-builder

Use the installation script to install it and get the dpeendencies:

                cd foreman-host-builder; python setup.py install


Or, if you are only interested in the script:

                pip install foreman-host-builder

## Configuration

The configuration in *config.cfg* can either be manually edited or entered at script execution time. If you are editing the file manually you have to enconde the passwords in base64.

If any of the values in *config.cfg* is not initialized, the script will ask for them and offer the possibility of saving those values to the file. The passwords are obfuscated with base64 encoding, while this offers no security (that should be provided by the right management of user permissions) it does difficult the fact of someone seeing the password while you are editing the file.

The configuration values are the addresses and credentials of the systems used by the scripts, these are:

* Foreman REST api

----

## foreman-host-builder.py

This is a script that creates a set of virtual machines using the foreman API. It aims to work independently of what virtualization provider the Foreman is using.

The script assumes that the foreman instance that it will be using is configured and able to create machines by itself.

The way it works is taking as input a template file in a given format. In the template a set of parameters are supplied, hostname, operating system, ip address and so on. The template file format is explained in detail bellow.


**Needs to be prepared in foreman**

The following elements must be prepared in foreman before attempting to create the machines

* location
* domain
* subnet


## Template file format

The template format is a yaml file, look into the provided template_example.yml for an example

```
#This is the template for the script input. It uses YAML that we'll be loaded as
#a dictionary. The special key common contains the defaults common to all the
#servers and will be removed from the dictionary once loaded.
#Make sure that the values corresponds with the names in Foreman (case
#sensitive)
servers:
  common: &defaults
    domain: domain.net
    location: thelocation
    subnet: thesubnet
    environment: production
    architecture: x86_64
    compute_resource: examplevmware
    hostgroup: thehostgroup
    compute_profile: examplesmall
    operatingsystem: Ubuntu 12.04
    ptable: default
    media: Ubuntu
    puppet_ca_proxy: puppetserver
    puppet_proxy: puppetserver
  server1:
    ip: 1.2.3.4
    mac: 12:34:56:78:90:ab
    <<: *defaults
  server2:
    ip: 1.2.3.5
    mac: 12:34:56:78:90:ac
    <<: *defaults
```


## Command line arguments

From running `./foreman-host-builder.py`:

           ./foreman-host-builder [OPTIONS]
           
            Creates a set of machines on the foreman server specified in config.py
           
            -t , --template <template_file>
                 the template file containing the lst with machines to be created and their configuration parameters
           

 
