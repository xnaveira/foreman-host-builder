#!/usr/bin/env python
import argparse
import re

def parse_args():
    """
    Parse command line arguments, also formats help.
    """
    parser = argparse.ArgumentParser(description="Given a list with ipmi-mac and another with mac-port creates a list with ipmi-mac-port")
    parser.add_argument('-i', '--ipmif', action='store', help='File with the ordered list of ipmi and mac addresses pairs, one per line')
    parser.add_argument('-p', '--portf', action='store', help='File with the ordered list of mac and port addresses pairs, one per line')
    args = parser.parse_args()
    return args

def load_file_to_dict(ifile):
    res_dict = {}
    for line in ifile.readlines():
        #print line
        if not re.match('^#.*$',line):
            sline = line.strip('\n').split(' ')
            #print sline
            if not len(sline) == 2:
                print 'ERROR: Lines must contain two elements separated by one space'
                exit(1)
            else:
                res_dict[sline[0]] =  sline[1]
    return res_dict

def main():
    arguments = parse_args()
    with open (arguments.ipmif, 'r+') as ipmif:
        ipmid = load_file_to_dict(ipmif)
    with open (arguments.portf, 'r+') as portf:
        portd = load_file_to_dict(portf)
    imd = {}
    for ipmi, mac in ipmid.iteritems():
        try:
            imd[ipmi] = portd[mac]
        except:
            imd[ipmi] = 'NO_MAC'
    for ipmi, mac in imd.iteritems():
        print '{} {}'.format(ipmi,mac)


if __name__ == "__main__":
    main()
