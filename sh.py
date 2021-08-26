#!/usr/bin/python3
from botbase import *
import re
_shpat = re.compile(r"schleswig-holstein.de").search

def sh(sheets):
    from urllib.request import urlopen
    from bs4 import BeautifulSoup
    from lxml import etree
    url = "https://www.schleswig-holstein.de/DE/Schwerpunkte/Coronavirus/Zahlen/zahlen_node.html"
    client = urlopen(url)
    data = client.read()
    client.close()
    encoding = "UTF-8" # default
    if 'charset=' in client.headers.get('content-type', '').lower():
        encoding = client.headers.get("content-type").lower().split("charset=")[1].strip()
    soup = BeautifulSoup(data, "lxml", from_encoding=encoding)
    table = soup.find(id="cvd19_kreistabelle_kumulativ")
    if not table: raise Exception("SH HTML Tabelle cvd19_kreistabelle_kumulativ nicht gefunden.")
    stand = table.findNext("p").text
    if not today in stand: raise Exception("Schleswig-Holstein noch alt? " + stand)
    for row in table.find("tbody").findAll("tr"):
        row = [x.text.strip() for x in row.findAll("td")]
        #print(row)
        ags = ags_from_name(row[0])
        if not ags:
            print("Name not mapped:", row[0])
            continue
        c, d = force_int(row[2]), force_int(row[6], 0)
        cc, dd = force_int(row[3]), force_int(row[7], 0)
        print("AGS", ags, c, cc, d, dd)
        #cur = is_signed(sheets, ags)
        #if cur is None or cur == "RKI":
            #print("AGS", ags, c, cc, d, dd)
        update(sheets, ags, c=c, cc=cc, d=d, dd=dd, sig="Land", comment="Bot", dry_run=dry_run, date=today, check=_shpat)
    return True

def main():
    sheets = build('sheets', 'v4', credentials=authorize()).spreadsheets()
    sh(sheets)

if __name__ == '__main__':
    main()
