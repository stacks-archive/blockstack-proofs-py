# -*- coding: utf-8 -*-
"""
    proofchecker
    ~~~~~
    :copyright: (c) 2014-2016 by Halfmoon Labs, Inc.
    :copyright: (c) 2016 blockstack.org
    :license: MIT, see LICENSE for more details.
"""

import requests
import json
import hashlib

from time import time

from .htmlparsing import get_search_text, get_github_text, get_twitter_url
from .sites import SITES


def contains_valid_proof_statement(search_text, username):
    search_text = search_text.lower()

    verification_styles = [
        "verifying myself: my bitcoin username is +%s" % username,
        "verifying myself: my bitcoin username is %s" % username,
        "verifying myself: my openname is %s" % username,
        "verifying that +%s is my bitcoin username" % username,
        "verifying that %s is my bitcoin username" % username,
        "verifying that %s is my openname" % username,
        "verifying that +%s is my openname" % username,
        "verifying i am +%s on my passcard" % username,
        "verifying that +%s is my blockchain id" % username
    ]

    for verification_style in verification_styles:
        if verification_style in search_text:
            return True

    if "verifymyonename" in search_text and ("+" + username) in search_text:
        return True

    return False


def is_valid_proof(site, site_username, username, proof_url):

    site_username = site_username.lower()
    proof_url = proof_url.lower()
    username = username.lower()

    if site not in SITES and 'base_url' in SITES[site]:
        return False

    check_url = SITES[site]['base_url'] + site_username

    if not proof_url.startswith(check_url):

        if site == 'facebook':
            check_url = SITES['facebook-www']['base_url'] + site_username
            if not proof_url.startswith(check_url):
                return False
        else:
            return False

    try:
        r = requests.get(proof_url)
    except:
        return False

    if site == 'twitter':

        # fix for twitter checking only tweet IDs and forwarding requests
        # fetch URL of the page the request got forwarded to
        proof_url = get_twitter_url(r.text)

        proof_url = proof_url.lower()

        if not proof_url.startswith(check_url):
            return False

    if site == "github":
        try:
            search_text = get_github_text(r.text)
        except:
            search_text = ''
    elif site in SITES:
        try:
            search_text = get_search_text(site, r.text)
        except:
            search_text = ''
    else:
        search_text = ''

    return contains_valid_proof_statement(search_text, username)


def site_data_to_proof_url(site_data, identifier):
    proof_url = None

    if "proof" in site_data:
        proof = site_data["proof"]
    else:
        return proof_url

    if isinstance(proof, (str, unicode)):
        proof_url = proof

    elif isinstance(proof, dict):
        if "url" in proof:
            proof_url = proof["url"]
        elif "id" in proof:
            if key == "twitter":
                proof_url = "https://twitter.com/" + username + "/status/" + proof["id"]
            elif key == "github":
                proof_url = "https://gist.github.com/" + username + "/" + proof["id"]
            elif key == "facebook":
                proof_url = "https://facebook.com/" + username + "/posts/" + proof["id"]

    return proof_url


def site_data_to_identifier(site_data):
    identifier = None
    if "username" in site_data:
        identifier = site_data["username"]
    if "identifier" in site_data:
        identifier = site_data["identifier"]
    if "userid" in site_data:
        identifier = site_data["userid"]
    return identifier


def profile_to_proofs(profile, username, refresh=False):

    proofs = []

    try:
        test = profile.items()
    except:
        return proofs

    for proof_site, site_data in profile.items():
        if proof_site in SITES and isinstance(site_data, dict):
            identifier = site_data_to_identifier(site_data)
            if identifier:
                proof_url = site_data_to_proof_url(site_data, identifier)
                if proof_url:
                    proof = {
                        "service": proof_site,
                        "proof_url": proof_url,
                        "identifier": identifier,
                        "valid": False
                    }

                    if is_valid_proof(proof_site, identifier, username, proof_url):
                        proof["valid"] = True

                    proofs.append(proof)
    return proofs


def profile_v3_to_proofs(profile, username, refresh=False):
    """
        Convert profile format v3 to proofs
    """

    proofs = []

    try:
        test = profile.items()
    except:
        return proofs

    if 'accounts' in profile:
        accounts = profile['account']
    else:
        return proofs

    for account in accounts:

        # skip if proof service is not supported
        if 'service' in account and account['service'] not in SITES:
            continue

        if 'proofType' in account and account['proofType'] == "http":

            try:
                proof = {"service": account['service'],
                         "proof_url": account['proofUrl'],
                         "identifier": account['identifier'],
                         "valid": False}

                if is_valid_proof(account['service'], account['identifier'],
                                  username, account['proofUrl']):

                    proof["valid"] = True

                proofs.append(proof)
            except Exception as e:
                pass

    return proofs
