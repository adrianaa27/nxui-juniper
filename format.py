
import csv 
import yaml
from jinja2 import Environment, FileSystemLoader

with open('getfacts.csv', 'r') as csv_data:
    csv_reader = csv.reader(csv_data)
    #print(csv_reader)
    with open('format.yml','w') as destination_data:
        destination_data.write("---\ndevice:")
        for line in csv_reader:
            #open up the context manager to the file destination.txt
            with open('format.yml','a') as destination_data:
                destination_data.write("- device_name: " + line[0]+ "\n")
                destination_data.write("host_ip: " + line[1] + "\n")
                #destination_data.write("    details: " + line[2] + "\n")
        

lldp_dl = {}
with open('lldpfacts.txt', 'r') as lldp_file:
    txt_reader = lldp_file.readlines()
    #print(txt_reader) 
    for line in txt_reader:
        lldp_dl = (eval(line))
    for port, port_details in lldp_dl.items():
        for i in port_details:
            #print(port, ":", i)  
             with open('format.yml','a') as destination_data:
                destination_data.write("  - port: "+ port +"\n")   
                destination_data.write("        remote_chassis_id: "+ i['remote_chassis_id'] +"\n")
                destination_data.write("        remote_port: "+ i['remote_port'] +"\n") 
                destination_data.write("        remote_port_description: "+ i['remote_port_description'] +"\n")   
                destination_data.write("        remote_system_name: "+ i['remote_system_name'] +"\n")
                destination_data.write("        remote_system_description: "+ i['remote_system_description'] +"\n")   
                destination_data.write("        remote_system_capab: "+ i['remote_system_capab'][0] +"\n")   
                destination_data.write("        remote_system_enable_capab: "+ i['remote_system_enable_capab'][0] +"\n")  
                destination_data.write("        parent_interface: "+ i['parent_interface'] +"\n")   


                


        
   







                

