#!/usr/bin/python3
from botbase import *

def zwickau(sheets):
    soup = get_soup("https://www.landkreis-zwickau.de/coronafallzahlen-landkreiszwickau")
    main = soup.find(id="content-inner")
    panel = next(p for p in main.findAll(class_="panel") if "Wochenübersicht Fallzahlen" in p.get_text())
    table = next(t for t in panel.findAll("table") if "kumulativ" in t.get_text())
    rows = [[x.get_text().strip() for x in row.findAll(["th","td"])] for row in table.findAll("tr")]
    #print(*rows, sep="\n")
    col = today().weekday() + 1
    date = rows[0][col] if force_int(rows[1][col]) is not None else ""
    date = check_date(date, "Zwickau")
    assert "alle Infektionsfälle" in rows[1][0]
    c = force_int(rows[1][col])
    cc = c - force_int(rows[1][col - 1]) if col > 1 else None
    assert "aktive Infektionsfälle" in rows[2][0]
    a = force_int(rows[2][col])
    aa = a - force_int(rows[2][col - 1]) if col > 1 else None
    assert "Todesfälle" in rows[3][0]
    d = force_int(rows[3][col])
    dd = d - force_int(rows[3][col - 1]) if col > 1 else None
    g = c - d - a
    update(sheets, 14524, c=c, cc=cc, d=d, dd=dd, g=g, sig="Bot", ignore_delta="mon")
    return True

schedule.append(Task(11, 50, 15, 35, 360, zwickau, 14524))
if __name__ == '__main__': zwickau(googlesheets())
