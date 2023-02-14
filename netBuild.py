import napalm
import sys
import os
from napalm import get_network_driver

junos_driver = get_network_driver('junos')
#ios_driver = get_network_driver('ios')

#ex4300 = junos_driver('10.100.0.8', 'teset', 'H@ppyrout3')
#devices = [ex4300]

with junos_driver('10.100.0.8', 'test', 'H@ppyrout3') as device:
    lldp_result = [device.get_lldp_neighbors_detail()]
    facts_result = [device.get_facts()]
    #print(result)
    lldp_data = {}
    facts = {}
    for items in lldp_result:
        lldp_data = items
        print(lldp_data)
    for interface, int_details in lldp_data.items():
            for i in int_details:
                print(i + ":" + int_details)