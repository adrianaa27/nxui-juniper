import napalm
import sys
import os
from napalm import get_network_driver

junos_driver = get_network_driver('junos')
ios_driver = get_network_driver('ios')

#ex4300 = junos_driver('10.100.0.8', 'teset', 'H@ppyrout3')
#devices = [ex4300]

with junos_driver('10.100.0.8', 'test', 'H@ppyrout3') as device:
    print(device.get_facts())
    print(device.get_lldp_neighbors_detail())

lldp_data = {}
device_facts = {}

#for dev, output in device.get_facts().items:
