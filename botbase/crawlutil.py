# Ignore certificates:
import ssl
_ctx = ssl.create_default_context()
_ctx.check_hostname = False
_ctx.verify_mode = ssl.CERT_NONE

def get_raw(url):
    import gzip
    from urllib.request import urlopen, Request
    with urlopen(Request(url, headers={'Accept-Encoding': 'gzip'}), context=_ctx, timeout=60) as client:
        data = client.read()
        if client.info().get('Content-Encoding') == 'gzip': data = gzip.decompress(data)
        return data

def get_json(url):
    from urllib.request import urlopen, Request
    import json, gzip
    with urlopen(Request(url, headers={'Accept-Encoding': 'gzip'}), context=_ctx, timeout=60) as client:
        data = client.read()
        if client.info().get('Content-Encoding') == 'gzip': data = gzip.decompress(data)
        return json.loads(data)

def get_soup(url):
    import gzip
    from urllib.request import urlopen, Request
    from bs4 import BeautifulSoup
    with urlopen(Request(url, headers={'Accept-Encoding': 'gzip'}), context=_ctx, timeout=60) as client:
        data = client.read()
        if client.info().get('Content-Encoding') == 'gzip': data = gzip.decompress(data)
        encoding = "UTF-8" # default
        if 'charset=' in client.headers.get('content-type', '').lower():
            encoding = client.headers.get("content-type").lower().split("charset=")[1].strip()
        return BeautifulSoup(data, "lxml", from_encoding=encoding)

def get_csv(url):
    import pandas, gzip
    from urllib.request import urlopen, Request
    from io import StringIO
    with urlopen(Request(url, headers={'Accept-Encoding': 'gzip'}), context=_ctx, timeout=60) as client:
        data = client.read()
        if client.info().get('Content-Encoding') == 'gzip': data = gzip.decompress(data)
        return pandas.read_csv(StringIO(data.decode("utf-8")), sep=";")

