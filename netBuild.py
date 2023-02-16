import napalm
import sys
import os
from napalm import get_network_driver

junos_driver = get_network_driver('junos')
#ios_driver = get_network_driver('ios')

#ex4300 = junos_driver('10.100.0.8', 'teset', 'H@ppyrout3')
#devices = [ex4300]

with junos_driver('10.100.0.8', 'test', 'H@ppyrout3') as device:
    lldp_result = device.get_lldp_neighbors_detail()
    facts_result = device.get_facts()
    #print(lldp_result)
    print(facts_result)
    #for port, port_details in lldp_result.items():
        #for i in port_details:
            #print(port, ":" ,i)
    lldp_data = {}
    facts = {}

    for device, fact_list in facts_result.items():
        if fact_list[0].failed: 
            facts[device] = {
                'role': ('model', 'undefined'),
                'ip': ('hostname', 'n/a'),
            }
            continue
        device_fqdn = fact_list[6]
        print(device_fqdn)

        


