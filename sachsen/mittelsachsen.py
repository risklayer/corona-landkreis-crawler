#!/usr/bin/python3
from botbase import *

def mittelsachsen(sheets):
    import locale
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    soup = get_soup("https://www.landkreis-mittelsachsen.de/das-amt/behoerden/statistik.html")
    main = soup.find("main").find("table")
    rows = [[x.get_text() for x in row.findAll("td")] for row in main.findAll("tr")]
    #print(*rows, sep="\n")
    if not today().strftime("%-d. %B") in rows[0][0]: raise NotYetAvailableException("Mittelsachsen noch alt: "+rows[0][0]);
    assert "Bestätigte" in rows[0][0]
    c = force_int(rows[0][1])
    assert "Todesfälle" in rows[1][0]
    d = force_int(rows[1][1])
    assert "stationär" in rows[2][0]
    s = force_int(rows[2][1])
    assert "beatmet" in rows[3][0]
    i = force_int(rows[3][1])
    update(sheets, 14522, c=c, d=d, s=s, i=i, sig="Bot")
    return True

schedule.append(Task(12, 00, 15, 35, 360, mittelsachsen, 14522))
if __name__ == '__main__': mittelsachsen(googlesheets())
