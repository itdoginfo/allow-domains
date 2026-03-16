#!/usr/bin/env python3

import ipaddress
import urllib.request
import os
import shutil
import json
import sys

RIPE_STAT_URL = 'https://stat.ripe.net/data/announced-prefixes/data.json?resource=AS{}'
USER_AGENT = 'allow-domains/1.0'
IPv4_DIR = 'Subnets/IPv4'
IPv6_DIR = 'Subnets/IPv6'

ASN_SERVICES = {
    'meta.lst': ['32934', '63293', '54115', '149642'],
    'twitter.lst': ['13414'],
    'hetzner.lst': ['24940'],
    'ovh.lst': ['16276'],
    'digitalocean.lst': ['14061'],
}

ASN_TELEGRAM = ['44907', '59930', '62014', '62041', '211157']
TELEGRAM = 'telegram.lst'
CLOUDFLARE = 'cloudflare.lst'
CLOUDFRONT = 'cloudfront.lst'

# From https://iplist.opencck.org/
DISCORD_VOICE_V4='https://iplist.opencck.org/?format=text&data=cidr4&site=discord.gg&site=discord.media'
DISCORD_VOICE_V6='https://iplist.opencck.org/?format=text&data=cidr6&site=discord.gg&site=discord.media'

DISCORD = 'discord.lst'

TELEGRAM_CIDR_URL = 'https://core.telegram.org/resources/cidr.txt'

CLOUDFLARE_V4='https://www.cloudflare.com/ips-v4'
CLOUDFLARE_V6='https://www.cloudflare.com/ips-v6'

# https://support.google.com/a/answer/1279090
GOOGLE_MEET = 'google_meet.lst'
GOOGLE_MEET_V4 = [
    '74.125.247.128/32',
    '74.125.250.0/24',
    '142.250.82.0/24',
]
GOOGLE_MEET_V6 = [
    '2001:4860:4864:4:8000::/128',
    '2001:4860:4864:5::/64',
    '2001:4860:4864:6::/64',
]

AWS_CIDR_URL='https://ip-ranges.amazonaws.com/ip-ranges.json'

def make_request(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent', USER_AGENT)
    return req

def subnet_summarization(subnet_list):
    subnets = [ipaddress.ip_network(subnet, strict=False) for subnet in subnet_list]
    return list(ipaddress.collapse_addresses(subnets))

def fetch_asn_prefixes(asn_list):
    ipv4_subnets = []
    ipv6_subnets = []

    for asn in asn_list:
        url = RIPE_STAT_URL.format(asn)
        req = make_request(url)
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                data = json.loads(response.read().decode('utf-8'))
                for entry in data['data']['prefixes']:
                    prefix = entry['prefix']
                    try:
                        network = ipaddress.ip_network(prefix)
                        if network.version == 4:
                            ipv4_subnets.append(prefix)
                        else:
                            ipv6_subnets.append(prefix)
                    except ValueError:
                        print(f"Invalid subnet: {prefix}")
                        sys.exit(1)
        except Exception as e:
            print(f"Error fetching AS{asn}: {e}")
            sys.exit(1)

    return ipv4_subnets, ipv6_subnets

def download_subnets(*urls):
    ipv4_subnets = []
    ipv6_subnets = []

    for url in urls:
        req = make_request(url)
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                subnets = response.read().decode('utf-8').splitlines()
                for subnet_str in subnets:
                    try:
                        network = ipaddress.ip_network(subnet_str, strict=False)
                        if network.version == 4:
                            ipv4_subnets.append(subnet_str)
                        else:
                            ipv6_subnets.append(subnet_str)
                    except ValueError:
                        print(f"Invalid subnet: {subnet_str}")
                        sys.exit(1)
        except Exception as e:
            print(f"Query error {url}: {e}")
            sys.exit(1)

    return ipv4_subnets, ipv6_subnets

def download_aws_cloudfront_subnets():
    ipv4_subnets = []
    ipv6_subnets = []
    
    req = make_request(AWS_CIDR_URL)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))

            for prefix in data.get('prefixes', []):
                if prefix.get('service') == 'CLOUDFRONT':
                    ipv4_subnets.append(prefix['ip_prefix'])

            for prefix in data.get('ipv6_prefixes', []):
                if prefix.get('service') == 'CLOUDFRONT':
                    ipv6_subnets.append(prefix['ipv6_prefix'])

    except Exception as e:
        print(f"Error downloading AWS CloudFront ranges: {e}")
        sys.exit(1)

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
    # Services from ASN (meta, twitter, hetzner, ovh, digitalocean)
    for filename, asn_list in ASN_SERVICES.items():
        print(f'Fetching {filename}...')
        ipv4, ipv6 = fetch_asn_prefixes(asn_list)
        write_subnets_to_file(subnet_summarization(ipv4), f'{IPv4_DIR}/{filename}')
        write_subnets_to_file(subnet_summarization(ipv6), f'{IPv6_DIR}/{filename}')

    # Discord voice
    print(f'Fetching {DISCORD}...')
    ipv4_discord, ipv6_discord = download_subnets(DISCORD_VOICE_V4, DISCORD_VOICE_V6)
    write_subnets_to_file(ipv4_discord, f'{IPv4_DIR}/{DISCORD}')
    write_subnets_to_file(ipv6_discord, f'{IPv6_DIR}/{DISCORD}')

    # Telegram
    print(f'Fetching {TELEGRAM}...')
    ipv4_telegram_file, ipv6_telegram_file = download_subnets(TELEGRAM_CIDR_URL)
    ipv4_telegram_asn, ipv6_telegram_asn = fetch_asn_prefixes(ASN_TELEGRAM)
    ipv4_telegram = subnet_summarization(ipv4_telegram_file + ipv4_telegram_asn)
    ipv6_telegram = subnet_summarization(ipv6_telegram_file + ipv6_telegram_asn)
    write_subnets_to_file(ipv4_telegram, f'{IPv4_DIR}/{TELEGRAM}')
    write_subnets_to_file(ipv6_telegram, f'{IPv6_DIR}/{TELEGRAM}')

    # Cloudflare
    print(f'Fetching {CLOUDFLARE}...')
    ipv4_cloudflare, ipv6_cloudflare = download_subnets(CLOUDFLARE_V4, CLOUDFLARE_V6)
    write_subnets_to_file(ipv4_cloudflare, f'{IPv4_DIR}/{CLOUDFLARE}')
    write_subnets_to_file(ipv6_cloudflare, f'{IPv6_DIR}/{CLOUDFLARE}')

    # Google Meet
    print(f'Writing {GOOGLE_MEET}...')
    write_subnets_to_file(GOOGLE_MEET_V4, f'{IPv4_DIR}/{GOOGLE_MEET}')
    write_subnets_to_file(GOOGLE_MEET_V6, f'{IPv6_DIR}/{GOOGLE_MEET}')

    # AWS CloudFront
    print(f'Fetching {CLOUDFRONT}...')
    ipv4_cloudfront, ipv6_cloudfront = download_aws_cloudfront_subnets()
    write_subnets_to_file(ipv4_cloudfront, f'{IPv4_DIR}/{CLOUDFRONT}')
    write_subnets_to_file(ipv6_cloudfront, f'{IPv6_DIR}/{CLOUDFRONT}')

    # Legacy copies with capitalized names (e.g. meta.lst -> Meta.lst)
    LEGACY_FILES = ['meta.lst', 'twitter.lst', 'discord.lst']
    for legacy_file in LEGACY_FILES:
        copy_file_legacy(f'{IPv4_DIR}/{legacy_file}')
        copy_file_legacy(f'{IPv6_DIR}/{legacy_file}')