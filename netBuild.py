from napalm import get_network_driver
from napalm import 


ios_driver = get_network_driver('junos')
junos_driver = get_network_driver('ios')

ex4300 = junos_driver('10.100.0.8', 'teset', 'H@ppyrout3')

devices = [ex4300]

for device in devices:
    device.open()
    output = device.get_facts(), device.get_lldp_neighbors_detail()
    print(output)