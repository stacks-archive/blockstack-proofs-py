#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Proofchecker
    ~~~~~

    copyright: (c) 2014 by Halfmoon Labs, Inc.
    copyright: (c) 2015 by Blockstack.org

This file is part of Proofchecker.

    Proofchecker is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Proofchecker is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Proofchecker. If not, see <http://www.gnu.org/licenses/>.
"""

import os
import sys
import unittest
import requests

# Hack around absolute paths
current_dir = os.path.abspath(os.path.dirname(__file__))
parent_dir = os.path.abspath(current_dir + "/../")
sys.path.insert(0, parent_dir)

from proofchecker import profile_to_proofs
from proofchecker import contains_valid_proof_statement
from proofchecker.domain import get_proof_from_txt_record

test_users = ['muneeb', 'fredwilson']

test_domains = [{"username": "muneeb", 'domain': 'muneebali.com'}]

BASE_URL = 'http://resolver-btc.onename.com/v2/users/'


def get_profile(username):

    resp = requests.get(BASE_URL + username, timeout=10, verify=False)

    data = resp.json()

    return data[username]['profile']


class ProofcheckerTestCase(unittest.TestCase):

    def tearDown(self):
        pass

    def test_twitter_proof(self):
        """ Check twitter proof
        """

        for username in test_users:
            profile = get_profile(username)
            proofs = profile_to_proofs(profile, username)

            for proof in proofs:

                if proof['service'] == 'twitter':
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
