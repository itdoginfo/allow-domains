#!/usr/bin/python3.10

import tldextract
import urllib.request
import re
from pathlib import Path

rusDomainsInsideOut='Russia/inside'
rusDomainsInsideSrcSingle='src/Russia-domains-inside-single.lst'
rusDomainsInsideCategories='Categories'
rusDomainsInsideServices='Services'
rusDomainsOutsideSrc='src/Russia-domains-outside.lst'
rusDomainsOutsideOut='Russia/outside'
uaDomainsSrc='src/Ukraine-domains-inside.lst'
uaDomainsOut='Ukraine/inside'

def raw(src, out):
    domains_raw = set()
    files = []

    if isinstance(src, list):
        for dir_path in src:
            path = Path(dir_path)
            if path.is_dir():
                files.extend(path.glob('*'))
            elif path.is_file():
                files.append(path)

    for f in files:
        with open(f) as infile:
                for line in infile:
                    if tldextract.extract(line).suffix:
                        domains_raw.add(line.rstrip())

    domains_raw = sorted(domains_raw)

    with open(f'{out}-raw.lst', 'w') as file:
        for name in domains_raw:
            file.write(f'{name}\n')

def dnsmasq(src, out, remove={'google.com'}):
    domains = set()
    domains_single = set()
    files = []

    if isinstance(src, list):
        for dir_path in src:
            path = Path(dir_path)
            if path.is_dir():
                files.extend(path.glob('*'))
            elif path.is_file():
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
                files.extend(path.glob('*'))
            elif path.is_file():
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
                files.extend(path.glob('*'))
            elif path.is_file():
                files.append(path)

    for f in files:
        with open(f) as infile:
                for line in infile:
                    if tldextract.extract(line).suffix:
                        if re.search(r'[^а-я\-]', tldextract.extract(line).domain):
                            domains.add(tldextract.extract(line.rstrip()).fqdn)
                        if not tldextract.extract(line).domain and tldextract.extract(line).suffix:
                            domains.add(tldextract.extract(line.rstrip()).suffix)

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
                files.extend(path.glob('*'))
            elif path.is_file():
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
            file.write(f'/ip dns static add name={name} type=FWD address-list=allow-domains match-subdomain=yes forward-to=localhost\n')

if __name__ == '__main__':
    # Russia inside
    Path("Russia").mkdir(parents=True, exist_ok=True)

    removeDomains = {'google.com', 'googletagmanager.com', 'github.com', 'githubusercontent.com', 'githubcopilot.com', 'microsoft.com', 'cloudflare-dns.com', 'parsec.app' }
    removeDomainsKvas = {'google.com', 'googletagmanager.com', 'github.com', 'githubusercontent.com', 'githubcopilot.com', 'microsoft.com', 'cloudflare-dns.com', 'parsec.app', 't.co' }
    
    inside_lists = [rusDomainsInsideCategories, rusDomainsInsideServices]

    raw(inside_lists, rusDomainsInsideOut)
    dnsmasq(inside_lists, rusDomainsInsideOut, removeDomains)
    clashx(inside_lists, rusDomainsInsideOut, removeDomains)
    kvas(inside_lists, rusDomainsInsideOut, removeDomainsKvas)
    mikrotik_fwd(inside_lists, rusDomainsInsideOut, removeDomains)

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

    dnsmasq(ua_lists, uaDomainsOut)
    clashx(ua_lists, uaDomainsOut)
    kvas(ua_lists, uaDomainsOut)
    mikrotik_fwd(ua_lists, uaDomainsOut)

    for temp_file in ['uablacklist-domains.lst', 'zaboronahelp-domains.lst']:
        Path(temp_file).unlink()