#!/usr/bin/env python
"""
get_mac_from_ipmi.py

The purpose of this script is to convert a list of IPMI (BMC interfaces) MAC
addresses and return the first mac address of the host they are managing.

"""
from __future__ import print_function
# -*- coding: utf-8 -*-
__authors__ = 'Xavier Naveira <xavier.naveira@videoplaza.com>'
__date__ = '11/02/2015'
__version__ = '0.1'

import sys
import re
import subprocess

# CONSTANTS

ipmi_commands = { \
        'get_mac_address' : "ipmitool -H {ipmi_address} -U {ipmi_user} -P {ipmi_password} raw 0x30 0x21 | cut -d ' ' -f 6- | tr ' ' ':'",
    }

ipmi_user = 'ADMIN'
ipmi_password = 'ADMIN'


ERROR = 'error'
WARNING = 'warning'
INFO = 'info'
DEBUG = 'debug'

msg_level = { \
        'error'     : '\033[1;31m', #red
        'warning'   : '\033[1;33m', #yellow
        'info'      : '\033[1;32m', #green
        'debug'     : '\033[1;35m', #magenta
    }


# FUNCTIONS

def output_mesg(level, msg):
    """
    Uses the level to prefix and color the output message.
    warning and info levels are sent to stdout
    debug and error levels are sent to stderr
    """
    print('{}{}: {}'.format(msg_level[level], level.upper(), msg), file=sys.stderr if level == 'error' or 'debug' else sys.stdout)
    return

def match_pattern(pattern, line):
    """
    Given a pattern (regex) and a line (string) returns the result of trying to match the pattern to the line
    """
    return re.match(pattern, line)

def is_mac_address(line):
    """
    Returns True if line is in a valid mac address format, False otherwise
    """
    pattern = r'^(?i)([0-9A-F]{2}[:-]){5}([0-9A-F]{2})$'
    return match_pattern(pattern, line)

def is_ipv4_address(line):
    """
    Returns True if line is in a valid mac address format, False otherwise
    """
    pattern = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    return match_pattern(pattern, line)

#MAIN

def main():
    """
    main function
    """
    if not sys.stdin.isatty():
        data = sys.stdin.read()
        for line in data.splitlines():
            #output_mesg(DEBUG, line)
            if line != '' and is_ipv4_address(line):
                cmd = ipmi_commands['get_mac_address'].format(ipmi_address=line, ipmi_user=ipmi_user, ipmi_password=ipmi_password)
                result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell='True')
                #output_mesg(DEBUG, result)
                if not re.match('^Error.*', result) and is_mac_address(result):
                    #print(result)
                    sys.stdout.write(result)
                    continue
            print('E')
    else:
        output_mesg(ERROR, 'No data in stdin found')
        print('\033[0;37m\nget_mac_from_ipmi.py: Utility to retrieve a Supermicro server system mac address from the IPMI information.\n \
\nGiven a list of ip addresses in stdin (that corresponds to Supermicro IPMIs) it will return the primary MAC address for the manged server \
or "E" if the MAC can\'t be retrieved')
        exit(1)

if __name__ == "__main__":
    main()
