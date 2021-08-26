#!/usr/bin/python3
from botbase import *
import re

_matchbremen = re.compile(r"([0-9.]+)\s+\([+]?([-0-9.]+)\)")

def bremen(sheets):
    from urllib.request import urlopen
    from bs4 import BeautifulSoup
    url = "https://www.gesundheit.bremen.de/corona/corona/zahlen/corona_fallzahlen-37649"
    client = urlopen(url)
    data = client.read()
    client.close()
    encoding = "UTF-8" # default
    if 'charset=' in client.headers.get('content-type', '').lower():
        encoding = client.headers.get("content-type").lower().split("charset=")[1].strip()
    soup = BeautifulSoup(data, "lxml", from_encoding=encoding)
    stand = soup.find(id="main").find("h2").text
    if not today in stand: raise Exception("Bremen noch alt? " + stand)
    tables = soup.find(id="main").findAll("table")
    row = tables[1].findAll("tr")[1].findAll("td")
    ss, ii = int(row[1].text), int(row[2].text)
    for row in tables[0].findAll("tr")[2:]:
        row = [x.text.strip() for x in row.findAll("td")]
        # print(row)
        if row[0] == "Stadtgemeinde Bremen": ags, s, i = 4011, ss, ii
        elif row[0] == "Stadtgemeinde Bremerhaven": ags, s, i = 4012, 0, 0
        else: continue
        data = [force_int(y) for x in row[2:5] for y in _matchbremen.match(x).groups()]
        c, cc, g, gg, d, dd = data
        update(sheets, ags, c=c, cc=cc, g=g, gg=gg, s=s, i=i, d=d, dd=dd, sig="Bot", comment="Bot", dry_run=dry_run, ignore_delta=True, date=today)
    return True

schedule.append(Task(16, 15, 18, 30, 300, bremen, 4011))

def main():
    sheets = build('sheets', 'v4', credentials=authorize()).spreadsheets()
    bremen(sheets)

if __name__ == '__main__':
    main()
