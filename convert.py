#!/usr/bin/python3.10

import tldextract
import urllib.request
import re
from pathlib import Path
import json
import os
import subprocess

rusDomainsInsideOut='Russia/inside'
rusDomainsInsideSrcSingle='src/Russia-domains-inside-single.lst'
rusDomainsInsideCategories='Categories'
rusDomainsInsideServices='Services'
rusDomainsOutsideSrc='src/Russia-domains-outside.lst'
rusDomainsOutsideOut='Russia/outside'
uaDomainsSrc='src/Ukraine-domains-inside.lst'
uaDomainsOut='Ukraine/inside'
DiscordSubnets = 'Subnets/IPv4/discord.lst'
MetaSubnets = 'Subnets/IPv4/meta.lst'
TwitterSubnets = 'Subnets/IPv4/twitter.lst'
TelegramSubnets = 'Subnets/IPv4/telegram.lst'
CloudflareSubnets = 'Subnets/IPv4/cloudflare.lst'
HetznerSubnets = 'Subnets/IPv4/hetzner.lst'
OVHSubnets = 'Subnets/IPv4/ovh.lst'
DigitalOceanSubnets = 'Subnets/IPv4/digitalocean.lst'
CloudfrontSubnets = 'Subnets/IPv4/cloudfront.lst'
ExcludeServices = {"telegram.lst", "cloudflare.lst", "google_ai.lst", "google_play.lst", 'hetzner.lst', 'ovh.lst', 'digitalocean.lst', 'cloudfront.lst', 'hodca.lst'}

def raw(src, out):
    domains = set()
    files = []

    if isinstance(src, list):
        for dir_path in src:
            path = Path(dir_path)
            if path.is_dir():
                files.extend(f for f in path.glob('*') if f.name not in ExcludeServices)
            elif path.is_file() and path.name not in ExcludeServices:
                files.append(path)

    for f in files:
        if f.is_file():
            with open(f) as infile:
                    for line in infile:
                        if tldextract.extract(line).suffix:
                            if re.search(r'[^а-я\-]', tldextract.extract(line).domain):
                                domains.add(tldextract.extract(line.rstrip()).fqdn)
                            if not tldextract.extract(line).domain and tldextract.extract(line).suffix:
                                domains.add("." + tldextract.extract(line.rstrip()).suffix)

    domains = sorted(domains)

    with open(f'{out}-raw.lst', 'w') as file:
        for name in domains:
            file.write(f'{name}\n')

def dnsmasq(src, out, remove={'google.com'}):
    domains = set()
    domains_single = set()
    files = []

    if isinstance(src, list):
        for dir_path in src:
            path = Path(dir_path)
            if path.is_dir():
                files.extend(f for f in path.glob('*') if f.name not in ExcludeServices)
            elif path.is_file() and path.name not in ExcludeServices:
                files.append(path)

    for f in files:
        if f.is_file():
            with open(f) as infile:
                    for line in infile:
                        if tldextract.extract(line).suffix:
                            if re.search(r'[^а-я\-]', tldextract.extract(line).domain):
                                domains.add(tldextract.extract(line.rstrip()).fqdn)
                            if not tldextract.extract(line).domain and tldextract.extract(line).suffix:
                                domains.add("." + tldextract.extract(line.rstrip()).suffix)

    domains = domains - remove
    domains = sorted(domains)

    with open(f'{out}-dnsmasq-nfset.lst', 'w') as file:
        for name in domains:
            file.write(f'nftset=/{name}/4#inet#fw4#vpn_domains\n')

    with open(f'{out}-dnsmasq-ipset.lst', 'w') as file:
        for name in domains:
            file.write(f'ipset=/{name}/vpn_domains\n')

def clashx(src, out, remove={'google.com'}):
    domains = set()
    domains_single = set()
    files = []

    if isinstance(src, list):
        for dir_path in src:
            path = Path(dir_path)
            if path.is_dir():
                files.extend(f for f in path.glob('*') if f.name not in ExcludeServices)
            elif path.is_file() and path.name not in ExcludeServices:
                files.append(path)

    for f in files:
        with open(f) as infile:
                for line in infile:
                    if tldextract.extract(line).suffix:
                        if re.search(r'[^а-я\-]', tldextract.extract(line).domain):
                            domains.add(tldextract.extract(line.rstrip()).fqdn)
                        if not tldextract.extract(line).domain and tldextract.extract(line).suffix:
                            domains.add("." + tldextract.extract(line.rstrip()).suffix)

    domains = domains - remove
    domains = sorted(domains)

    with open(f'{out}-clashx.lst', 'w') as file:
        for name in domains:
            file.write(f'DOMAIN-SUFFIX,{name}\n')

