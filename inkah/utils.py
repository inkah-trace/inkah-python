from __future__ import absolute_import

import uuid
import sys


def generate_id():
    return str(uuid.uuid4())


def is_installed(module):
    return module in sys.modules
