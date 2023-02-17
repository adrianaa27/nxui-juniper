import napalm
import sys
import os
import json
from napalm import get_network_driver
from rich import print as rprint

#getting device info
''''
junos_driver = get_network_driver('junos')
devices = [['10.100.0.8','junos']]
network_devices = []
for device in devices:
    if device[1] == "junos":
        network_devices.append(
                        junos_driver(
                        hostname = device[0],
                        username = "test",
                        password = "H@ppyrout3"
                        )
                            )
print(network_devices)                            
for device in network_devices:
    device.open() 
 '''
    #with junos_driver(device) as getdevice:
junos_driver = get_network_driver('junos')
with junos_driver('10.100.0.8', 'test', 'H@ppyrout3') as device:
    lldp_result = device.get_lldp_neighbors_detail()
    facts_result = device.get_facts()
    #print(facts_result)
    lldp_data = {}
    facts = {}
    for fact, output in facts_result.items():
        device_fqdn = facts_result['fqdn']
        if not device_fqdn:
            device_fqdn = facts_result['hostname']
        if not device_fqdn:
            device_fqdn = device
        facts[device_fqdn] = facts_result
        facts['role'] = facts_result['model']
        facts['ip'] = facts_result['fqdn']
        lldp_data[device_fqdn] = facts_result['interface_list']
    rprint(facts)   
    for port, port_details in lldp_result.items():
        lldp_data[device_fqdn] = lldp_result
    #rprint(lldp_data)
        
    interface_full_name_map = {
        'Eth': 'Ethernet',
        'Fa': 'FastEthernet',
        'Gi': 'GigabitEthernet',
        'Te': 'TenGigabitEthernet',
        }
    def if_fullname(ifname):
        for k, v in interface_full_name_map.items():
            if ifname.startswith(v):
                return ifname
            if ifname.startswith(k):
                return ifname.replace(k, v)
        return ifname

    def if_shortname(ifname):
        for k, v in interface_full_name_map.items():
            if ifname.startswith(v):
                return ifname.replace(v, k)
        return ifname

    def extract_lldp_details(lldp_data_dict):
        """
        LLDP data dict parser.
        Returns set of all the discovered hosts,
        LLDP capabilities dict with all LLDP-discovered host,
        and all discovered interconections between hosts.
        """
        discovered_hosts = set()
        lldp_capabilities_dict = {}
        global_interconnections = []
        for host, lldp_data in lldp_data_dict.items():
            if not host:
                continue
            discovered_hosts.add(host)
            if not lldp_data:
                continue
            for interface, neighbors in lldp_data.items():
                for neighbor in neighbors:
                    if not neighbor['remote_system_name']:
                        continue
                    discovered_hosts.add(neighbor['remote_system_name'])
                    if neighbor['remote_system_enable_capab']:
                        # In case of multiple enable capabilities pick first in the list
                        lldp_capabilities_dict[neighbor['remote_system_name']] = (
                            neighbor['remote_system_enable_capab'][0]
                        )
                    else:
                        lldp_capabilities_dict[neighbor['remote_system_name']] = ''
                    # Store interconnections in a following format:
                    # ((source_hostname, source_port), (dest_hostname, dest_port))
                    local_end = (host, interface)
                    remote_end = (
                        neighbor['remote_system_name'],
                        if_fullname(neighbor['remote_port'])
                    )
                    # Check if the link is not a permutation of already added one
                    # (local_end, remote_end) equals (remote_end, local_end)
                    link_is_already_there = (
                        (local_end, remote_end) in global_interconnections
                        or (remote_end, local_end) in global_interconnections
                    )
                    if link_is_already_there:
                        continue
                    global_interconnections.append((
                        (host, interface),
                        (neighbor['remote_system_name'], if_fullname(neighbor['remote_port']))
                    ))
        return [discovered_hosts, global_interconnections, lldp_capabilities_dict]
    
    #rprint(extract_lldp_details(lldp_data))

    #GLOBAL_LLDP_DATA, GLOBAL_FACTS  = normalize_result(get_host_data_result)
    TOPOLOGY_DETAILS = extract_lldp_details(lldp_data)

icon_capability_map = {
    'router': 'router',
    'switch': 'switch',
    'bridge': 'switch',
    'station': 'host'
}

