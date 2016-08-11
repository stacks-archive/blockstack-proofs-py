#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    proofchecker
    ~~~~~
    :copyright: (c) 2014-2015 by Halfmoon Labs, Inc.
    :copyright: (c) 2016 blockstack.org
    :license: MIT, see LICENSE for more details.
"""

import os
import sys
import json
import unittest
import requests

# Hack around absolute paths
current_dir = os.path.abspath(os.path.dirname(__file__))
parent_dir = os.path.abspath(current_dir + "/../")
sys.path.insert(0, parent_dir)

from blockstack_proofs import profile_to_proofs, profile_v3_to_proofs
from blockstack_proofs import contains_valid_proof_statement
from blockstack_proofs import get_proof_from_txt_record

test_users = ['ryan', 'werner', 'muneeb', 'fredwilson']

test_domains = [{"username": "muneeb", 'domain': 'muneebali.com'}]

check_proofs = ['twitter', 'facebook', 'github']

BASE_URL = 'https://resolver.onename.com/v2/users/'


def get_profile(username):

    resp = requests.get(BASE_URL + username, timeout=10)

    data = resp.json()

    if 'zone_file' in data[username]:
        return data[username]['profile'], data[username]['zone_file']
    else:
        return data[username]['profile'], None


def is_profile_in_legacy_format(profile):
    """
    Is a given profile JSON object in legacy format?
    """
    if isinstance(profile, dict):
        pass
    elif isinstance(profile, (str, unicode)):
        try:
            profile = json.loads(profile)
        except ValueError:
            return False
    else:
        return False

    if "@type" in profile:
        return False

    if "@context" in profile:
        return False

    is_in_legacy_format = False

    if "avatar" in profile:
        is_in_legacy_format = True
    elif "cover" in profile:
        is_in_legacy_format = True
    elif "bio" in profile:
        is_in_legacy_format = True
    elif "twitter" in profile:
        is_in_legacy_format = True
    elif "facebook" in profile:
        is_in_legacy_format = True

    return is_in_legacy_format


class ProofcheckerTestCase(unittest.TestCase):

    def tearDown(self):
        pass

    def test_proofs(self):
        """ Check twitter proof
        """

        for username in test_users:
            profile, zone_file = get_profile(username)

            if not is_profile_in_legacy_format(zone_file):
                proofs = profile_v3_to_proofs(profile, username)
            else:
                proofs = profile_to_proofs(profile, username)

            for proof in proofs:

                if proof['service'] in check_proofs:
                    self.assertTrue(proof['valid'])

    def test_domain_proof(self):
        """ Check domain proof
        """

        for test_domain in test_domains:
            username = test_domain['username']
            domain = test_domain['domain']

            proof_txt = get_proof_from_txt_record(domain)

            validProof = contains_valid_proof_statement(proof_txt, username)

            self.assertTrue(validProof)

if __name__ == '__main__':

    unittest.main()