def kvas(src, out, remove={'google.com'}):
    domains = set()
    domains_single = set()
    files = []

    if isinstance(src, list):
        for dir_path in src:
            path = Path(dir_path)
            if path.is_dir():
                files.extend(f for f in path.glob('*') if f.name not in ExcludeServices)
            elif path.is_file() and path.name not in ExcludeServices:
                files.append(path)

    for f in files:
        with open(f) as infile:
                for line in infile:
                    if tldextract.extract(line).suffix:
                        if re.search(r'[^а-я\-]', tldextract.extract(line).domain):
                            domains.add(tldextract.extract(line.rstrip()).fqdn)
                        if not tldextract.extract(line).domain and tldextract.extract(line).suffix:
                            domains.add(tldextract.extract(line.rstrip()).suffix)

    domains = domains - remove
    domains = sorted(domains)

    with open(f'{out}-kvas.lst', 'w') as file:
        for name in domains:
            file.write(f'{name}\n')

def mikrotik_fwd(src, out, remove={'google.com'}):
    domains = set()
    domains_single = set()
    files = []

    if isinstance(src, list):
        for dir_path in src:
            path = Path(dir_path)
            if path.is_dir():
                files.extend(f for f in path.glob('*') if f.name not in ExcludeServices)
            elif path.is_file() and path.name not in ExcludeServices:
                files.append(path)

    for f in files:
        with open(f) as infile:
                for line in infile:
                    if tldextract.extract(line).suffix:
                        if re.search(r'[^а-я\-]', tldextract.extract(line).domain):
                            domains.add(tldextract.extract(line.rstrip()).fqdn)
                        if not tldextract.extract(line).domain and tldextract.extract(line).suffix:
                            domains.add("." + tldextract.extract(line.rstrip()).suffix)

    domains = domains - remove
    domains = sorted(domains)

    with open(f'{out}-mikrotik-fwd.lst', 'w') as file:
        for name in domains:
            if name.startswith('.'):
                file.write(f'/ip dns static add name=*.{name[1:]} type=FWD address-list=allow-domains forward-to=localhost\n')
            else:
                file.write(f'/ip dns static add name={name} type=FWD address-list=allow-domains match-subdomain=yes forward-to=localhost\n')

def domains_from_file(filepath):
    domains = []
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                domain = line.strip()
                if domain:
                    domains.append(domain)
    except FileNotFoundError:
        print(f"File not found: {filepath}")
    return domains

def generate_srs_domains(domains, output_name):
    output_directory = 'JSON'
    compiled_output_directory = 'SRS'

    os.makedirs(output_directory, exist_ok=True)
    os.makedirs(compiled_output_directory, exist_ok=True)

    data = {
        "version": 3,
        "rules": [
            {"domain_suffix": domains}
        ]
    }

    json_file_path = os.path.join(output_directory, f"{output_name}.json")
    srs_file_path = os.path.join(compiled_output_directory, f"{output_name}.srs")

    try:
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4)
        print(f"JSON file generated: {json_file_path}")

        subprocess.run(
            ["sing-box", "rule-set", "compile", json_file_path, "-o", srs_file_path], check=True
        )
        print(f"Compiled .srs file: {srs_file_path}")
    except subprocess.CalledProcessError as e:
        print(f"Compile error {json_file_path}: {e}")
    except Exception as e:
        print(f"Error while processing {output_name}: {e}")

def generate_srs_for_categories(directories, output_json_directory='JSON', compiled_output_directory='SRS'):
    os.makedirs(output_json_directory, exist_ok=True)
    os.makedirs(compiled_output_directory, exist_ok=True)

    exclude = {"meta", "twitter", "discord", "telegram", "hetzner", "ovh", "digitalocean", "cloudfront"}

    for directory in directories:
        for filename in os.listdir(directory):
            if any(keyword in filename for keyword in exclude):
                continue
            file_path = os.path.join(directory, filename)
            
            if os.path.isfile(file_path):
                domains = []
                with open(file_path, 'r', encoding='utf-8') as file:
                    for line in file:
                        domain = line.strip()
                        if domain:
                            domains.append(domain)

            data = {
                "version": 3,
                "rules": [
                    {
                        "domain_suffix": domains
                    }
                ]
            }

            output_file_path = os.path.join(output_json_directory, f"{os.path.splitext(filename)[0]}.json")

            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                json.dump(data, output_file, indent=4)

            print(f"JSON file generated: {output_file_path}")

    print("\nCompile JSON files to .srs files...")
    for filename in os.listdir(output_json_directory):
        if filename.endswith('.json'):
            json_file_path = os.path.join(output_json_directory, filename)
            srs_file_path = os.path.join(compiled_output_directory, f"{os.path.splitext(filename)[0]}.srs")
            try:
                subprocess.run(
                    ["sing-box", "rule-set", "compile", json_file_path, "-o", srs_file_path], check=True
                )
                print(f"Compiled .srs file: {srs_file_path}")
            except subprocess.CalledProcessError as e:
                print(f"Compile error {json_file_path}: {e}")

