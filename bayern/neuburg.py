#!/usr/bin/python3
from botbase import *

_neuburg_date = re.compile(r"Fallzahlen vom (\d\d\.\d\d.20\d\d)")

def neuburg(sheets):
    soup = get_soup("http://www.neuburg-schrobenhausen.info/corona-zahlen-2")
    main = soup.find(id="main")
    rows = [[x.get_text().strip() for x in row.findAll(["td","th"])] for row in main.findAll("tr")]
    rows = [[x for x in r if not x == ""] for r in rows]
    rows = [r for r in rows if not len(r) == 0]
    #print(*rows, sep="\n")
    date = _neuburg_date.search(main.get_text()).group(1)
    date = check_date(date, "Neuburg-Schrobenhausen")
    assert "Neuinfektionen" in rows[1][2]
    cc = force_int(rows[1][1])
    assert "Genesene" in rows[2][1]
    gg = force_int(rows[2][0])
    assert "Genesenen" in rows[4][2]
    g = force_int(rows[4][1])
    assert "bisher bestätigt" in rows[5][1]
    c = force_int(rows[5][0])
    assert "Todesfälle" in rows[6][1]
    d = force_int(rows[6][0])
    assert "Kreiskrankenhaus" in rows[7][2]
    assert "KJF Klinik" in rows[8][1]
    s = force_int(rows[7][1]) + force_int(rows[8][0])
    update(sheets, 9185, c=c, cc=cc, d=d, g=g, gg=gg, s=s, sig="Bot", comment="Bot ohne I", ignore_delta="mon")
    return True

schedule.append(Task(12, 30, 16, 35, 360, neuburg, 9185))
if __name__ == '__main__': neuburg(googlesheets())
