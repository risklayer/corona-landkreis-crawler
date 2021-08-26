#!/usr/bin/python3
from botbase import *
import re, time
_lglpat = re.compile(r"lgl.bayern.de").search

def lgl(sheets):
    from urllib.request import urlopen
    from bs4 import BeautifulSoup
    from lxml import etree
    url = "https://www.lgl.bayern.de/gesundheit/infektionsschutz/infektionskrankheiten_a_z/coronavirus/karte_coronavirus/index.htm"
    client = urlopen(url)
    data = client.read()
    client.close()
    encoding = "UTF-8" # default
    if 'charset=' in client.headers.get('content-type', '').lower():
        encoding = client.headers.get("content-type").lower().split("charset=")[1].strip()
    soup = BeautifulSoup(data, "lxml", from_encoding=encoding)
    table = soup.find(id="tableLandkreise")
    if not table: raise Exception("LGL HTML Tabelle tableLandkreise nicht gefunden.")
    if not today in table.find("caption").text: raise Exception("LGL noch alt? " +table.find("caption").text)
    for row in table.findAll("tr")[1:-1]:
        row = [x.text.strip() for x in row.findAll("td")]
        ags = ags_from_name(row[0])
        if not ags:
            print("Name not mapped:", row[0])
            continue
        c, d = force_int(row[1]), force_int(row[6])
        cc, dd = force_int(row[2]), force_int(row[7])
        #cur = is_signed(sheets, ags)
        #if cur is None or cur == "RKI":
        #    #print("AGS", ags, c, cc, d, dd)
        update(sheets, ags, c=c, cc=cc, d=d, dd=dd, sig="Land", comment="Bot", dry_run=dry_run, date=today, check=_lglpat)
        time.sleep(50) # to avoid rate limit problems
    return True

def main():
    sheets = build('sheets', 'v4', credentials=authorize()).spreadsheets()
    lgl(sheets)

if __name__ == '__main__':
    main()
