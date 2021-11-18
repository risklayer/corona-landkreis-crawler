#!/usr/bin/python3
from botbase import *

_dadi1 = re.compile(r"\(\+?\s*(-?[0-9.]+)\s*(?:zum Vortag)?\)", re.M)
_dadi2 = re.compile(r"\s*(-?[0-9.]+)\s*\*?\s*", re.M)

def dadi(sheets):
    data = get_soup("https://perspektive.ladadi.de/corona-news/")
    body = data.find("main")
    rows = [[x.get_text() for x in y.findAll(["td","th"])] for y in body.find("table").findAll("tr")]
    #print(*rows, sep="\n")
    date = check_date(rows[0][0], "Darmstadt-Dieburg")
    assert "Bestätigte" in rows[0][1]
    c = force_int(_dadi2.match(rows[1][1]).group(1))
    m = _dadi1.search(rows[0][1])
    cc = force_int(m.group(1)) if m else None
    assert "Todesfälle" in rows[0][2]
    d = force_int(_dadi2.match(rows[1][2]).group(1))
    m = _dadi1.search(rows[0][2])
    dd = force_int(m.group(1)) if m else None
    assert "gesund" in rows[0][4]
    g = force_int(_dadi2.match(rows[1][4]).group(1))
    update(sheets, 6432, c=c, cc=cc, g=g, d=d, dd=dd, sig="Bot", comment="Bot ohne SI", ignore_delta=False)
    return True

schedule.append(Task(17, 00, 18, 50, 360, dadi, 6432))
if __name__ == '__main__': dadi(googlesheets())
