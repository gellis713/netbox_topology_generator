#!/usr/bin/env python3

import sys
import os
import subprocess
import requests
import pygraphviz as pgv

read_only_api_key='REPLACE_ME_WITH_NETBOX_API_KEY'
netboxURL = "https://REPLACE_ME_WITH_NETBOX_URL"
topologyPath = "./topology.dot"

def getNetboxJSON(uri):
	result = requests.get(netboxURL + uri, headers={'Authorization': 'Token %s' % (read_only_api_key)},verify=False)
	if result.status_code == 200:
		return result.json()
	elif result.status_code == 403:
		print("API Request - 403 forbidden, please check your API key (read_only_api_key)")
		sys.exit(1)

def getPlatform(device):
	result = getNetboxJSON("/api/dcim/devices/%s" % (device['id']))
	if result['platform'] == None:
		return "None"
	else:
		return result['platform']['slug']

def isPhysicalInterface(interface):
	#We don't want subinterfaces popping up in our physical list
	if interface['name'].startswith(('swp','Ethernet','enp')) and "." not in interface['name']:
		return True

	return False

def main():
	#Retrieve JSON data for devices
	cumulusSwitches = getNetboxJSON("/api/dcim/devices/?platform=cumulus-linux&limit=0")['results']

	#Setup base Graphviz object
	topology = pgv.AGraph()

	#Add all Cumulus devices we want to simulate to the topology and pull their interfaces
	for switch in cumulusSwitches:
		switch['interfaces'] = getNetboxJSON("/api/dcim/interfaces/?device_id=%s&limit=0" % (switch['id']))['results']
		topology.add_node(switch['name'],function="spine",os="CumulusCommunity/cumulus-vx",version="4.0.0",memory="512")

	#Create inter-switch links
	for switch in cumulusSwitches:
		blackholeInterfaceCounter = 0
		for interface in switch['interfaces']:
			if isPhysicalInterface(interface) == False:
				continue
			if interface['connected_endpoint'] is None:
				continue
			if getPlatform(interface['connected_endpoint']['device']) == "cumulus-linux":
				topology.add_edge("%s:%s" % (switch['name'],interface['name']),"%s:%s" % (interface['connected_endpoint']['device']['name'],interface['connected_endpoint']['name']))
			else:
				topology.add_node("%s-blackhole" % (switch['name']),function="fake")
				topology.add_edge("%s:%s" % (switch['name'],interface['name']),"%s-blackhole:swp%s" % (switch['name'],blackholeInterfaceCounter))
				blackholeInterfaceCounter += 1

	#Write topology DOT file
	topology.write(topologyPath)

if __name__ == "__main__":
	main()
