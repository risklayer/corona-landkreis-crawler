#!/usr/bin/python3
from botbase import *

_stand = re.compile(r"(\d\d\.\d\d.20\d\d)")
_goerlitz_i = re.compile(r"(\w+)\s+davon benötigen eine intensiv", re.U)

def goerlitz(sheets):
    soup = get_soup("https://www.kreis-goerlitz.de/city_info/webaccessibility/index.cfm?item_id=873097")
    main = soup.find(id="content_frame")
    #print(main)
    date = _stand.search(main.find(text=_stand)).group(1)
    date = check_date(date,"Görlitz")
    rows = [[x.text for x in row.findAll(["th","td"])] for row in main.findAll("tr")]
    #print(*rows, sep="\n")
    assert "Aktuell" in rows[0][1] and "Veränderung" in rows[0][2]
    assert "gesamt" in rows[2][0]
    c, cc = force_int(rows[2][1].replace("*","")), force_int(rows[2][2].replace("*",""))
    assert "Quarant" in rows[3][0]
    a, aa = force_int(rows[3][1].replace("*","")), force_int(rows[3][2].replace("*",""))
    assert "station" in rows[4][0]
    s = force_int(rows[4][1].replace("*",""))
    assert "Tod" in rows[5][0]
    d, dd = force_int(rows[5][1].replace("*","")), force_int(rows[5][2].replace("*",""))
    #print(main.get_text())
    m = _goerlitz_i.search(main.get_text())
    i = force_int(m.group(1)) if m else None
    g = c - a - s - d
    update(sheets, 14626, c=c, cc=cc, d=d, dd=dd, g=g, s=s, i=i, sig="Bot", ignore_delta=True)
    return True

schedule.append(Task(12, 2, 14, 35, 600, goerlitz, 14626))
if __name__ == '__main__': goerlitz(googlesheets())
