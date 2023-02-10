
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
                destination_data.write("- device_name: "+'"'+ line[0]+'"'+"\n")
                destination_data.write("    host_ip: " + line[1] + "\n")
                #destination_data.write("    details: " + line[2] + "\n")
        

lldp_dl = {}
with open('lldpfacts.txt', 'r') as lldp_file:
    txt_reader = lldp_file.readlines()
    #print(txt_reader) 
    for line in txt_reader:
        lldp_dl = (eval(line))
#print(lldp_dl)

for k, v in lldp_dl.items():
    for i in v:
        #print(k, ":", i)
        for key, values  in i:
            print(k, ":", values)



        
   







                

