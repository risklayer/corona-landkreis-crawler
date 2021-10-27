#!/usr/bin/python3
from botbase import *

_stand = re.compile(r"(\d\d\.\d\d.20\d\d)")
_bautzen_i = re.compile(r"(\w+)\s+davon benötigen eine intensiv", re.U)

def bautzen(sheets):
    soup = get_soup("https://www.landkreis-bautzen.de/corona-pandemie-im-landkreis-bautzen.php")
    main = soup.find(id="main")
    date = _stand.search(main.find(text=_stand)).group(1)
    date = check_date(date,"Bautzen")
    rows = [[x.text for x in row.findAll(["th","td"])] for row in main.findAll("tr")]
    #print(*rows, sep="\n")
    assert "Vergleich" in rows[0][2]
    assert "Gesamt" in rows[1][0]
    c, cc = force_int(rows[1][1].replace("*","")), force_int(rows[1][2].replace("*",""))
    assert "Genesen" in rows[2][0]
    g, gg = force_int(rows[2][1].replace("*","")), force_int(rows[2][2].replace("*",""))
    assert "Tod" in rows[3][0]
    d, dd = force_int(rows[3][1].replace("*","")), force_int(rows[3][2].replace("*",""))
    assert "station" in rows[5][0]
    s = force_int(rows[5][1].replace("*",""))
    assert "Quarantänen" in rows[6][0]
    q = force_int(rows[6][1].replace("*","")) + c-g-d
    update(sheets, 14625, c=c, cc=cc, d=d, dd=dd, g=g, gg=gg, s=s, q=q, sig="Bot", ignore_delta=True)
    return True

schedule.append(Task(13, 30, 17, 35, 600, bautzen, 14625))
if __name__ == '__main__': bautzen(googlesheets())
