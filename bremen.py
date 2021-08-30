#!/usr/bin/python3
from botbase import *
import re

_matchbremen = re.compile(r"([0-9.]+)\s+\([+]?([-0-9.]+)\)")

def bremen(sheets):
    soup = get_soup("https://www.gesundheit.bremen.de/corona/corona/zahlen/corona_fallzahlen-37649")
    stand = soup.find(id="main").find("h2").text
    if not datetime.date.today().strftime("%d.%m.%Y") in stand: raise NotYetAvailableException("Bremen noch alt? " + stand)
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
        update(sheets, ags, c=c, cc=cc, g=g, gg=gg, s=s, i=i, d=d, dd=dd, sig="Bot", ignore_delta=True)
    return True

schedule.append(Task(16, 00, 18, 30, 300, bremen, 4011))
if __name__ == '__main__': bremen(googlesheets())
