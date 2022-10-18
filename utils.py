import json
import sys


class APIException(Exception):
    def __init__(self, message, code):
        Exception.__init__(self, message)
        self.code = code

#RPC Address
BASE_URL = "http://198.204.255.156:26657/"
TIMEOUT = 10


py_version = sys.version_info[0]
if py_version >= 3:
    # Python 3.0 and later
    from urllib.request import urlopen
    from urllib.error import HTTPError
    from urllib.parse import urlencode
else:
    # Python 2.x
    from urllib2 import urlopen
    from urllib2 import HTTPError
    from urllib import urlencode


def call_api(resource, data=None, base_url=None):
    base_url = BASE_URL if base_url is None else base_url
    try:
        payload = None if data is None else urlencode(data)
        if py_version >= 3 and payload is not None:
            payload = payload.encode('UTF-8')
        response = urlopen(base_url + resource, payload, timeout=TIMEOUT).read()
        return handle_response(response)
            
    except HTTPError as e:
        raise APIException(handle_response(e.read()), e.code)


def handle_response(response):
    # urllib returns different types in Python 2 and 3 (str vs bytes)
    if isinstance(response, str):
        return response
    else:
        return response.decode('utf-8')
