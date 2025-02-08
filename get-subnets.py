#!/usr/bin/python3.10

import ipaddress
import urllib.request
import os
import shutil

BGP_TOOLS_URL = 'https://bgp.tools/table.txt'
USER_AGENT = 'itdog.info - hi@itdog.info'
AS_FILE = 'AS.lst'
IPv4_DIR = 'Subnets/IPv4'
IPv6_DIR = 'Subnets/IPv6'

AS_META = '32934'
AS_TWITTER = '13414'
META = 'meta.lst'
TWITTER = 'twitter.lst'
TELEGRAM = 'telegram.lst'

# From https://iplist.opencck.org/
DISCORD_VOICE_V4='https://iplist.opencck.org/?format=text&data=cidr4&site=discord.gg&site=discord.media'
DISCORD_VOICE_V6='https://iplist.opencck.org/?format=text&data=cidr6&site=discord.gg&site=discord.media'

DISCORD = 'discord.lst'

TELEGRAM_CIDR_URL = 'https://core.telegram.org/resources/cidr.txt'

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

def download_ready_subnets(url_v4, url_v6):
    ipv4_subnets = []
    ipv6_subnets = []

    urls = [(url_v4, 4), (url_v6, 6)]

    for url, version in urls:
        req = urllib.request.Request(url)
        try:
            with urllib.request.urlopen(req) as response:
                if response.status == 200:
                    subnets = response.read().decode('utf-8').splitlines()
                    for subnet_str in subnets:
                        try:
                            subnet = ipaddress.ip_network(subnet_str)
                            if subnet.version == 4:
                                ipv4_subnets.append(subnet_str)
                            elif subnet.version == 6:
                                ipv6_subnets.append(subnet_str)
                        except ValueError:
                            print(f"Invalid subnet: {subnet_str}")
                            sys.exit(1)
        except Exception as e:
            print(f"Query error: {e}")

    return ipv4_subnets, ipv6_subnets

def download_ready_split_subnets(url):
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        subnets = response.read().decode('utf-8').splitlines()

    ipv4_subnets = [cidr for cidr in subnets if isinstance(ipaddress.ip_network(cidr, strict=False), ipaddress.IPv4Network)]
    ipv6_subnets = [cidr for cidr in subnets if isinstance(ipaddress.ip_network(cidr, strict=False), ipaddress.IPv6Network)]
    
    return ipv4_subnets, ipv6_subnets

def write_subnets_to_file(subnets, filename):
    with open(filename, 'w') as file:
        for subnet in subnets:
            file.write(f'{subnet}\n')

def copy_file_legacy(src_filename):
    base_filename = os.path.basename(src_filename)
    new_filename = base_filename.capitalize()
    shutil.copy(src_filename, os.path.join(os.path.dirname(src_filename), new_filename))

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

    # Discord voice
    ipv4_discord, ipv6_discord = download_ready_subnets(DISCORD_VOICE_V4, DISCORD_VOICE_V6)
    write_subnets_to_file(ipv4_discord, f'{IPv4_DIR}/{DISCORD}')
    write_subnets_to_file(ipv6_discord, f'{IPv6_DIR}/{DISCORD}')

    # Telegram
    ipv4_telegram, ipv6_telegram = download_ready_split_subnets(TELEGRAM_CIDR_URL)
    write_subnets_to_file(ipv4_telegram, f'{IPv4_DIR}/{TELEGRAM}')
    write_subnets_to_file(ipv6_telegram, f'{IPv6_DIR}/{TELEGRAM}')

    # Legacy name
    copy_file_legacy(f'{IPv4_DIR}/{META}')
    copy_file_legacy(f'{IPv6_DIR}/{META}')
    copy_file_legacy(f'{IPv4_DIR}/{TWITTER}')
    copy_file_legacy(f'{IPv6_DIR}/{TWITTER}')
    copy_file_legacy(f'{IPv4_DIR}/{DISCORD}')
    copy_file_legacy(f'{IPv6_DIR}/{DISCORD}')