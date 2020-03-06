# netbox_topology_generator
Generate Graphviz files from Netbox data to create virtual labs of your production network

This is currently used in a Cumulus VX lab to run unit tests in our CI pipeline.

Requirements for data modeling:
 - Any connections you want simulated need to be mapped in Netbox. (https://netbox.readthedocs.io/en/stable/core-functionality/devices/#cables)
 - You need to define what types of devices you want to simulate. This can either be by device role, platform, etc. (See the cumulusSwitches variable definition if you want to edit what devices are pulled from Netbox)
 - If you have physical interfaces not currently defined in this script you'll need to add them. Subinterfaces,port-channels,VLANs, etc. are NOT physical interfaces, they are logical constructs.
 
Setup:
 - pip3 install -r requirements.txt
 - Add your Netbox API (preferably read only) key to the variable in the top of the script
 - Add your Netbox URL e.g. "https://netbox.company.com/"
 - Edit the "topologyPath" variable if you want the topology file to go somewhere besides the PWD.
 
Usage:
python3 netbox_topology_generator.py

When you've generated your desired topology you can use https://gitlab.com/cumulus-consulting/tools/topology_converter to generate a Vagrantfile for simulation if desired or you can just use the topology file for PTM on Cumulus devices
