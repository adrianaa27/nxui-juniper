from napalm import get_network_driver
from rich import print as rprint
import json 
import csv
import yaml
from jinja2 import Environment, FileSystemLoader

with open('getfacts.csv','r+') as getfacts_data:
    reader = csv.reader(getfacts_data)
    for row in reader:
        print(row)
        #getfacts_data.write(row[0])


