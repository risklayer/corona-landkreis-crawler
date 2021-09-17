#!/usr/bin/python3
from botbase import *

def dithmarschen(sheets):
    soup = get_soup("https://www.dithmarschen.de/Neues-erfahren/Coronavirus/index.php?La=1&object=tx,2046.8521.1&kat=&kuo=2&sub=0")
    rows = soup.find(id="maincontent").find("table").findAll("tr")
    header = [[x.text.strip() for x in row.findAll("th")] for row in rows]
    rows = [[x.text.strip() for x in row.findAll("td")] for row in rows]
    #for row in rows: print(row)
    if not today().strftime("%d.%m.%Y") in header[0][1]: raise NotYetAvailableException("Dithmarschen noch alt: " + header[0][1])
    assert "Gesamtzahl" in rows[2][0]
    c, cc = force_int(rows[2][1]), force_int(rows[2][2],0)
    assert "Klinik" in rows[4][0]
    s = force_int(rows[4][1])
    assert "Genesene" in rows[6][0]
    g, gg = force_int(rows[6][1]), force_int(rows[6][2],0)
    assert "verstorbene" in rows[7][0]
    d, dd = force_int(rows[7][1]), force_int(rows[7][2],0)
    assert "Quarantäne" in rows[8][0]
    q = force_int(rows[8][1]) + c - d - g
    update(sheets, 1051, c=c, cc=cc, d=d, dd=dd, g=g, gg=gg, q=q, s=s, sig="Bot", ignore_delta=True)
    return True

schedule.append(Task(15, 2, 20, 35, 600, dithmarschen, 1051))
if __name__ == '__main__': dithmarschen(googlesheets())
