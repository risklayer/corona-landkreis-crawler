#!/usr/bin/python3
from botbase import *
import re

_matchbremen = re.compile(r"([0-9.]+)\s*(?:\([+ ]*([-0-9.]+)\))?")
_matchh1bremen = re.compile(r"^Stadt Bremen")
_matchh1bremerhaven = re.compile(r"^Stadt Bremerhaven")

def bremen(sheets):
    soup = get_soup("https://www.gesundheit.bremen.de/corona/corona/zahlen/corona_fallzahlen-37649")
    main = soup.find(id="main")
    stand = main.find("h2").text
    if not datetime.date.today().strftime("%d.%m.%Y") in stand: raise NotYetAvailableException("Bremen noch alt? " + stand)
    tables = main.findAll("table")
    b, bh = dict(), dict()
    for table in tables:
        text = table.parent.parent.get_text(" ").strip()
        if not datetime.date.today().strftime("%d.%m.%Y") in text: continue
        rows = [[x.get_text().strip() for x in row.findAll(["th","td"])] for row in table.findAll("tr")]
        #print(*rows,"---",sep="\n")
        if rows[0][1] == "Aktive Infektionen":
            assert "insgesamt" in rows[0][2]
            assert "Genesene" in rows[0][3]
            assert "Verstorben" in rows[0][4]
            if rows[1][0] == "Stadtgemeinde Bremen":
                b["c"], b["cc"] = map(force_int, _matchbremen.match(rows[1][2]).groups())
                b["g"], b["gg"] = map(force_int, _matchbremen.match(rows[1][3]).groups())
                b["d"], b["dd"] = map(force_int, _matchbremen.match(rows[1][4]).groups())
            if rows[1][0] == "Stadtgemeinde Bremerhaven":
                bh["c"], bh["cc"] = map(force_int, _matchbremen.match(rows[1][2]).groups())
                bh["g"], bh["gg"] = map(force_int, _matchbremen.match(rows[1][3]).groups())
                bh["d"], bh["dd"] = map(force_int, _matchbremen.match(rows[1][4]).groups())
        if rows[0][1] == "Stationär versorgt":
            assert "Intensiv" in rows[0][2]
            if "Stadtgemeinde Bremen" in rows[1][0] and not "s" in b:
                b["s"], b["i"] = map(force_int, rows[1][1:3])
            if "Stadtgemeinde Bremerhaven" in rows[1][0] and not "s" in bh:
                bh["s"], bh["i"] = map(force_int, rows[1][1:3])
    #print(b, bh, sep="\n")
    if not "c" in b and "d" in b and "c" in bh and "d" in bh: return False
    update(sheets, 4011, **b, sig="Bot", ignore_delta=True)
    update(sheets, 4012, **bh, sig="Bot", ignore_delta=True)
    return True

schedule.append(Task(16, 00, 18, 30, 300, bremen, 4011))
if __name__ == '__main__': bremen(googlesheets())
