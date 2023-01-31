from napalm import get_network_driver
from rich import print as rprint
import json 

#---
# #
junos_driver = get_network_driver("junos")
ex4300 = junos_driver('10.100.0.8', 'test', 'H@ppyrout3')
ex2200 = junos_driver('10.196.29.170', 'root', 'H@ppyrout3')

devices = [ex4300, ex2200]

for device in devices:
    device.open()
    output = device.get_lldp_neighbors_detail()
    print(json.dumps(output, sort_keys=True, indent=4))

#---#

