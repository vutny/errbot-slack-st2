# -*- coding: utf-8 -*-

"""
This is a minimal configuration to get you started with Errbot and StackStorm.

Checkout the options in the more complete config-template.py from here:
https://raw.githubusercontent.com/errbotio/errbot/master/errbot/config-template.py
"""


import importlib
import os
import sys


# Import default ``config.py``
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ERRBOT_CONFIG = importlib.import_module('config')

# Get all constants from ``config.py``
ERRBOT_DICT = ERRBOT_CONFIG.__dict__
try:
    ERRBOT_SETTINGS = ERRBOT_DICT.__all__
except AttributeError:
    ERRBOT_SETTINGS = [name for name in ERRBOT_DICT if not name.startswith('_')]
globals().update({name: ERRBOT_DICT[name] for name in ERRBOT_SETTINGS})


ST2_HOST = os.environ['ST2_HOST']

# err-stackstorm's plugin settings
STACKSTORM = {
    'api_auth': {
        'key': os.environ['ST2_API_KEY'],
    },
    'auth_url': 'https://{}/auth/v1'.format(ST2_HOST),
    'api_url': 'https://{}/api/v1'.format(ST2_HOST),
    'stream_url': 'https://{}/stream/v1'.format(ST2_HOST),
    'verify_cert': False,  # ST2 uses self-signed cert
    # Interval for Errbot to refresh a list of available action aliases.
    'timer_update': 900,  # Unit: seconds.
}
