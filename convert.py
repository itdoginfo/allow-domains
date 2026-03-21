#!/usr/bin/env python3

import tldextract
import urllib.request
import re
from pathlib import Path
import json
import os
import shutil
import subprocess
import sys

rusDomainsInsideOut='Russia/inside'
rusDomainsInsideSrcSingle='src/Russia-domains-inside-single.lst'
rusDomainsInsideCategories='Categories'
rusDomainsInsideServices='Services'
rusDomainsOutsideSrc='src/Russia-domains-outside.lst'
rusDomainsOutsideOut='Russia/outside'
uaDomainsSrc='src/Ukraine-domains-inside.lst'
uaDomainsOut='Ukraine/inside'
SUBNET_SERVICES = [
    'discord', 'meta', 'twitter', 'telegram',
    'cloudflare', 'hetzner', 'ovh', 'digitalocean',
    'cloudfront', 'roblox', 'google_meet',
]
ExcludeServices = {"telegram.lst", "cloudflare.lst", "google_ai.lst", "google_play.lst", 'hetzner.lst', 'ovh.lst', 'digitalocean.lst', 'cloudfront.lst', 'hodca.lst', 'roblox.lst', 'google_meet.lst'}

def collect_files(src):
    files = []
    for dir_path in src:
        path = Path(dir_path)
        if path.is_dir():
            files.extend(f for f in path.glob('*') if f.name not in ExcludeServices)
        elif path.is_file() and path.name not in ExcludeServices:
            files.append(path)
    return files

def collect_domains(src, dot_prefix=True):
    domains = set()
    for f in collect_files(src):
        if not f.is_file():
            continue
        with open(f) as infile:
            for line in infile:
                ext = tldextract.extract(line.rstrip())
                if not ext.suffix:
                    continue
                if re.search(r'[^а-я\-]', ext.domain):
                    domains.add(ext.fqdn)
                elif not ext.domain:
                    prefix = '.' if dot_prefix else ''
                    domains.add(prefix + ext.suffix)
    return domains

def raw(src, out):
    domains = sorted(collect_domains(src))

    with open(f'{out}-raw.lst', 'w') as file:
        for name in domains:
            file.write(f'{name}\n')

def dnsmasq(src, out, remove={'google.com'}):
    domains = sorted(collect_domains(src) - remove)

    with open(f'{out}-dnsmasq-nfset.lst', 'w') as file:
        for name in domains:
            file.write(f'nftset=/{name}/4#inet#fw4#vpn_domains\n')

    with open(f'{out}-dnsmasq-ipset.lst', 'w') as file:
        for name in domains:
            file.write(f'ipset=/{name}/vpn_domains\n')

def clashx(src, out, remove={'google.com'}):
    domains = sorted(collect_domains(src) - remove)

    with open(f'{out}-clashx.lst', 'w') as file:
        for name in domains:
            file.write(f'DOMAIN-SUFFIX,{name}\n')

def kvas(src, out, remove={'google.com'}):
    domains = sorted(collect_domains(src, dot_prefix=False) - remove)

    with open(f'{out}-kvas.lst', 'w') as file:
        for name in domains:
            file.write(f'{name}\n')

def mikrotik_fwd(src, out, remove={'google.com'}):
    domains = sorted(collect_domains(src) - remove)

    with open(f'{out}-mikrotik-fwd.lst', 'w') as file:
        for name in domains:
            if name.startswith('.'):
                file.write(f'/ip dns static add name=*.{name[1:]} type=FWD address-list=allow-domains forward-to=localhost\n')
            else:
                file.write(f'/ip dns static add name={name} type=FWD address-list=allow-domains match-subdomain=yes forward-to=localhost\n')

def lines_from_file(filepath):
    if not os.path.exists(filepath):
        print(f"Warning: input file not found: {filepath}", file=sys.stderr)
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def compile_mrs(domains, name, mrs_dir='MRS', behavior='domain'):
    os.makedirs(mrs_dir, exist_ok=True)

    txt_path = os.path.join(mrs_dir, f"{name}.txt")
    mrs_path = os.path.join(mrs_dir, f"{name}.mrs")

    with open(txt_path, 'w', encoding='utf-8') as f:
        for d in domains:
            f.write(f"{d}\n")

    try:
        subprocess.run(
            ["mihomo", "convert-ruleset", behavior, "text", txt_path, mrs_path], check=True
        )
        print(f"Compiled: {mrs_path}")
    except subprocess.CalledProcessError as e:
        print(f"Compile error {txt_path}: {e}")
        sys.exit(1)

