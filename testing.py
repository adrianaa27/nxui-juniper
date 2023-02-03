from napalm import get_network_driver
from rich import print as rprint
import json 
import csv
import yaml
from jinja2 import Environment, FileSystemLoader

with open('getfacts.csv','w') as getfacts_data:
   
    for facts in getfacts_data:
        getfacts_data.write(ansible_facts{napalm_facts{napalm_fqdn[0]})
