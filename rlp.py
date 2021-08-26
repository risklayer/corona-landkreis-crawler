#!/usr/bin/python3
from botbase import *
import re, time
_rlpat = re.compile(r"lua.rlp.de|speyer.de|rhein-pfalz-kreis.de").search

def rlp(sheets):
    blacklist=[7317,7340,7320] # Pirmasens, Südwestpfalz, Zweibrücken
    from urllib.request import urlopen
    from bs4 import BeautifulSoup
    from lxml import etree
    url = "https://lua.rlp.de/de/presse/detail/news/News/detail/coronavirus-sars-cov-2-aktuelle-fallzahlen-fuer-rheinland-pfalz/"
    client = urlopen(url)
    data = client.read()
    client.close()
    encoding = "UTF-8" # default
    if 'charset=' in client.headers.get('content-type', '').lower():
        encoding = client.headers.get("content-type").lower().split("charset=")[1].strip()
    soup = BeautifulSoup(data, "lxml", from_encoding=encoding)
    stand = soup.find(id="content").find("h5").text
    if not today in stand: raise Exception("RLP noch alt? " + stand)
    for row in soup.find(id="content").findAll("tr")[3:-1]:
        row = [x.text.strip() for x in row.findAll("td")]
        #print(row)
        ags = ags_from_name(row[0])
        if ags in blacklist: continue
        if not ags:
            print("Name not mapped:", row[0])
            continue
        c, d, g = int(row[1]), int(row[4]), int(row[5])
        cc = int(row[2])
        #print("AGS", ags, c, cc, g, d)
        update(sheets, ags, c=c, cc=cc, g=g, d=d, sig="Land", comment="Bot", dry_run=dry_run, date=today, check=_rlpat)
        time.sleep(50) # avoid rate limit problems
    return True

def main():
    sheets = build('sheets', 'v4', credentials=authorize()).spreadsheets()
    rlp(sheets)

if __name__ == '__main__':
    main()