def generate_srs_subnets(input_file, output_json_directory='JSON', compiled_output_directory='SRS'):
    os.makedirs(output_json_directory, exist_ok=True)
    os.makedirs(compiled_output_directory, exist_ok=True)

    subnets = []
    with open(input_file, 'r', encoding='utf-8') as file:
        for line in file:
            subnet = line.strip()
            if subnet:
                subnets.append(subnet)
    data = {
        "version": 3,
        "rules": [
            {
                "ip_cidr": subnets
            }
        ]
    }

    filename = os.path.splitext(os.path.basename(input_file))[0]
    output_file_path = os.path.join(output_json_directory, f"{filename}.json")

    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        json.dump(data, output_file, indent=4)

    print(f"JSON file generated: {output_file_path}")

    srs_file_path = os.path.join(compiled_output_directory, f"{filename}.srs")
    try:
        subprocess.run(
            ["sing-box", "rule-set", "compile", output_file_path, "-o", srs_file_path], check=True
        )
        print(f"Compiled .srs file: {srs_file_path}")
    except subprocess.CalledProcessError as e:
        print(f"Compile error {output_file_path}: {e}")

def generate_srs_combined(input_subnets_file, input_domains_file, output_json_directory='JSON', compiled_output_directory='SRS'):
    os.makedirs(output_json_directory, exist_ok=True)
    os.makedirs(compiled_output_directory, exist_ok=True)

    domains = []
    if os.path.exists(input_domains_file):
        with open(input_domains_file, 'r', encoding='utf-8') as file:
            domains = [line.strip() for line in file if line.strip()]

    subnets = []
    if os.path.exists(input_subnets_file):
        with open(input_subnets_file, 'r', encoding='utf-8') as file:
            subnets = [line.strip() for line in file if line.strip()]

    if input_subnets_file == "Subnets/IPv4/discord.lst":
        data = {
            "version": 3,
            "rules": [
                {
                    "domain_suffix": domains
                },
                {
                    "network": ["udp"],
                    "ip_cidr": subnets,
                    "port_range": ["50000:65535"]
                }
            ]
        }
    else:
        data = {
            "version": 3,
            "rules": [
                {
                    "domain_suffix": domains,
                    "ip_cidr": subnets
                }
            ]
        }

    filename = os.path.splitext(os.path.basename(input_subnets_file))[0]
    output_file_path = os.path.join(output_json_directory, f"{filename}.json")

    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        json.dump(data, output_file, indent=4)

    print(f"JSON file generated: {output_file_path}")

    srs_file_path = os.path.join(compiled_output_directory, f"{filename}.srs")
    try:
        subprocess.run(
            ["sing-box", "rule-set", "compile", output_file_path, "-o", srs_file_path], check=True
        )
        print(f"Compiled .srs file: {srs_file_path}")
    except subprocess.CalledProcessError as e:
        print(f"Compile error {output_file_path}: {e}")


def prepare_dat_domains(domains, output_name, dirs=[]):
    output_lists_directory = 'geosite_data'
    os.makedirs(output_lists_directory, exist_ok=True)

    domain_attrs = {domain: [] for domain in domains}

    for directory in dirs:
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
    import shutil
    
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
 
def generate_dat_domains(data_path='geosite_data', output_name='geosite.dat', output_directory='DAT'):
    os.makedirs(output_directory, exist_ok=True)

    try:
        subprocess.run(
            ["domain-list-community", f"-datapath={data_path}", f"-outputname={output_name}", f"-outputdir={output_directory}"],
            check=True,
            stdout=subprocess.DEVNULL
        )
        print(f"Compiled .dat file: {output_directory}/{output_name}")
    except subprocess.CalledProcessError as e:
        print(f"Compile error {data_path}: {e}")

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
    russia_inside = domains_from_file('Russia/inside-raw.lst')
    russia_outside = domains_from_file('Russia/outside-raw.lst')
    ukraine_inside = domains_from_file('Ukraine/inside-raw.lst')
    generate_srs_domains(russia_inside, 'russia_inside')
    generate_srs_domains(russia_outside, 'russia_outside')
    generate_srs_domains(ukraine_inside, 'ukraine_inside')

    # Sing-box categories
    directories = ['Categories', 'Services']
    generate_srs_for_categories(directories)

    # Sing-box subnets + domains
    generate_srs_combined(DiscordSubnets, "Services/discord.lst")
    generate_srs_combined(TwitterSubnets, "Services/twitter.lst")
    generate_srs_combined(MetaSubnets, "Services/meta.lst")
    generate_srs_combined(TelegramSubnets, "Services/telegram.lst")
    generate_srs_combined(CloudflareSubnets, "Services/cloudflare.lst")
    generate_srs_combined(HetznerSubnets, "Services/hetzner.lst")
    generate_srs_combined(OVHSubnets, "Services/ovh.lst")
    generate_srs_combined(DigitalOceanSubnets, "Services/digitalocean.lst")
    generate_srs_combined(CloudfrontSubnets, "Services/cloudfront.lst")

    # Xray domains
    prepare_dat_domains(russia_inside, 'russia-inside', directories)
    prepare_dat_domains(russia_outside, 'russia-outside')
    prepare_dat_domains(ukraine_inside, 'ukraine-inside')
    prepare_dat_combined(directories)
    generate_dat_domains()
