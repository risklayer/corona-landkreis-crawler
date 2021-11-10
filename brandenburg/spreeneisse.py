#!/usr/bin/python3
from botbase import *

def spreeneisse(sheets):
    soup = get_soup("https://www.lkspn.de/aktuelles/coronavirus/corona-statistik.html")
    main = soup.find(id="content")
    rows = [[x.get_text().strip() for x in row.findAll("td")] for row in main.findAll("tr")]
    #print(*rows, sep="\n")
    date = check_date(rows[0][1].split(":",2)[-1], "Spree-Neisse")
    assert "Infektionen insgesamt" in rows[2][0]
    c = force_int(rows[2][1])
    assert "Veränderung" in rows[3][0]
    cc = force_int(rows[3][1])
    assert "davon geheilt" in rows[5][0]
    g = force_int(rows[5][1])
    assert "Todesfälle" in rows[6][0]
    d = force_int(rows[6][1])
    assert "Quarantäne" in rows[4][0]
    q = force_int(rows[4][1]) + c - g - d
    if q > 4 * (c - g - d): q = None # komischer Wert mal wieder
    update(sheets, 12071, c=c, cc=cc, d=d, g=g, q=q, sig="Bot", ignore_delta="mon")
    return True

schedule.append(Task(10, 2, 12, 35, 600, spreeneisse, 12071))
if __name__ == '__main__': spreeneisse(googlesheets())
