# -*- coding: utf-8 -*-
"""
    proofchecker
    ~~~~~
    :copyright: (c) 2014-2016 by Halfmoon Labs, Inc.
    :copyright: (c) 2016 blockstack.org
    :license: MIT, see LICENSE for more details.
"""


import socket
import dns.resolver

import dns.name
import dns.message
import dns.query
import dns.flags

from .config import DNS_SERVERS, TXT_RECORD_PREFIX, ADDITIONAL_RDCLASS


def dns_resolver(domain):

    domain = dns.name.from_text(domain)

    if not domain.is_absolute():
        domain = domain.concatenate(dns.name.root)

    request = dns.message.make_query(domain, dns.rdatatype.TXT)
    request.flags |= dns.flags.AD
    request.find_rrset(request.additional, dns.name.root, ADDITIONAL_RDCLASS,
                       dns.rdatatype.OPT, create=True, force_unique=True)

    data = dns.query.udp(request, DNS_SERVERS[0])

    return data.to_text()


def parse_txt_from_data(data):

    proof_txt = None

    data = data.split('\n')

    for entry in data:
        if "blockchainid" in entry:

            data = entry.split('TXT')

            if data[1] != '':
                proof_txt = data[1].lstrip(" ")

    return proof_txt


def get_proof_from_txt_record(domain):

    check_domain = TXT_RECORD_PREFIX + domain
    dns_data = dns_resolver(check_domain)
    proof_txt = parse_txt_from_data(dns_data)

    return proof_txt


if __name__ == '__main__':

    print get_proof_from_txt_record('muneebali.com')
