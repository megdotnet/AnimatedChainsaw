# parse firewall config and pull the ip addresses of vpn tunnels

from dotenv import load_dotenv
from pathlib import Path
import os 

# load .env variables
load_dotenv()

# initiate empty list
vpn_addresses = []

# path variables
output_fp = Path("./output.txt")
config_fo = Path(os.environ.get('config_fo'))

# get the path to the newest config file in the folder
directory_listing = sorted(Path(config_fo).glob('*.cfg'), key=os.path.getmtime, reverse=True)
config_fp = directory_listing[0]

# find vpn tunnel ip addresses in the config file
with open(config_fp,"r") as file:
   for line in file: 
       if "ipsec-l2l" in line:
           ip_address = line.split(" ")[1]
           vpn_addresses.append(ip_address) # <---  NEED TO CHECK FOR DUPLICATES (probably)

# save ip addresses to text file
with open(output_fp, 'w') as output:
    for item in vpn_addresses:
        output.write("{}\n".format(item))