def compile_srs(data, name, json_dir='JSON', srs_dir='SRS'):
    os.makedirs(json_dir, exist_ok=True)
    os.makedirs(srs_dir, exist_ok=True)

    json_path = os.path.join(json_dir, f"{name}.json")
    srs_path = os.path.join(srs_dir, f"{name}.srs")

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

    try:
        subprocess.run(
            ["sing-box", "rule-set", "compile", json_path, "-o", srs_path], check=True
        )
        print(f"Compiled: {srs_path}")
    except subprocess.CalledProcessError as e:
        print(f"Compile error {json_path}: {e}")
        sys.exit(1)

def srs_rule(name, rules):
    compile_srs({"version": 3, "rules": rules}, name)

def generate_srs_for_categories(directories):
    exclude = {"meta", "twitter", "discord", "telegram", "hetzner", "ovh", "digitalocean", "cloudfront", "roblox", "google_meet"}

    for directory in directories:
        for filename in os.listdir(directory):
            if any(keyword in filename for keyword in exclude):
                continue
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                domains = lines_from_file(file_path)
                name = os.path.splitext(filename)[0]
                srs_rule(name, [{"domain_suffix": domains}])


def prepare_dat_domains(domains, output_name, dirs=None):
    output_lists_directory = 'geosite_data'
    os.makedirs(output_lists_directory, exist_ok=True)

    domain_attrs = {domain: [] for domain in domains}

    for directory in (dirs or []):
        if not os.path.isdir(directory):
            continue
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if not os.path.isfile(file_path):
                continue

            attribute = os.path.splitext(filename)[0].replace('_', '-')

            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    domain = line.strip()
                    if not domain:
                        continue
                    if domain in domain_attrs:
                        domain_attrs[domain].append(f" @{attribute}")

    output_file_path = os.path.join(output_lists_directory, output_name)
    with open(output_file_path, 'w', encoding='utf-8') as out_f:
        for domain, attrs in domain_attrs.items():
            line = domain + "".join(attrs)
            out_f.write(f"{line}\n")

def prepare_dat_combined(dirs):
    output_lists_directory = 'geosite_data'
    os.makedirs(output_lists_directory, exist_ok=True)

    for directory in dirs:
        if not os.path.isdir(directory):
            continue

        for filename in os.listdir(directory):
            source_path = os.path.join(directory, filename)
            if not os.path.isfile(source_path):
                continue

            new_name = os.path.splitext(filename)[0].replace('_', '-')
            destination_path = os.path.join(output_lists_directory, new_name)

            shutil.copyfile(source_path, destination_path)
 
def parse_geosite_line(line):
    from proto import geosite_pb2

    parts = line.split()
    raw_domain = parts[0]
    attrs = [p.lstrip('@') for p in parts[1:] if p.startswith('@')]

    if raw_domain.startswith('full:'):
        domain_type = geosite_pb2.Domain.Full
        value = raw_domain[5:]
    elif raw_domain.startswith('regexp:'):
        domain_type = geosite_pb2.Domain.Regex
        value = raw_domain[7:]
    elif raw_domain.startswith('keyword:'):
        domain_type = geosite_pb2.Domain.Plain
        value = raw_domain[8:]
    else:
        domain_type = geosite_pb2.Domain.RootDomain
        value = raw_domain.lstrip('.')

    return domain_type, value, attrs

def generate_dat_domains(data_path='geosite_data', output_name='geosite.dat', output_directory='DAT'):
    from proto import geosite_pb2

    os.makedirs(output_directory, exist_ok=True)

    geo_site_list = geosite_pb2.GeoSiteList()

    for filename in sorted(os.listdir(data_path)):
        file_path = os.path.join(data_path, filename)
        if not os.path.isfile(file_path):
            continue

        geo_site = geo_site_list.entry.add()
        geo_site.country_code = filename.upper()

        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                domain_type, value, attrs = parse_geosite_line(line)

                domain = geo_site.domain.add()
                domain.type = domain_type
                domain.value = value

                for attr in attrs:
                    attribute = domain.attribute.add()
                    attribute.key = attr
                    attribute.bool_value = True

    output_path = os.path.join(output_directory, output_name)
    with open(output_path, 'wb') as f:
        f.write(geo_site_list.SerializeToString())

    print(f"Compiled .dat file: {output_path}")

