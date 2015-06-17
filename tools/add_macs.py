#!/usr/bin/env python
import argparse
import yaml
import pprint

def parse_args():
    """
    Parse command line arguments, also formats help.
    """
    parser = argparse.ArgumentParser(description="JunOS configuration creator")
    parser.add_argument('-m', '--macf', action='store', help='File with the ordered list of ipmi and mac addresses pairs, one per line')
    parser.add_argument('-y', '--yamlf', action='store', help='YAML file containing the foreman-host-builder template')
    args = parser.parse_args()
    return args

def lookup_server_by_ipmi(servers, ipmi):
    for server in servers:
        try:
            if servers[server]['ipmi'] == ipmi:
                return server
        except:
            pass
    print 'ERROR: Ipmi {} not found in servers template.'.format(ipmi)
    exit(1)

def main():
    arguments = parse_args()
    with open(arguments.yamlf, 'r+') as yamlf:
        servers = yaml.load(yamlf)
        with open(arguments.macf, 'r') as macf:
            macs = [(tuple.split(' ')[0], tuple.split(' ')[1]) for tuple in macf.read().splitlines()]
            if len(macs) != len(servers) -1:
                print 'ERROR: Number of macs ({}) different from number of servers ({}).'.format(len(macs),len(servers)-1)
                exit(1)
        for pair in macs:
            servers[lookup_server_by_ipmi(servers, pair[0])]['mac'] = pair[1]
        yamlf.seek(0)
        yamlf.write(yaml.dump(servers, default_flow_style=False))

if __name__ == "__main__":
    main()