icon_model_map = {
    'CSR1000V': 'router',
    'Nexus': 'switch',
    'IOSXRv': 'router',
    'IOSv': 'switch',
    '2901': 'router',
    '2911': 'router',
    '2921': 'router',
    '2951': 'router',
    '4321': 'router',
    '4331': 'router',
    '4351': 'router',
    '4421': 'router',
    '4431': 'router',
    '4451': 'router',
    '2960': 'switch',
    '3750': 'switch',
    '3850': 'switch',
    'EX4300': 'switch',
    'EX2200':'switch',
    'SRX340':'switch'
}

def get_icon_type(device_cap_name, device_model=''):
    """
    Device icon selection function. Selection order:
    - LLDP capabilities mapping.
    - Device model mapping.
    - Default 'unknown'.
    """
    if device_cap_name:
        icon_type = icon_capability_map.get(device_cap_name)
        if icon_type:
            return icon_type
    if device_model:
        # Check substring presence in icon_model_map keys
        # string until the first match
        for model_shortname, icon_type in icon_model_map.items():
            if model_shortname in device_model:
                return icon_type
    return 'unknown'

def generate_topology_json(*args):
    """
    JSON topology object generator.
    Takes as an input:
    - discovered hosts set,
    - LLDP capabilities dict with hostname keys,
    - interconnections list,
    - facts dict with hostname keys.
    """
    discovered_hosts, interconnections, lldp_capabilities_dict, facts = args
    host_id = 0
    host_id_map = {}
    topology_dict = {'nodes': [], 'links': []}
    for host in discovered_hosts:
        device_model = 'n/a'
        device_serial = 'n/a'
        device_ip = 'n/a'
        if facts.get(host):
            device_model = facts[host].get('model', 'n/a')
            device_serial = facts[host].get('serial_number', 'n/a')
            device_ip = facts[host].get('nr_ip', 'n/a')
        host_id_map[host] = host_id
        topology_dict['nodes'].append({
            'id': host_id,
            'name': host,
            'primaryIP': device_ip,
            'model': device_model,
            'serial_number': device_serial,
            'icon': get_icon_type(
                lldp_capabilities_dict.get(host, ''),
                device_model
            )
        })
        host_id += 1
    link_id = 0
    for link in interconnections:
        topology_dict['links'].append({
            'id': link_id,
            'source': host_id_map[link[0][0]],
            'target': host_id_map[link[1][0]],
            'srcIfName': if_shortname(link[0][1]),
            'srcDevice': link[0][0],
            'tgtIfName': if_shortname(link[1][1]),
            'tgtDevice': link[1][0],
        })
        link_id += 1
    return topology_dict

#---#

OUTPUT_TOPOLOGY_FILENAME = 'topology.js'
TOPOLOGY_FILE_HEAD = "\n\nvar topologyData = "

def write_topology_file(topology_json, header=TOPOLOGY_FILE_HEAD, dst=OUTPUT_TOPOLOGY_FILENAME):
    with open(dst, 'w') as topology_file:
        topology_file.write(header)
        topology_file.write(json.dumps(topology_json, indent=4, sort_keys=True))
        topology_file.write(';')
"""
TOPOLOGY_DICT = generate_topology_json(*TOPOLOGY_DETAILS)
write_topology_file(TOPOLOGY_DICT)

#rprint(*TOPOLOGY_DETAILS)
"""

def good_luck_have_fun():
    """Main script logic"""
    #get_host_data_result = nr.run(get_host_data)
    #GLOBAL_LLDP_DATA, GLOBAL_FACTS = normalize_result(get_host_data_result)
    TOPOLOGY_DETAILS = extract_lldp_details(lldp_data)
    TOPOLOGY_DETAILS.append(facts)
    TOPOLOGY_DICT = generate_topology_json(*TOPOLOGY_DETAILS)
    write_topology_file(TOPOLOGY_DICT)
    """
    CACHED_TOPOLOGY = read_cached_topology()
    write_topology_file(TOPOLOGY_DICT)
    write_topology_cache(TOPOLOGY_DICT)
    print('Open main.html in a project root with your browser to view the topology')
    if CACHED_TOPOLOGY:
        DIFF_DATA = get_topology_diff(CACHED_TOPOLOGY, TOPOLOGY_DICT)
        print_diff(DIFF_DATA)
        write_topology_file(DIFF_DATA[2], dst='diff_topology.js')
        if topology_is_changed:
           print('Open diff_page.html in a project root to view the changes.')
            print("Optionally, open main.html and click 'Display diff' button")
    else:
        # write current topology to diff file if the cache is missing
        write_topology_file(TOPOLOGY_DICT, dst='diff_topology.js')
    """
if __name__ == '__main__':
    good_luck_have_fun()