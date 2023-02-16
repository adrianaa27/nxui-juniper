import napalm
import sys
import os
from napalm import get_network_driver

junos_driver = get_network_driver('junos')
#ios_driver = get_network_driver('ios')

#devices = [ex4300, ]
#network_devices = []
    #for device in devices:
        #if device[1] == "ios":
            #network_devices.append(
                            #driver_ios(
                            #hostname = device[0],
                            #username = "admin",
                            #password = "Time4work!"
                            #)
                              #)
        #elif device[1] == "junos":
            #network_devices.append(
                            #driver_junos(
                            #hostname = device[0],
                            #username = "test",
                            #password = "H@ppyrout3"
                            #)
                              #)
#for device in network_devices:
        #device.open()
with junos_driver('10.100.0.8', 'test', 'H@ppyrout3') as device:
    
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

    lldp_result = device.get_lldp_neighbors_detail()
    facts_result = device.get_facts()
    #print(facts_result)
    lldp_data = {}
    facts = {}
    for fact, output in facts_result.items():
        #device_fqdn = facts_result['fqdn']
        #if not device_fqdn:
            device_fqdn = facts_result['hostname']
        #if not device_fqdn:
            #facts[device_fqdn] = facts_result
            facts['ip'] = facts_result['fqdn']
            facts['role'] = facts_result['model']
            #lldp_data[device_fqdn] = output['interface_list']
    #print(facts)   
    for port, port_details in lldp_result.items():
        lldp_data[device_fqdn] = lldp_result
    #print(lldp_data)
        
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
    
    print(extract_lldp_details(lldp_data))


