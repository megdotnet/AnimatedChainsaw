# parse firewall config and pull the ip addresses of vpn tunnels

from dotenv import load_dotenv
from pathlib import Path
import os 
import ipaddress

# load .env variables
load_dotenv()

def classy(ip_address):
    # get class A, B, & C network addresses for the ip_address
    a = str(ipaddress.ip_network(f"{ip_address}/255.0.0.0", strict=False).network_address)
    b = str(ipaddress.ip_network(f"{ip_address}/255.255.0.0", strict=False).network_address)
    c = str(ipaddress.ip_network(f"{ip_address}/255.255.255.0", strict=False).network_address)    
    return (a,b,c)

# initialize empty list variables
vpn_addresses = []
vpn_class_a = []
vpn_class_b = []
vpn_class_c = []

# path variables
output_fo = Path(os.path.dirname(os.path.realpath(__file__)))
output_fn = Path("output.txt")
output_fp = output_fo / output_fn

config_fo = Path(os.environ.get('config_fo'))

# get the path to the newest config file in the folder
directory_listing = sorted(Path(config_fo).glob('*.cfg'), key=os.path.getmtime, reverse=True)
config_fp = directory_listing[0]

# find vpn tunnel ip addresses in the config file
with open(config_fp,"r") as file:
   for line in file: 
       if "ipsec-l2l" in line:
           ip_address = line.split(" ")[1]
           a,b,c = classy(ip_address)
           
           if ip_address not in vpn_addresses: 
               vpn_addresses.append(ip_address)
           if a not in vpn_class_a: 
               vpn_class_a.append(a)
           if b not in vpn_class_a: 
               vpn_class_b.append(b)
           if a not in vpn_class_a: 
               vpn_class_b.append(b)



# save ip addresses to text file
# with open(output_fp, 'w') as output:
#     for item in vpn_addresses:
#         output.write("{}\n".format(item))