"""
config.py: Config module for foreman-host-builder.py
"""
import fabric.api
from getpass import getpass
import ConfigParser
import base64

configfile = 'config.cfg'
configdict = {}

configuration = ConfigParser.SafeConfigParser()
test = configuration.read(configfile)

if test == []:
    print "config.cfg file not found, creating it"
    configuration.add_section('foreman')
    configuration.set('foreman','foreman_server','')
    configuration.set('foreman','foreman_username','')
    configuration.set('foreman','foreman_password','')
    configuration.set('foreman','foreman_api_version','2')
    with open(configfile, 'w+') as f:
        configuration.write(f)

user_input = False
sections = configuration.sections()

for section in sections:
    for name,value in configuration.items(section):
        if 'password' in name:
            if value == '':
                user_input = True
                value = base64.b64encode(getpass('Please enter {0} (or set the value in {1}): '.format(name,configfile)))
                configuration.set(section,name,value)
            configdict[name] = base64.b64decode(value)
        else:
            if value == '':
                user_input = True
                value = raw_input('Please enter {0} (or set the value in {1}): '.format(name,configfile))
                configuration.set(section,name,value)
            configdict[name] = value
if user_input:
    answer = raw_input('Do you want to save the configuration to {0}?  (y/N) '.format(configfile))
    if answer == 'Y' or answer == 'y':
        with open(configfile, 'w') as cfile:
            configuration.write(cfile)

