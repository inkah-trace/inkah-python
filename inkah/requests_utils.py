# -*- coding: utf-8 -*-

"""
requests.api
~~~~~~~~~~~~

This module provides utilities passing Inkah HTTP headers when making HTTP
requests between services.

:copyright: (c) 2016 by Kenneth Reitz.
:license: MIT, see LICENSE for more details.
"""

import requests

def get(url):
    requests.get(url, headers={})
