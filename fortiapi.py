#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pyfortiapi
import sys
import json

def main():
    
    server_ip = sys.argv[1]
    with open(sys.argv[2]) as f:
        first_line = f.readline()
    user   = first_line.split(" ")[0]
    passwd = first_line.split(" ")[1].rstrip('\r\n')
    policy_name = sys.argv[3] 
    group_name  = sys.argv[4]
    host_name = sys.argv[5]
    host_ip   = sys.argv[6]
    src_intf = sys.argv[7]
    dst_intf = sys.argv[8]

	# login to server:
    device = pyfortiapi.FortiGate(ipaddr = server_ip, username = user, password = passwd)

	# create host
    addresses = device.get_firewall_address()
    addresses = str(addresses).replace("\'", "\"")

    if host_name in addresses:
        print("Address available")
        update_payload = "{'type': 'subnet', 'subnet': '" + host_ip + " 255.255.255.255'}"
        device.update_firewall_address(host_name, update_payload)
    else:
        create_payload = "{'name': '" + host_name+"', 'type': 'subnet', 'subnet': '" + host_ip + " 255.255.255.255'}"
        device.create_firewall_address(host_name, create_payload)

    # create group
    groups = device.get_address_group()
    groups = str(groups).replace("\'", "\"")
    groups = json.loads(groups)

    if(len(groups) == 0):
        create_payload = "{'name': '" + group_name + "', 'member': [{'name': '" + host_name +"'}]}"
        device.create_address_group(group_name, create_payload)
    else:
        for g in range(len(groups)):
            if(groups[g]["name"] == group_name):
                print("Group available")
                group_members = groups[g]["member"]
                group_members = str(group_members).replace("[", "")
                group_members = str(group_members).replace("]", "")

                update_payload = "{'member': [" + group_members  + ", {'q_origin_key': '" + host_name  + "', 'name': '" + host_name + "'}]}"
                device.update_address_group(group_name, update_payload)
            else:
                create_payload = "{'name': '" + group_name + "', 'member': [{'name': '" + host_name +"'}]}"
                device.create_address_group(group_name, create_payload)

    # add policy
    policies = device.get_firewall_policy() 
    policies = str(policies).replace("\'", "\"")
    policies = json.loads(policies)
    
    if(len(policies) == 0):
        create_payload = "{'name': '" + policy_name + "', 'srcintf': [{'name': '" + src_intf + "'}], 'dstintf': [{'name': '" + dst_intf + "'}], 'srcaddr': [{'name': '" + group_name + "'}], 'dstaddr': [{'name': 'all'}], 'action': 'deny', 'status': 'disable', 'schedule': 'always', 'service': [{'name': 'ALL'}]}"
        device.create_firewall_policy(policy_name, create_payload)
    else:
        for p in range(len(policies)):
            if(policies[p]["name"] == policy_name):
                print("Policy available")
                policy_id = policies[p]["policyid"]
                policy_srcaddr = policies[p]["srcaddr"]
                policy_srcaddr = str(policy_srcaddr).replace("[", "")
                policy_srcaddr = str(policy_srcaddr).replace("]", "")

                update_payload = "{'srcaddr': [" + policy_srcaddr  + ", {'q_origin_key': '" + group_name  + "', 'name': '" + group_name + "'}]}"
                device.update_firewall_policy(policy_id, update_payload)
            else:
                create_payload = "{'name': '" + policy_name + "', 'srcintf': [{'name': '" + src_intf + "'}], 'dstintf': [{'name': '" + dst_intf + "'}], 'srcaddr': [{'name': '" + group_name + "'}], 'dstaddr': [{'name': 'all'}], 'action': 'deny', 'status': 'disable', 'schedule': 'always', 'service': [{'name': 'ALL'}]}"
                device.create_firewall_policy(policy_name, create_payload)

if __name__ == "__main__":
    main()
    
