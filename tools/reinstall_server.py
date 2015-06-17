#!/usr/bin/env python

import urllib2
import re
import sys
import sh

sys.path.append('..')
from fhb.imports import *

from getpass import getpass

def ipmi_from_host(hostfqdn):
    p = re.match('^.*\.(.*)\.videoplaza.net',hostfqdn)
    return hostfqdn.replace(p.group(1),'oob')


def check_oob_connection(ipmifqdn):
    print 'https://' + ipmifqdn
    try:
        response=urllib2.urlopen('https://' + ipmifqdn,timeout=1)
        return True
    except urllib2.URLError as err:
        pass
    return False


if __name__ == '__main__':

    hostfqdn = sys.argv[1]
    ipmifqdn = ipmi_from_host(hostfqdn)

    if check_oob_connection(ipmifqdn):
        print green('Connected to the oob network!')
    else:
        print red('You need to connect to the oob network in order for this script to work.')
        exit(1)

    print 'Making sure that the host ' +  cyan('{}'.format(hostfqdn)) + ' is in build state...'
    foreman_api = Foreman('http://' + configdict['foreman_server'],(configdict['foreman_username'],configdict['foreman_password']),api_version=configdict['foreman_api_version'])
    build_dict = {}
    build_dict['build'] = True
    r = foreman_api.hosts.update(id=hostfqdn,host=build_dict)
    if r == []:
        print red('Host ') + cyan('{}'.format(hostfqdn)) + red(' not found in foreman, aborting.')
        exit(2)

    ipass = getpass('Enter IPMI password for ' + cyan('{}'.format(hostfqdn)) + ': ')
    print red('You are about to reboot and reinstall ') + cyan(hostfqdn) + red('. ALL information will be ERASED')
    sure = raw_input(red('If you are sure write "reinstall": '))
    if sure.lower() == 'reinstall':
        print 'Seting pxe boot at ' + cyan('{}'.format(ipmifqdn)) 
        sh.ipmitool('-H',ipmifqdn,'-U','ADMIN','-P',ipass,'chassis','bootdev','pxe')
        print red('Rebooting ') + cyan('{}'.format(hostfqdn)) 
        sh.ipmitool('-H',ipmifqdn,'-U','ADMIN','-P',ipass,'chassis','power','reset')
        exit(0)
    else:
        print red('Reinstallation of ') + cyan('{}'.format(hostfqdn)) + red(' CANCELLED')
        exit(3)
