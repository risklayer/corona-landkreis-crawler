# Ignore certificates:
import ssl
_ctx = ssl.create_default_context()
_ctx.check_hostname = False
_ctx.verify_mode = ssl.CERT_NONE

def get_raw(url):
    import gzip
    from urllib.request import urlopen, Request
    with urlopen(Request(url, headers={'Accept-Encoding': 'gzip', 'User-Agent': 'RiskLayer Spreadsheet Bot'}), context=_ctx, timeout=60) as client:
        data = client.read()
        if client.info().get('Content-Encoding') == 'gzip': data = gzip.decompress(data)
        return data

def get_json(url):
    from urllib.request import urlopen, Request
    import json, gzip
    with urlopen(Request(url, headers={'Accept-Encoding': 'gzip', 'User-Agent': 'RiskLayer Spreadsheet Bot'}), context=_ctx, timeout=60) as client:
        data = client.read()
        if client.info().get('Content-Encoding') == 'gzip': data = gzip.decompress(data)
        return json.loads(data)

def get_soup(url):
    import gzip
    from urllib.request import urlopen, Request
    from bs4 import BeautifulSoup
    with urlopen(Request(url, headers={'Accept-Encoding': 'gzip', 'User-Agent': 'RiskLayer Spreadsheet Bot'}), context=_ctx, timeout=60) as client:
        data = client.read()
        if client.info().get('Content-Encoding') == 'gzip': data = gzip.decompress(data)
        encoding = "UTF-8" # default
        if 'charset=' in client.headers.get('content-type', '').lower():
            encoding = client.headers.get("content-type").lower().split("charset=")[1].strip()
        return BeautifulSoup(data, "lxml", from_encoding=encoding)

def get_csv(url, sep=";"):
    import pandas, gzip
    from urllib.request import urlopen, Request
    from io import StringIO
    with urlopen(Request(url, headers={'Accept-Encoding': 'gzip', 'User-Agent': 'RiskLayer Spreadsheet Bot'}), context=_ctx, timeout=60) as client:
        data = client.read()
        if client.info().get('Content-Encoding') == 'gzip': data = gzip.decompress(data)
        return pandas.read_csv(StringIO(data.decode("utf-8")), sep=sep)

def get_pdf_text(url, **kwargs):
    from pdfminer.high_level import extract_text_to_fp
    from urllib.request import urlopen, Request
    from io import BytesIO, StringIO
    with urlopen(Request(url, headers={'Accept-Encoding': 'gzip', 'User-Agent': 'RiskLayer Spreadsheet Bot'}), context=_ctx, timeout=60) as client:
        #if client.info().get("Content-Type") != "application/pdf":
        data = BytesIO(client.read())
        out = StringIO()
        extract_text_to_fp(data, out, **kwargs)
        return out.getvalue()
