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


MEMCACHED_ENABLED = False

DEFAULT_PORT = 5000
DEFAULT_HOST = '0.0.0.0'
MEMCACHED_PORT = 11211
MEMCACHED_SERVER = '127.0.0.1'

RECENT_BLOCKS = 100
VALID_BLOCKS = 36000
REFRESH_BLOCKS = 25

MEMCACHED_TIMEOUT = 12 * 60 * 60

try:
    MEMCACHED_USERNAME = os.environ['MEMCACHEDCLOUD_USERNAME']
    MEMCACHED_PASSWORD = os.environ['MEMCACHEDCLOUD_PASSWORD']
except:
    try:
        MEMCACHED_USERNAME = os.environ['MEMCACHIER_USERNAME']
        MEMCACHED_PASSWORD = os.environ['MEMCACHIER_PASSWORD']
    except:
        MEMCACHED_USERNAME = None
        MEMCACHED_PASSWORD = None

try:
    MEMCACHED_SERVERS = os.environ['MEMCACHEDCLOUD_SERVERS'].split(',')
except:
    try:
        MEMCACHED_SERVERS = os.environ['MEMCACHIER_SERVERS'].split(',')
    except:
        memcached_server = MEMCACHED_SERVER + ':' + str(MEMCACHED_PORT)
        MEMCACHED_SERVERS = [memcached_server]
