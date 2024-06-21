#!/usr/bin/python3.10

import ipaddress
import urllib.request

BGP_TOOLS_URL = 'https://bgp.tools/table.txt'
USER_AGENT = 'itdog.info - hi@itdog.info'
AS_FILE = 'AS.lst'
IPv4_DIR = 'Subnets/IPv4'
IPv6_DIR = 'Subnets/IPv6'

AS_META = '32934'
AS_TWITTER = '13414'
META = 'Meta.lst'
TWITTER = 'Twitter.lst'

subnet_list = []

def subnet_summarization(subnet_list):
    subnets = [ipaddress.ip_network(subnet) for subnet in subnet_list]
    return list(ipaddress.collapse_addresses(subnets))

def process_subnets(subnet_list, target_as):
    ipv4_subnets = []
    ipv6_subnets = []

    for subnet_str, as_number in subnet_list:
        try:
            subnet = ipaddress.ip_network(subnet_str)
            if as_number == target_as:
                if subnet.version == 4:
                    ipv4_subnets.append(subnet_str)
                elif subnet.version == 6:
                    ipv6_subnets.append(subnet_str)
        except ValueError:
            print(f"Invalid subnet: {subnet_str}")
            sys.exit(1)

    ipv4_merged = subnet_summarization(ipv4_subnets)
    ipv6_merged = subnet_summarization(ipv6_subnets)

    return ipv4_merged, ipv6_merged

def write_subnets_to_file(subnets, filename):
    with open(filename, 'w') as file:
        for subnet in subnets:
            file.write(f'{subnet}\n')

if __name__ == '__main__':
    request = urllib.request.Request(BGP_TOOLS_URL, headers={'User-Agent': USER_AGENT})
    
    with urllib.request.urlopen(request) as response:
        for line in response:
            decoded_line = line.decode('utf-8').strip()
            subnet, as_number = decoded_line.split()
            subnet_list.append((subnet, as_number))

    # Meta
    ipv4_merged_meta, ipv6_merged_meta = process_subnets(subnet_list, AS_META)
    write_subnets_to_file(ipv4_merged_meta, f'{IPv4_DIR}/{META}')
    write_subnets_to_file(ipv6_merged_meta, f'{IPv6_DIR}/{META}')

    # Twitter
    ipv4_merged_twitter, ipv6_merged_twitter = process_subnets(subnet_list, AS_TWITTER)
    write_subnets_to_file(ipv4_merged_twitter, f'{IPv4_DIR}/{TWITTER}')
    write_subnets_to_file(ipv6_merged_twitter, f'{IPv6_DIR}/{TWITTER}')