import napalm
import sys
import os
from napalm import get_network_driver

junos_driver = get_network_driver('junos')
#ios_driver = get_network_driver('ios')

#ex4300 = junos_driver('10.100.0.8', 'teset', 'H@ppyrout3')
#devices = [ex4300]

with junos_driver('10.100.0.8', 'test', 'H@ppyrout3') as device:
    #lldp_result = device.get_lldp_neighbors_detail()
    #facts_result = device.get_facts()
    result = device.get_facts() + device.get_bgp_neighbors_detail()
    #print(lldp_result)
    print(result)
    #for port, port_details in lldp_result.items():
        #for i in port_details:
            #print(port, ":" ,i)
            
#for device, output in nornir_job_result.items():
    #if output[0].failed:
        # Write default data to dicts if the task is failed.
        # Use the host inventory object name as a key.
        #global_lldp_data[device] = {}
        #global_facts[device] = {
            #'nr_ip': nr.inventory.hosts[device].get('hostname', 'n/a'),
       # }
        #continue
        # Use FQDN as unique ID for devices withing the script.
   # device_fqdn = output[1].result['facts']['fqdn']
    #if not device_fqdn:
        # If FQDN is not set use hostname.
        # LLDP TLV follows the same logic.
     #       device_fqdn = output[1].result['facts']['hostname']
    #if not device_fqdn:
        # Use host inventory object name as a key if
        # neither FQDN nor hostname are set
     #   device_fqdn = device
  #  global_facts[device_fqdn] = output[1].result['facts']
    # Populate device facts with its IP address or hostname as per Inventory data
   # global_facts[device_fqdn]['nr_ip'] = nr.inventory.hosts[device].get('hostname', 'n/a')
    #global_lldp_data[device_fqdn] = output[1].result['lldp_neighbors_detail']
#return global_lldp_data, global_facts