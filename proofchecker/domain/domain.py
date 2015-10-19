# -*- coding: utf-8 -*-
"""
    Proofchecker
    ~~~~~

    copyright: (c) 2014 by Halfmoon Labs, Inc.
    copyright: (c) 2015 by Blockstack.org

This file is part of Proofchecker.

    Resolver is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Resolver is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Proofchecker. If not, see <http://www.gnu.org/licenses/>.
"""

import socket
import dns.resolver

DNS_SERVERS = ['8.8.8.8', '8.8.4.4']  # use a Google DNS servers as default
TXT_RECORD_PREFIX = 'blockchainid.proof.'
ADDITIONAL_RDCLASS = 65535


def dns_resolver(domain):
    import dns.name
    import dns.message
    import dns.query
    import dns.flags

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
        if "blockchainid.proof" in entry:

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
