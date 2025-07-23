# app/utils.py

import random
import string
import re

def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def is_valid_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:\S+(?::\S*)?@)?'  # user:pass@
        r'(?:[A-Za-z0-9.-]+)'  # domain
        r'(?:\:[0-9]+)?'       # optional port
        r'(?:[/?]\S*)?$', re.IGNORECASE
    )
    return re.match(regex, url) is not None
