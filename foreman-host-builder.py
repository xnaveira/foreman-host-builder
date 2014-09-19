#!/usr/bin/python
"""
foreman-host-builder.py: Given a text file based template builds that environment in
foreman.

See README.md
"""

from imports import *

def _usage():
    print ""
    print "./foreman-host-builder [OPTIONS]"
    print ""
    print " Creates a set of machines on the foreman server specified in config.py"
    print ""
    print " -t , --template <template_file>"
    print "      the template file containing the lst with machines to be created and their configuration parameters"

def _template_parser(filename):
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
    except IOError, e:
        print(red("Error: " + str(e)))
        exit(5)
    i=0
    servers = {}
    for l in lines:
        if "#" not in l and l not in ['\n','\r\n']:
            l=l.rstrip('\r\n')
            params = l.split(";")
            if len(params) != 13:
                raise ValueError(red('Wrong number of params in line ' + str(i)))
            servers[params[0]] = {}
            servers[params[0]]['domain']=params[1]
            servers[params[0]]['location']=params[2]
            servers[params[0]]['subnet']=params[3]
            servers[params[0]]['environment']=params[4]
            servers[params[0]]['architecture']=params[5]
            servers[params[0]]['compute_resource']=params[6]
            servers[params[0]]['hostgroup']=params[7]
            servers[params[0]]['compute_profile']=params[8]
            servers[params[0]]['operatingsystem']=params[9]
            servers[params[0]]['ip']=params[10]
            servers[params[0]]['ptable']=params[11]
            servers[params[0]]['media']=params[12]
        i=i+1
    return servers

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "t:h", ["template=","help"])
    except getopt.GetoptError as err:
        print(red(str(err)))
        _usage()
        sys.exit(3)

    if opts == [] or len(opts) > 1:
        _usage()
        sys.exit(4)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            _usage()
            sys.exit(0)
        elif opt in ("-t", "--template"):
            template = arg

    print "Building ..."

#READ TEMPLATE

    servers=_template_parser(template)

#CONNECT TO FOREMAN INSTANCE

    foreman_api = Foreman('http://' + configdict['foreman_server'],(configdict['foreman_username'],configdict['foreman_password']),api_version=configdict['foreman_api_version'])

#SERVER PARAMETERS ID

    #This is the dictionary holding the host creation query parameters 
    build_dict = {}

    for server in servers:
        print ''
        print 'Getting parameters for ' + cyan(server) + '...'


        build_dict['hostgroup_id'] = foreman_api.hostgroups.show(id=servers[server]['hostgroup'])['id']
        print 'Hostgroup ' + cyan(servers[server]['hostgroup']) + ' has id: ' + cyan(build_dict['hostgroup_id'])

        build_dict['domain_id'] = foreman_api.domains.show(id=servers[server]['domain'])['id']
        print 'Domain ' + cyan(servers[server]['domain']) + ' has id: ' + cyan(build_dict['domain_id'])

        build_dict['architecture_id'] = foreman_api.architectures.show(id=servers[server]['architecture'])['id']
        print 'Architecture ' + cyan(servers[server]['architecture']) + ' has id: ' + cyan(build_dict['architecture_id'])

        build_dict['compute_resource_id'] = foreman_api.compute_resources.show(id=servers[server]['compute_resource'])['id']
        print 'Compute Resource ' + cyan(servers[server]['compute_resource']) + ' has id: ' + cyan(build_dict['compute_resource_id'])

        build_dict['name'] = server
        print 'Name: ' + cyan(server)

        build_dict['subnet_id'] = foreman_api.subnets.show(id=servers[server]['subnet'])['id']
        print 'Subnet ' + cyan(servers[server]['subnet']) + ' has id: ' + cyan(build_dict['subnet_id'])

        build_dict['operatingsystem_id'] = foreman_api.operatingsystems.show(id=servers[server]['operatingsystem'])['id']
        print 'Operating System ' + cyan(servers[server]['operatingsystem']) + ' has id: ' + cyan(build_dict['operatingsystem_id'])

        build_dict['ptable_id'] = foreman_api.ptables.show(id=servers[server]['ptable'])['id']
        print 'Partition Table ' + cyan(servers[server]['ptable']) + ' has id: ' + cyan(build_dict['ptable_id'])

        build_dict['medium_id'] = foreman_api.media.show(id=servers[server]['media'])['id']
        print 'Media ' + cyan(servers[server]['media']) + ' has id: ' + cyan(build_dict['medium_id'])

        build_dict['environment_id'] = foreman_api.environments.show(id=servers[server]['environment'])['id']
        print 'Environment ' + cyan(servers[server]['environment']) + ' has id: ' + cyan(build_dict['environment_id'])

        build_dict['compute_attributes'] = {}

        #Find out compute attributes in compute_resource knowing the compute_profile 
        for compute_profiles in foreman_api.compute_resources.show(id=servers[server]['compute_resource'])['compute_attributes']:
            if compute_profiles['compute_profile_name'] == servers[server]['compute_profile']:
                build_dict['compute_attributes'].update(compute_profiles['vm_attrs'])
                print 'Compute attributes for ' + cyan(servers[server]['compute_profile']) + ' are: ' + cyan(compute_profiles['vm_attrs'])

        subnets = foreman_api.subnets.index()['results']
        subnets_dict = {}
        for subnet in subnets:
            subnets_dict[subnet['id']] = subnet['vlanid']

        for network in foreman_api.compute_resources.available_networks(id=build_dict['compute_resource_id'],cluster_id=build_dict['compute_attributes']['cluster'])['results']:
            vlanid = subnets_dict[build_dict['subnet_id']]
            if vlanid in network['name']:
                build_dict['compute_attributes'].update({'nics_attributes':{ '0':{ 'name':'NIC1', 'network':network['id'] } } })
                build_dict['compute_attributes']['interfaces_attributes'].clear()
                build_dict['compute_attributes']['interfaces_attributes'].update({ '0':{ 'name':'NIC1', 'network':network['id'] } })
                print 'Network ' + cyan(servers[server]['subnet']) + ' with VLAN_ID ' + cyan(vlanid) + ' in ' + cyan(servers[server]['compute_resource']) + ' ' + cyan(build_dict['compute_attributes']['cluster']) + ' has id: ' + cyan(network['id'])

#SERVER BUILD
        #Setup the machine to be started upon creation
        build_dict['compute_attributes']['start'] = '1'
        build_dict['build'] = 'true'
        print ''
        print 'Requesting machine creation...'

        try:
            foreman_api.hosts.create(host=build_dict)
            print green('Machine created')
        except ForemanException, e:
            print red(str(e) + ', see error description above')

if __name__ == "__main__":
    main(sys.argv[1:])
