#!/usr/bin/python3.10

import tldextract
import urllib.request
import re
from pathlib import Path

rusDomainsInsideSrc='src/Russia-domains-inside.lst'
rusDomainsInsideOut='Russia/inside'
rusDomainsOutsideSrc='src/Russia-domains-outside.lst'
rusDomainsOutsideOut='Russia/outside'
uaDomainsOut='Ukraine/inside'

def raw(src, out):
    domains_raw = set()

    for f in src:
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

    for f in src:
        with open(f) as infile:
                for line in infile:
                    if tldextract.extract(line).suffix:
                        if re.search(r'[^а-я\-]', tldextract.extract(line).domain):
                            domains.add(tldextract.extract(line.rstrip()).registered_domain)

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

    for f in src:
        with open(f) as infile:
                for line in infile:
                    if tldextract.extract(line).suffix:
                        if re.search(r'[^а-я\-]', tldextract.extract(line).domain):
                            domains.add(tldextract.extract(line.rstrip()).registered_domain)

    domains = domains - remove
    domains = sorted(domains)

    with open(f'{out}-clashx.lst', 'w') as file:
        for name in domains:
            file.write(f'DOMAIN-SUFFIX,{name}\n')

if __name__ == '__main__':
    # Russia inside
    Path("Russia").mkdir(parents=True, exist_ok=True)

    removeDomains = {'google.com', 'youtube.com'}
    urllib.request.urlretrieve("https://community.antifilter.download/list/domains.lst", "antifilter-domains.lst")
    inside_lists = ['antifilter-domains.lst', rusDomainsInsideSrc]

    raw(inside_lists, rusDomainsInsideOut)
    dnsmasq(inside_lists, rusDomainsInsideOut, removeDomains)
    clashx(inside_lists, rusDomainsInsideOut, removeDomains)

    # Russia outside
    ouside_lists = [rusDomainsOutsideSrc]

    raw(ouside_lists, rusDomainsOutsideOut)
    dnsmasq(ouside_lists, rusDomainsOutsideOut)
    clashx(ouside_lists, rusDomainsOutsideOut)

    # Ukraine
    Path("Ukraine").mkdir(parents=True, exist_ok=True)

    urllib.request.urlretrieve("https://uablacklist.net/domains.txt", "uablacklist-domains.lst")
    ua_lists = ['uablacklist-domains.lst']

    dnsmasq(ua_lists, uaDomainsOut)
    clashx(ua_lists, uaDomainsOut)