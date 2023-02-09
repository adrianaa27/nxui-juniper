
import csv
import yaml
from jinja2 import Environment, FileSystemLoader

with open('getfacts.csv', 'r') as csv_data:
    csv_reader = csv.reader(csv_data)
    #print(csv_reader)
    with open('format.yml','w') as destination_data:
        destination_data.write("---\ndevice:" + "\n")
    for line in csv_reader:
        
        #open up the context manager to the file destination.txt
    
        with open('format.yml','a') as destination_data:
            #destination_data.write("device:" + "\n    ")
            destination_data.write("  - device_name: "+'"'+ line[0]+'"'+"\n    ")
            destination_data.write("host_ip: " + line[1] + "\n")
            destination_data.write("details: " + line[2] + "\n")

