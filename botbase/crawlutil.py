# Ignore certificates:
import ssl
_ctx = ssl.create_default_context()
_ctx.check_hostname = False
_ctx.verify_mode = ssl.CERT_NONE

def get_raw(url):
    from urllib.request import urlopen
    with urlopen(url, context=_ctx) as client:
        return client.read()

def get_json(url):
    from urllib.request import urlopen
    import json
    with urlopen(url, context=_ctx) as client:
        return json.loads(client.read())

def get_soup(url):
    from urllib.request import urlopen
    from bs4 import BeautifulSoup
    with urlopen(url, context=_ctx) as client:
        data = client.read()
        encoding = "UTF-8" # default
        if 'charset=' in client.headers.get('content-type', '').lower():
            encoding = client.headers.get("content-type").lower().split("charset=")[1].strip()
        return BeautifulSoup(data, "lxml", from_encoding=encoding)

def get_csv(url):
    import pandas
    from urllib.request import urlopen
    with urlopen(url, context=_ctx) as client:
        return pandas.read_csv(client, sep=";")

