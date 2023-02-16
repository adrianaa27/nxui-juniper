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
    print(facts)   
    for port, port_details in lldp_result.items():
        lldp_data[device_fqdn] = lldp_result
    print(lldp_data)