if __name__ == '__main__':
    # Russia inside
    Path("Russia").mkdir(parents=True, exist_ok=True)

    removeDomains = {'google.com', 'googletagmanager.com', 'github.com', 'githubusercontent.com', 'githubcopilot.com', 'microsoft.com', 'cloudflare-dns.com', 'parsec.app' }
    removeDomainsMikrotik = {'google.com', 'googletagmanager.com', 'github.com', 'githubusercontent.com', 'githubcopilot.com', 'microsoft.com', 'cloudflare-dns.com', 'parsec.app', 'showip.net' }
    removeDomainsKvas = {'google.com', 'googletagmanager.com', 'github.com', 'githubusercontent.com', 'githubcopilot.com', 'microsoft.com', 'cloudflare-dns.com', 'parsec.app', 't.co', 'ua' }
    
    inside_lists = [rusDomainsInsideCategories, rusDomainsInsideServices]

    raw(inside_lists, rusDomainsInsideOut)
    dnsmasq(inside_lists, rusDomainsInsideOut, removeDomains)
    clashx(inside_lists, rusDomainsInsideOut, removeDomains)
    kvas(inside_lists, rusDomainsInsideOut, removeDomainsKvas)
    mikrotik_fwd(inside_lists, rusDomainsInsideOut, removeDomainsMikrotik)

    # Russia outside
    outside_lists = [rusDomainsOutsideSrc]

    raw(outside_lists, rusDomainsOutsideOut)
    dnsmasq(outside_lists, rusDomainsOutsideOut)
    clashx(outside_lists, rusDomainsOutsideOut)
    kvas(outside_lists, rusDomainsOutsideOut)
    mikrotik_fwd(outside_lists, rusDomainsOutsideOut)

    # Ukraine
    Path("Ukraine").mkdir(parents=True, exist_ok=True)

    urllib.request.urlretrieve("https://uablacklist.net/domains.txt", "uablacklist-domains.lst")
    urllib.request.urlretrieve("https://raw.githubusercontent.com/zhovner/zaborona_help/master/config/domainsdb.txt", "zaboronahelp-domains.lst")

    ua_lists = ['uablacklist-domains.lst', 'zaboronahelp-domains.lst', uaDomainsSrc]
    
    raw(ua_lists, uaDomainsOut)
    dnsmasq(ua_lists, uaDomainsOut)
    clashx(ua_lists, uaDomainsOut)
    kvas(ua_lists, uaDomainsOut)
    mikrotik_fwd(ua_lists, uaDomainsOut)

    for temp_file in ['uablacklist-domains.lst', 'zaboronahelp-domains.lst']:
        Path(temp_file).unlink()

    # Sing-box ruleset main
    russia_inside = lines_from_file('Russia/inside-raw.lst')
    russia_outside = lines_from_file('Russia/outside-raw.lst')
    ukraine_inside = lines_from_file('Ukraine/inside-raw.lst')
    srs_rule('russia_inside', [{"domain_suffix": russia_inside}])
    srs_rule('russia_outside', [{"domain_suffix": russia_outside}])
    srs_rule('ukraine_inside', [{"domain_suffix": ukraine_inside}])

    # Sing-box categories
    directories = ['Categories', 'Services']
    generate_srs_for_categories(directories)

    # Sing-box subnets + domains
    for service in SUBNET_SERVICES:
        if service == 'discord':
            continue
        subnets = lines_from_file(f'Subnets/IPv4/{service}.lst')
        domains = lines_from_file(f'Services/{service}.lst')
        srs_rule(service, [{"domain_suffix": domains, "ip_cidr": subnets}])

    # Discord (domains + UDP subnets on high ports)
    discord_subnets = lines_from_file('Subnets/IPv4/discord.lst')
    discord_domains = lines_from_file('Services/discord.lst')
    srs_rule('discord', [
        {"domain_suffix": discord_domains},
        {"network": ["udp"], "ip_cidr": discord_subnets, "port_range": ["50000:65535"]},
    ])

    # Mihomo main
    to_mrs = lambda domains: [f'+.{d.lstrip(".")}' for d in domains]
    mrs_russia_inside = to_mrs(russia_inside)
    mrs_russia_outside = to_mrs(russia_outside)
    mrs_ukraine_inside = to_mrs(ukraine_inside)
    compile_mrs(mrs_russia_inside, 'russia_inside_domain')
    compile_mrs(mrs_russia_outside, 'russia_outside_domain')
    compile_mrs(mrs_ukraine_inside, 'ukraine_inside_domain')

    # Mihomo categories
    for directory in ['Categories', 'Services']:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                domains = to_mrs(lines_from_file(file_path))
                name = os.path.splitext(filename)[0]
                compile_mrs(domains, f'{name}_domain')

    # Mihomo subnets
    for service in SUBNET_SERVICES:
        subnets = lines_from_file(f'Subnets/IPv4/{service}.lst')
        compile_mrs(subnets, f'{service}_ipcidr', behavior='ipcidr')

    # Xray domains
    prepare_dat_domains(russia_inside, 'russia-inside', directories)
    prepare_dat_domains(russia_outside, 'russia-outside')
    prepare_dat_domains(ukraine_inside, 'ukraine-inside')
    prepare_dat_combined(directories)
    generate_dat_domains()
