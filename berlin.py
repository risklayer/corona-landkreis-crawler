#!/usr/bin/python3
from botbase import *

def berlin(sheets):
    import re
    def _extract(text): return int(re.search(r"(-?[0-9 ]+)", text)[0].replace(" ",""))
    from urllib.request import urlopen
    from bs4 import BeautifulSoup
    url = "https://data.lageso.de/lageso/corona/corona.html"
    client = urlopen(url)
    data = client.read()
    client.close()
    encoding = "UTF-8" # default
    if 'charset=' in client.headers.get('content-type', '').lower():
        encoding = client.headers.get("content-type").lower().split("charset=")[1].strip()
    soup = BeautifulSoup(data, "lxml", from_encoding=encoding)
    stand = soup.find(class_="toptitle").find("p").text
    if not today in stand: raise Exception("Berlin noch alt? " + stand)
    ags = 11000
    c = _extract(soup.find(id="box-fallzahl").find(class_="inner").text)
    d = _extract(soup.find(id="box-todesfaelle").find(class_="inner").text)
    g = _extract(soup.find(id="box-genesene").find(class_="inner").text)
    cc = _extract(soup.find(id="box-fallzahl_diff").find(class_="inner").text)
    dd = _extract(soup.find(id="box-todesfaelle_diff").find(class_="inner").text)
    gg = _extract(soup.find(id="box-genesene_diff").find(class_="inner").text)
    s, i = None, None
    ivena = soup.find(id="selbstauskunft-der-krankenhäuser-in-ivena")
    if ivena:
        for row in ivena.findAll("tr"):
            row = [x.text for x in row.findAll("td")]
            if "stationärer Behandlung" in row[0]: s = int(row[1])
            if "ITS" in row[0]: i = int(row[1])
    update(sheets, ags, c=c, cc=cc, g=g, gg=gg, s=s, i=i, d=d, dd=dd, sig="Bot", comment="Bot", dry_run=dry_run, date=today)
    return True

schedule.append(Task(9, 0, 10, 0, 300, berlin, 11000))
if __name__ == '__main__': berlin(googlesheets())
