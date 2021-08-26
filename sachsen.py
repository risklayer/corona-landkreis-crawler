#!/usr/bin/python3
from botbase import *
import re
_sachsen = re.compile(r"coronavirus.sachsen.de").search

def sachsen(sheets):
    from urllib.request import urlopen
    from bs4 import BeautifulSoup
    from lxml import etree
    import json, dateutil.parser, datetime
    # url = "https://www.coronavirus.sachsen.de/infektionsfaelle-in-sachsen-4151.html"
    url = "https://www.coronavirus.sachsen.de/corona-statistics/rest/stateOfDataApi.jsp"
    client = urlopen(url)
    data = client.read()
    client.close()
    updated = dateutil.parser.isoparse(json.loads(data).get("lastUpdate"))
    if updated.date() != datetime.date.today(): raise Exception("Sachsen noch alt? " + str(updated))
    updated = updated.strftime("%d.%m.%Y %H:%M")

    url = "https://www.coronavirus.sachsen.de/corona-statistics/rest/infectionOverview.jsp"
    client = urlopen(url)
    data = client.read()
    client.close()
    for ags, v in json.loads(data).items():
        ags = int(ags)
        if ags == 14: continue # Land. Unten G ausfüllen?
        # print(ags, v)
        c, cc, d, dd = v["totalInfections"], v["infectionsDifferenceToYesterday"], v["totalDeaths"], v["deathsDifferenceToYesterday"]
        update(sheets, ags, c=c, cc=cc, d=d, dd=dd, sig="Land", comment="Bot", dry_run=dry_run, date=updated, check=_sachsen)
    return True

def main():
    sheets = build('sheets', 'v4', credentials=authorize()).spreadsheets()
    sachsen(sheets)

if __name__ == '__main__':
    main()
